# GiftScout - Architecture & Implementation Guide

## Project Overview

**GiftScout** is an autonomous web agent that finds perfect gifts by:
1. Analyzing the gift recipient's persona (age, gender, interests)
2. Researching social media trends (Reddit, TikTok, YouTube)
3. Searching live products with real prices and buy links
4. Filtering recommendations by budget
5. Delivering actionable, shoppable gift suggestions

## Technology Stack Integration

### 1. **Tavily API** - Live Web Search
```
Purpose: Real-time product and trend discovery
Location: agent/tavily_search.py

Key Functions:
- search_social_trends(persona) → Finds trending gift discussions
- search_products(description, budget) → Locates items with pricing
- search_store_specific(product, store) → Checks Amazon, Etsy, etc.
- search_personalized_gifts(interests, age, budget) → Comprehensive search
```

**Usage in Agent:**
```python
@tool
def search_social_trends(persona: str) -> str:
    """Search TikTok, Reddit trends for gifts"""
    response = tavily_client.search(query=f"best gift for {persona}")
    return json.dumps({"trends": trends})
```

### 2. **Redis** - State Management & Caching
```
Purpose: Session persistence, search result caching, analytics
Location: agent/redis_utils.py
Connection: redis://localhost:6379 (configurable via REDIS_HOST/PORT)

Key Functions:
- cache_search_results(session_id, results) → Store findings
- get_cached_results(session_id) → Retrieve previous searches
- track_search_history(user_id, search_data) → Analytics
- save_user_preference(user_id, preferences) → Personalization
```

**Usage in Agent:**
```python
def save_gift_search_session(session_id, persona, budget, results):
    save_to_redis(session_id, "persona", persona)
    save_to_redis(session_id, "budget", budget)
    save_to_redis(session_id, "results", results)
```

### 3. **CopilotKit** - AI Orchestration
```
Purpose: Tool management, frontend-backend communication, UI rendering
Location: src/app/api/copilotkit/route.ts

Configuration:
- Agent ID: "giftscount_agent"
- Model: GPT-4o
- Tools: search_social_trends, search_products, filter_recommendations
- State Sync: Real-time updates to frontend
```

## Agent Workflow

### ReAct Loop (Reasoning + Acting)
```
1. USER INPUT
   "Find a gaming gift under $50 for a teenager"
   ↓
2. REASONING (chat_node)
   - Understand persona: "teenager into gaming"
   - Set budget: $50
   - Plan: search trends → search products → filter
   ↓
3. TOOL EXECUTION
   a. search_social_trends("teenager gamer")
      → Returns: TikTok trending games, Reddit discussions
   
   b. search_products("gaming gift under $50", 50)
      → Returns: Steam cards, controllers, indie games
   
   c. filter_recommendations(products, 50)
      → Returns: Top 5 items with links
   ↓
4. STATE PERSISTENCE (Redis)
   - Cache results for session
   - Track search history
   - Save user preferences
   ↓
5. RESPONSE
   Curated list with direct shopping links
```

## File Structure

```
agent/
├── agent.py              # Main LangGraph agent (ReAct pattern)
├── tavily_search.py      # Tavily search wrapper
├── redis_utils.py        # Redis operations
├── requirements.txt      # Python dependencies
├── langgraph.json        # LangGraph configuration
└── .env                  # Environment variables

src/app/
├── page.tsx             # Main UI component
├── layout.tsx           # App layout
└── api/
    └── copilotkit/
        └── route.ts     # CopilotKit runtime endpoint
```

## Environment Configuration

Create `.env` in the `agent/` directory:

```env
# OpenAI
OPENAI_API_KEY=sk-xxx

# Tavily API
TAVILY_API_KEY=tvly-xxx

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# CopilotKit
COPILOTKIT_API_KEY=your_key

# LangSmith (optional, for monitoring)
LANGSMITH_API_KEY=your_key
```

## Tool Specifications

### search_social_trends
- **Input:** persona (string describing gift recipient)
- **Output:** JSON with trending topics, sources, snippets
- **API:** Tavily search with social media filtering
- **Cache:** TTL 1 hour per session

### search_products_by_budget
- **Input:** item_description (string), max_price (float)
- **Output:** JSON array of products with URLs and prices
- **API:** Tavily search with budget constraints
- **Filtering:** Price-aware results

### filter_recommendations_by_budget
- **Input:** products (JSON string), budget (float)
- **Output:** Top 5 filtered recommendations sorted by relevance
- **Scoring:** Relevance score + budget alignment

### save_gift_search_session
- **Input:** session_id, persona, budget, results
- **Output:** Confirmation + session ID
- **Storage:** Redis (30-90 day retention)
- **Use Case:** User history & preferences

## Performance Optimization

### Caching Strategy
```python
# Short-lived cache for trending data (1 hour)
redis_client.setex(key, 3600, value)

# Long-lived cache for preferences (30 days)
redis_client.setex(key, 86400*30, value)

# Session history (90 days, LIFO queue)
redis_client.lpush(key, value)
redis_client.ltrim(key, 0, 99)
```

### Rate Limiting
- Tavily: Built-in API limits (configure per account)
- Redis: In-memory storage, no external limits
- CopilotKit: Concurrent user limits (configure)

## Testing

### Manual Testing
```bash
# Start development servers
npm run dev

# In browser sidebar, try:
"Find a gaming gift under $50 for a teenager"

# Check Redis data
redis-cli
> KEYS giftscount:*
> GET giftscount:results:session-id
```

### Debug Mode
```bash
npm run dev:debug
```
Enables LOG_LEVEL=debug for detailed tracing

## Evaluation Criteria Alignment

| Criterion | Implementation |
|-----------|-----------------|
| **Working Prototype** | ✅ Fully functional demo with UI + backend |
| **Core-Stack Integration** | ✅ Tavily (search) + Redis (state) + CopilotKit (orchestration) |
| **Innovation & Creativity** | ✅ Social-trend-aware gift finding with live web search |
| **Real-World Impact** | ✅ Solves concrete gift-finding problem for millions |
| **Theme Alignment** | ✅ Perfect embodiment of autonomous web browsing for execution |

## Future Enhancements

1. **Multi-store comparison** - Compare prices across Amazon, Etsy, Walmart
2. **Gift occasion support** - Birthdays, holidays, corporate gifts
3. **User reviews integration** - Aggregate ratings from multiple sources
4. **Image/video generation** - AI-generated gift idea visualizations
5. **Shareable wishlists** - Redis-backed collaborative lists
6. **Email notifications** - Price drops and new recommendations
7. **Mobile app** - React Native version with offline cache

## Troubleshooting

### "Agent connection failed"
- Ensure LangGraph dev server is running on port 8123
- Check `LANGGRAPH_DEPLOYMENT_URL` in environment

### "Redis connection refused"
- Verify Redis is running: `redis-cli ping`
- Check `REDIS_HOST` and `REDIS_PORT`

### "Tavily API errors"
- Verify `TAVILY_API_KEY` is set correctly
- Check Tavily rate limits on dashboard

### Search results are slow
- Check Redis cache hit rate: `redis-cli INFO stats`
- Verify network latency to Tavily API
