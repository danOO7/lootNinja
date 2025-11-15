# CopilotKit Configuration Guide

## Overview

CopilotKit is configured to work with:
- **OpenAI Adapter**: Handles LLM reasoning (uses GPT-4o)
- **Two Registered Agents**: `giftscount_agent` and `sample_agent`
- **LangGraph Backend**: Hosted at `http://localhost:8123` during development
- **Public API Key**: `ck_pub_2f3c4528d076fade691d644551bac4d3`

## Backend Configuration

### File: `/src/app/api/copilotkit/route.ts`

**Key Components:**

1. **OpenAI Adapter**
   ```typescript
   const serviceAdapter = new OpenAIAdapter({
     model: "gpt-4o",
   });
   ```
   - Handles all LLM-based reasoning and chat completions
   - Uses `OPENAI_API_KEY` from environment variables
   - Uses GPT-4o for superior gift discovery reasoning

2. **Registered Agents**
   ```typescript
   agents: {
     "giftscount_agent": new LangGraphAgent({...}),
     "sample_agent": new LangGraphAgent({...}),
   }
   ```

   - **giftscount_agent**: Primary agent for gift discovery
     - Connects to: `http://localhost:8123/giftscount_agent`
     - Handles: Social trend search, product discovery, recommendation curation
   
   - **sample_agent**: Fallback agent for compatibility
     - Also routes to: `http://localhost:8123/giftscount_agent` 
     - Provides redundancy and testing capability

3. **Runtime Endpoint**
   - POST `/api/copilotkit`: Main request handler
   - Processes messages, tool calls, and agent state

## Frontend Configuration

### File: `/src/app/page.tsx`

**Key Components:**

1. **CopilotKit Wrapper**
   ```typescript
   <CopilotKit 
     publicApiKey="ck_pub_2f3c4528d076fade691d644551bac4d3"
     runtimeUrl="/api/copilotkit"
   >
   ```
   - Enables CopilotKit functionality
   - Authenticates with public API key
   - Connects to backend runtime endpoint

2. **CopilotSidebar**
   ```typescript
   <CopilotSidebar
     instructions="You are GiftScout, an expert..."
     defaultOpen={true}
   />
   ```
   - Displays conversational interface
   - Pre-loaded with GiftScout system prompt
   - Opens by default on page load
   - Automatically uses registered agents

## How It Works

### User Interaction Flow

1. **User sends message** via CopilotSidebar
   ↓
2. **Frontend** sends POST to `/api/copilotkit`
   ↓
3. **OpenAI Adapter** processes message with GPT-4o
   ↓
4. **Runtime** routes to appropriate agent (giftscount_agent or sample_agent)
   ↓
5. **LangGraph Agent** at port 8123 processes request
   - Searches for trends (Tavily API)
   - Finds products
   - Caches in Redis
   - Returns recommendations
   ↓
6. **Response** sent back to frontend
   ↓
7. **UI** displays results in sidebar

## Environment Variables Required

```env
# Required for OpenAI Adapter
OPENAI_API_KEY=sk_...

# LangGraph Configuration
LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123
LANGSMITH_API_KEY=ls_...

# CopilotKit Public Key (already in code)
COPILOTKIT_API_KEY=ck_pub_2f3c4528d076fade691d644551bac4d3

# Tavily API (for agent)
TAVILY_API_KEY=tvly-...

# Redis (for caching)
REDIS_URL=redis://localhost:6379
```

## Agents Explained

### giftscount_agent
- **Purpose**: Main gift discovery and recommendation engine
- **Capabilities**:
  - Searches social trends (Reddit, TikTok, blogs)
  - Finds real products with pricing
  - Filters by budget
  - Returns shopping links
  - Caches results for performance
  - Remembers user preferences

### sample_agent
- **Purpose**: Testing and fallback
- **Routing**: Also uses giftscount_agent backend
- **Use Case**: Can be used for testing UI with multiple agents

## Testing the Setup

### 1. Start Development Server
```bash
npm run dev
```
- UI: http://localhost:3003
- Agent: http://localhost:8123
- API Docs: http://localhost:8123/docs

### 2. Test in UI
1. Open browser to http://localhost:3003
2. Click on CopilotSidebar (right side)
3. Type: "Find a gaming gift under $50 for a teenager"
4. Agent will:
   - Search trends
   - Find products
   - Return recommendations

### 3. Monitor Backend
```bash
# Check agent logs
curl http://localhost:8123/docs

# View registered graphs
curl http://localhost:8123/graphs
```

## Troubleshooting

### Issue: "Agent fetch failed"
**Solution**: Ensure agent server is running on port 8123
```bash
npm run dev:agent
```

### Issue: "Invalid adapter configuration"
**Solution**: Verify OpenAIAdapter is imported and serviceAdapter is passed to endpoint

### Issue: "No such agent"
**Solution**: Check agent names match exactly:
- `giftscount_agent` ✓
- `sample_agent` ✓

### Issue: "OPENAI_API_KEY not set"
**Solution**: Add to `.env`:
```
OPENAI_API_KEY=sk_...
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                     │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  CopilotKit Wrapper (publicApiKey)             │    │
│  │  ├─ CopilotSidebar                            │    │
│  │  │  └─ User Input                              │    │
│  │  └─ Main Page UI                              │    │
│  └────────────────────────────────────────────────┘    │
└────────────┬──────────────────────────────────────────┘
             │ POST /api/copilotkit
             ↓
┌─────────────────────────────────────────────────────────┐
│              Backend (Next.js API Route)                │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  CopilotRuntime                                │    │
│  │  ├─ OpenAI Adapter (GPT-4o)                    │    │
│  │  └─ Agents:                                    │    │
│  │     ├─ giftscount_agent                       │    │
│  │     └─ sample_agent                           │    │
│  └────────────────────────────────────────────────┘    │
└────────────┬──────────────────────────────────────────┘
             │ HTTP (port 8123)
             ↓
┌─────────────────────────────────────────────────────────┐
│          LangGraph Agent Server (Python)                │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  GiftScout Agent (agent.py)                    │    │
│  │  ├─ Tavily Search (web search)                 │    │
│  │  ├─ Redis Cache (session storage)              │    │
│  │  └─ Recommendations (curated results)          │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Next Steps

1. ✅ Backend configured with OpenAI Adapter
2. ✅ Agents registered (giftscount_agent, sample_agent)
3. ✅ Frontend connected to backend
4. → Test the full flow with `npm run dev`
5. → Monitor logs for issues
6. → Deploy to production

## Production Considerations

1. **Update LANGGRAPH_DEPLOYMENT_URL** to production LangGraph instance
2. **Use managed OpenAI** deployment or API
3. **Enable Redis** authentication
4. **Secure API keys** with environment variables
5. **Monitor agent performance** with LangSmith
6. **Add rate limiting** on `/api/copilotkit`
7. **Implement logging** for audit trails
