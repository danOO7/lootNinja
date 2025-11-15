# GiftScout Agent - Pydantic AI

A CopilotKit-integrated agent built with [Pydantic AI](https://ai.pydantic.dev/) for discovering perfect gifts using social trends and product search.

## Features

- 🎁 **Smart Gift Discovery**: Uses AI to understand gift recipients and find perfect matches
- 🔍 **Social Trend Analysis**: Searches Reddit, TikTok, and blogs for trending gift ideas
- 💰 **Budget-Aware**: Filters recommendations within specified budget constraints
- 💾 **Redis Caching**: Persists search sessions for future reference
- 🌐 **Live Web Search**: Uses Tavily API for current product availability and pricing

## Technology Stack

- **Framework**: [Pydantic AI](https://ai.pydantic.dev/)
- **LLM**: OpenAI GPT-4o Mini
- **State Management**: Pydantic models
- **Web Search**: Tavily API
- **Caching**: Redis
- **Server**: Uvicorn + AG UI
- **Integration**: CopilotKit

## Setup

### Prerequisites

- Python 3.12+
- Redis running locally (or remote Redis server)
- API Keys:
  - OpenAI API key
  - Tavily API key

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or using uv (faster):
uv sync
```

### Environment Variables

Create a `.env` file in the agent directory:

```env
# Required
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...

# Optional (defaults shown)
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Running

### Development

```bash
cd agent/src
python -m main
```

The agent will start on `http://localhost:8000` with AG UI dashboard.

### From project root

```bash
npm run dev:agent
```

## Agent Architecture

### State Model: `GiftScoutState`

Tracks:
- `persona_description`: Gift recipient profile
- `budget`: Maximum price constraint
- `search_session_id`: Unique session identifier
- `tiktok_trends`: Trending topics found
- `product_results`: Search results with scores
- `filtered_recommendations`: Curated top 5 recommendations

### Tools

1. **search_social_trends**
   - Searches for trending gift discussions
   - Input: Persona description
   - Output: Trending topics and sources

2. **search_products_by_budget**
   - Finds products matching criteria
   - Input: Item description, max price
   - Output: Products with links and relevance scores

3. **filter_recommendations_by_budget**
   - Curates top recommendations
   - Sorts by relevance and budget fit
   - Returns top 5 results

4. **save_gift_search_session**
   - Persists search results to Redis
   - Enables session retrieval later

## Integration with CopilotKit

The agent is accessed through CopilotKit's runtime at `/api/copilotkit`:

```bash
# Frontend connects to:
POST /api/copilotkit

# Which routes to agent at:
http://localhost:8000
```

### Example Flow

1. User: "Find a gaming gift under $50 for a teenager"
2. Agent searches social trends for "gaming teenager gifts"
3. Agent searches products: "gaming gift under $50"
4. Agent filters and ranks by relevance
5. Agent returns curated recommendations with links

## Development

### Adding New Tools

```python
@agent.tool
def my_new_tool(ctx: RunContext[StateDeps[GiftScoutState]], param: str) -> str:
    """Tool description for the model."""
    # Update state as needed
    ctx.deps.state.some_field = value
    return json.dumps({"result": "data"})
```

### Testing

```bash
python -m pytest test_agent.py -v
```

## Performance Considerations

- **Tavily Search**: Each search costs API credits (configurable max_results)
- **Redis Expiry**: Search results cached for 1 hour
- **Parallel Tool Calls**: Disabled for sequential, deterministic behavior
- **Model**: Using gpt-4o-mini for cost-effectiveness

## Troubleshooting

### Redis Connection Error
```
Failed to connect to Redis
```
Ensure Redis is running: `redis-server` or update `REDIS_HOST`/`REDIS_PORT`

### Tavily API Key Error
```
TAVILY_API_KEY not set - search functionality may not work
```
Add `TAVILY_API_KEY` to `.env`

### OpenAI API Error
```
Missing OPENAI_API_KEY
```
Set `OPENAI_API_KEY` in environment

## Resources

- [Pydantic AI Docs](https://ai.pydantic.dev/)
- [CopilotKit Docs](https://docs.copilotkit.ai/)
- [AG UI Documentation](https://ai.pydantic.dev/ag-ui/)
- [Tavily API](https://tavily.com/)
