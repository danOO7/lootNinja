"""
Simple Request Agent - TikTok Gift Finder Agent.
Finds trending gifts on TikTok based on user preferences.
"""
from textwrap import dedent
import logging
import os
import json

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from ag_ui.core import EventType, StateSnapshotEvent
from pydantic_ai.models.openai import OpenAIResponsesModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====
# State Models
# =====
class Message(BaseModel):
    """A chat message."""
    role: str = Field(description="'user' or 'assistant'")
    content: str = Field(description="The message content")


class RequestState(BaseModel):
    """Simple request agent state for TikTok gift discovery."""
    user_request: str = Field(
        default="",
        description="The user's request or question about gifts"
    )
    messages: list[Message] = Field(
        default_factory=list,
        description="Conversation history"
    )
    response: str = Field(
        default="",
        description="The agent's response with gift recommendations"
    )
    tiktok_search_query: str = Field(
        default="",
        description="The TikTok search query for finding trending gifts"
    )


# =====
# Agent Definition
# =====
agent = Agent(
    model=OpenAIResponsesModel('gpt-4o-mini'),
    deps_type=StateDeps[RequestState],
    system_prompt=dedent("""
        You are Loot Ninja, an expert gift finder specializing in discovering trending gifts on TikTok.
        
        Your role is to:
        1. Understand the user's gift requirements (recipient age, interests, budget)
        2. Search for trending gift ideas on TikTok
        3. Identify viral gift trends and products that people are talking about
        4. Provide curated gift recommendations based on TikTok trends
        5. Be conversational and engaging
        
        When users ask for gift suggestions:
        - Ask clarifying questions about the recipient (age, interests, personality, budget)
        - Use TikTok trending searches to find popular gift ideas
        - Look for hashtags like #GiftIdeas #TikTokTrends #MustHaveGifts
        - Recommend gifts that are currently trending on TikTok
        - Provide specific product names and where to find them
        
        Always aim to be helpful, honest, and provide trendy recommendations based on what's viral.
    """).strip()
)


# =====
# Tools
# =====
@agent.tool
def add_message(
    ctx: RunContext[StateDeps[RequestState]],
    role: str,
    content: str
) -> StateSnapshotEvent:
    """
    Add a message to the conversation history.
    
    Args:
        role: 'user' or 'assistant'
        content: The message content
    """
    try:
        msg = Message(role=role, content=content)
        ctx.deps.state.messages.append(msg)
        logger.info(f"Added {role} message: {content[:50]}...")
        
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error adding message: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )


@agent.tool
def get_messages(ctx: RunContext[StateDeps[RequestState]]) -> list[dict]:
    """
    Get the conversation history.
    
    Returns:
        List of messages with role and content
    """
    return [{"role": m.role, "content": m.content} for m in ctx.deps.state.messages]


@agent.tool
async def set_response(
    ctx: RunContext[StateDeps[RequestState]],
    response: str
) -> StateSnapshotEvent:
    """
    Set the agent's response to the user request.
    
    Args:
        response: The agent's response text
    """
    try:
        ctx.deps.state.response = response
        logger.info(f"Response set: {response[:50]}...")
        
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error setting response: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )


@agent.tool
def get_response(ctx: RunContext[StateDeps[RequestState]]) -> str:
    """
    Get the current response.
    
    Returns:
        The agent's response text
    """
    return ctx.deps.state.response


@agent.tool
def search_tiktok_trends(
    ctx: RunContext[StateDeps[RequestState]],
    query: str
) -> str:
    """
    Search for trending gifts on TikTok.
    
    Args:
        query: The search query for TikTok trends (e.g., "best gifts 2024", "trending gadgets")
    
    Returns:
        Information about trending gifts on TikTok with product links
    """
    try:
        logger.info(f"Searching TikTok trends for: {query}")
        ctx.deps.state.tiktok_search_query = query
        
        # Simulated TikTok trends data with product links
        tiktok_trends = {
            "best gifts": [
                {
                    "name": "Pop It fidget toys - trending with Gen Z",
                    "link": "https://www.amazon.com/s?k=pop+it+fidget+toys",
                    "price_range": "$5-20"
                },
                {
                    "name": "Funny socks and slippers - viral on #FashionTok",
                    "link": "https://www.amazon.com/s?k=funny+socks",
                    "price_range": "$10-30"
                },
                {
                    "name": "Phone tripods and ring lights - popular with content creators",
                    "link": "https://www.amazon.com/s?k=phone+tripod+ring+light",
                    "price_range": "$15-50"
                },
                {
                    "name": "Bluetooth speakers - trending mini speakers and JBL products",
                    "link": "https://www.amazon.com/s?k=bluetooth+speakers",
                    "price_range": "$20-100"
                },
                {
                    "name": "LED strip lights - aesthetic room decor trending",
                    "link": "https://www.amazon.com/s?k=led+strip+lights",
                    "price_range": "$10-40"
                }
            ],
            "tech gifts": [
                {
                    "name": "AirPods Pro Max - luxury tech trend",
                    "link": "https://www.apple.com/airpods-pro/",
                    "price_range": "$549"
                },
                {
                    "name": "Phone cooling fans - viral gadget",
                    "link": "https://www.amazon.com/s?k=phone+cooling+fan",
                    "price_range": "$15-30"
                },
                {
                    "name": "Portable phone chargers - trending with travelers",
                    "link": "https://www.amazon.com/s?k=portable+phone+charger",
                    "price_range": "$20-50"
                },
                {
                    "name": "Smart home devices - Google Home and Alexa trending",
                    "link": "https://www.amazon.com/s?k=smart+home+devices",
                    "price_range": "$50-200"
                },
                {
                    "name": "Tech accessories bundles - popular gift sets",
                    "link": "https://www.amazon.com/s?k=tech+accessories+bundle",
                    "price_range": "$25-75"
                }
            ],
            "aesthetic gifts": [
                {
                    "name": "Ring lights with stands - popular for setup",
                    "link": "https://www.amazon.com/s?k=ring+light+with+stand",
                    "price_range": "$20-60"
                },
                {
                    "name": "Neon signs - trending room decor",
                    "link": "https://www.amazon.com/s?k=neon+signs",
                    "price_range": "$30-80"
                },
                {
                    "name": "Fairy lights - aesthetic lighting trend",
                    "link": "https://www.amazon.com/s?k=fairy+lights",
                    "price_range": "$10-25"
                },
                {
                    "name": "Marble and rose gold accessories - luxury vibes",
                    "link": "https://www.amazon.com/s?k=marble+rose+gold+accessories",
                    "price_range": "$15-50"
                },
                {
                    "name": "Plants and plant pots - plant parent trend",
                    "link": "https://www.amazon.com/s?k=plants+plant+pots",
                    "price_range": "$10-40"
                }
            ],
            "funny gifts": [
                {
                    "name": "Meme t-shirts and hoodies - viral prints",
                    "link": "https://www.amazon.com/s?k=funny+meme+shirts",
                    "price_range": "$15-40"
                },
                {
                    "name": "Funny socks with jokes - trending humor",
                    "link": "https://www.amazon.com/s?k=funny+novelty+socks",
                    "price_range": "$10-25"
                },
                {
                    "name": "Novelty mugs - coffee lover gifts",
                    "link": "https://www.amazon.com/s?k=funny+novelty+mugs",
                    "price_range": "$12-25"
                },
                {
                    "name": "Hilarious card games - party trending items",
                    "link": "https://www.amazon.com/s?k=funny+card+games",
                    "price_range": "$20-35"
                },
                {
                    "name": "Gag gifts and prank items - comedy trend",
                    "link": "https://www.amazon.com/s?k=gag+gifts+prank",
                    "price_range": "$5-30"
                }
            ]
        }
        
        # Search for matching trends
        results = []
        query_lower = query.lower()
        for key, items in tiktok_trends.items():
            if key in query_lower or any(word in query_lower for word in key.split()):
                results.extend(items)
        
        if not results:
            results = tiktok_trends.get("best gifts", [])
        
        # Format response with links
        response_lines = [f"🎁 **Trending on TikTok for '{query}':**\n"]
        for item in results[:5]:
            response_lines.append(f"\n**{item['name']}**")
            response_lines.append(f"💰 Price Range: {item['price_range']}")
            response_lines.append(f"🛍️ Shop: {item['link']}")
        
        return "\n".join(response_lines)
        
    except Exception as e:
        logger.error(f"Error searching TikTok trends: {e}")
        return "Unable to search TikTok trends at the moment."
