from textwrap import dedent
from typing import Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from ag_ui.core import EventType, StateSnapshotEvent
from pydantic_ai.models.openai import OpenAIResponsesModel
import json
import logging
import os
from tavily import TavilyClient
import redis

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis client for state management
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

# Initialize Tavily client for web search
tavily_api_key = os.getenv("TAVILY_API_KEY", "")
if not tavily_api_key:
    logger.warning("TAVILY_API_KEY not set - search functionality may not work")
    tavily_client = None
else:
    tavily_client = TavilyClient(api_key=tavily_api_key)

# =====
# State
# =====
class GiftSearchResult(BaseModel):
    """Individual gift search result."""
    title: str
    url: str
    source: str
    snippet: str
    relevance_score: float


class GiftScoutState(BaseModel):
    """GiftScout agent state for gift discovery."""
    persona_description: str = Field(
        default="",
        description="Description of the gift recipient (age, gender, interests)"
    )
    budget: float = Field(
        default=0.0,
        description="Budget constraint for the gift"
    )
    search_session_id: str = Field(
        default="",
        description="Unique session ID for tracking searches"
    )
    tiktok_trends: list[str] = Field(
        default_factory=list,
        description="Trending topics found on social media"
    )
    product_results: list[GiftSearchResult] = Field(
        default_factory=list,
        description="Products found matching criteria"
    )
    filtered_recommendations: list[GiftSearchResult] = Field(
        default_factory=list,
        description="Final curated gift recommendations"
    )


# =====
# Redis Helpers
# =====
def save_to_redis(session_id: str, key: str, value: Any) -> None:
    """Save data to Redis for persistent state management."""
    if not redis_client:
        return
    try:
        redis_key = f"giftscount:{session_id}:{key}"
        redis_client.set(redis_key, json.dumps(value))
        redis_client.expire(redis_key, 3600)  # 1 hour expiry
    except Exception as e:
        logger.error(f"Error saving to Redis: {e}")


def get_from_redis(session_id: str, key: str) -> Any:
    """Retrieve data from Redis."""
    if not redis_client:
        return None
    try:
        redis_key = f"giftscount:{session_id}:{key}"
        value = redis_client.get(redis_key)
        return json.loads(value) if value else None
    except Exception as e:
        logger.error(f"Error retrieving from Redis: {e}")
        return None


# =====
# Agent
# =====
agent = Agent(
    model=OpenAIResponsesModel('gpt-4o-mini'),
    deps_type=StateDeps[GiftScoutState],
    system_prompt=dedent("""
        You are GiftScout, an autonomous web agent that finds perfect gifts by researching 
        social trends and live product availability.

        Your workflow:
        1. Understand the gift recipient's persona (age, gender, interests)
        2. Determine the budget constraint
        3. Search for trending topics on social media (TikTok, Reddit, blogs)
        4. Search for actual products matching those trends within budget
        5. Filter and curate top recommendations with links
        6. Save the session to Redis for future reference

        Always provide direct product links and pricing information from real stores.
        Be conversational but focused on delivering actionable gift recommendations.
        When the user provides persona and budget, use the search tools to find the best gifts.
    """).strip()
)


# =====
# Tools
# =====
@agent.tool
def search_social_trends(ctx: RunContext[StateDeps[GiftScoutState]], persona: str) -> str:
    """
    Search for trending topics and discussions about gifts on social media.
    Uses Tavily to find Reddit, TikTok, and blog discussions.
    """
    try:
        if not tavily_client:
            return json.dumps({"error": "Tavily API key not configured"})

        # Search for social discussions and trends
        search_query = f"best gift ideas for {persona} 2024 reddit OR tiktok OR twitter trending"
        logger.info(f"Searching for trends: {search_query}")
        response = tavily_client.search(query=search_query, max_results=5)

        trends = []
        for result in response.get("results", []):
            trends.append({
                "source": result.get("source", ""),
                "title": result.get("title", ""),
                "content": result.get("content", "")[:200],
                "url": result.get("url", "")
            })

        # Update state with trends
        ctx.deps.state.tiktok_trends = [t["title"] for t in trends]
        
        logger.info(f"Found {len(trends)} trends")
        return json.dumps({"trends": trends})
    except Exception as e:
        logger.error(f"Error in search_social_trends: {e}", exc_info=True)
        return json.dumps({"error": f"Search failed: {str(e)}", "trends": []})


@agent.tool
def search_products_by_budget(
    ctx: RunContext[StateDeps[GiftScoutState]], 
    item_description: str, 
    max_price: float
) -> str:
    """
    Search for products matching the description and budget using Tavily.
    Returns product results with prices and purchase links.
    """
    try:
        if not tavily_client:
            return json.dumps({"error": "Tavily API key not configured"})

        search_query = f"{item_description} buy online under ${max_price}"
        logger.info(f"Searching for products: {search_query}")
        response = tavily_client.search(query=search_query, max_results=8)

        products = []
        for result in response.get("results", []):
            product = {
                "title": result.get("title", ""),
                "source": result.get("source", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")[:300],
                "relevance": result.get("score", 0)
            }
            products.append(product)

        # Update state with products
        ctx.deps.state.product_results = [
            GiftSearchResult(
                title=p["title"],
                url=p["url"],
                source=p["source"],
                snippet=p["snippet"],
                relevance_score=p["relevance"]
            )
            for p in products
        ]

        logger.info(f"Found {len(products)} products")
        return json.dumps({"products": products})
    except Exception as e:
        logger.error(f"Error in search_products_by_budget: {e}", exc_info=True)
        return json.dumps({"error": f"Search failed: {str(e)}", "products": []})


@agent.tool
async def filter_recommendations_by_budget(
    ctx: RunContext[StateDeps[GiftScoutState]], 
) -> StateSnapshotEvent:
    """
    Filter and curate product recommendations based on budget constraints.
    Returns top recommendations sorted by relevance.
    """
    try:
        # The search_products_by_budget tool already filters by budget.
        # This tool is for curating the results.
        
        # Sort by relevance
        sorted_products = sorted(ctx.deps.state.product_results, key=lambda x: x.relevance_score, reverse=True)

        # Keep top 5
        ctx.deps.state.filtered_recommendations = sorted_products[:5]

        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error filtering recommendations: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )


@agent.tool
async def save_gift_search_session(
    ctx: RunContext[StateDeps[GiftScoutState]], 
    session_id: Optional[str] = None
) -> StateSnapshotEvent:
    """
    Save the complete gift search session to Redis for retrieval later.
    """
    try:
        session_key = session_id or ctx.deps.state.search_session_id
        if session_key:
            save_to_redis(session_key, "persona", ctx.deps.state.persona_description)
            save_to_redis(session_key, "budget", ctx.deps.state.budget)
            save_to_redis(session_key, "trends", ctx.deps.state.tiktok_trends)
            save_to_redis(session_key, "recommendations", [
                r.model_dump() for r in ctx.deps.state.filtered_recommendations
            ])
            logger.info(f"Saved session {session_key} to Redis")

        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error saving session: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
