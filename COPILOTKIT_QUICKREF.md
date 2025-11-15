# CopilotKit Configuration Quick Reference

## ✅ What's Configured

### Backend (`/src/app/api/copilotkit/route.ts`)
- ✅ **OpenAI Adapter** with GPT-4o model
- ✅ **Two Agents Registered**:
  - `giftscount_agent`: Primary gift discovery
  - `sample_agent`: Fallback/testing
- ✅ **LangGraph Integration** at `http://localhost:8123`
- ✅ **Service Adapter** for LLM communication

### Frontend (`/src/app/page.tsx`)
- ✅ **CopilotKit Wrapper** with public API key
- ✅ **Runtime URL** pointing to `/api/copilotkit`
- ✅ **CopilotSidebar** with GiftScout system prompt
- ✅ **Auto-open** on page load

## 🚀 How to Use

### Start Development
```bash
cd /home/dbu/ai-hackaton/lootNinja
npm run dev
```

**Expected Output:**
```
[ui] ▲ Next.js 16.0.1 - Local: http://localhost:3003
[agent] - 🚀 API: http://localhost:8123
```

### Access the App
1. Open http://localhost:3003
2. Look for CopilotSidebar on the right
3. Start chatting with GiftScout!

### Example Prompts
- "Find a gaming gift under $50 for a teenager"
- "What are trending tech gifts this season?"
- "Recommend a gift for someone who loves cooking"
- "Find gifts for a 5-year-old budget $30"

## 📊 Agent Information

### giftscount_agent
| Property | Value |
|----------|-------|
| **Type** | LangGraphAgent |
| **Graph ID** | giftscount_agent |
| **URL** | http://localhost:8123 |
| **Purpose** | Gift discovery & recommendations |
| **Uses** | Tavily API + Redis + GPT-4o |

### sample_agent
| Property | Value |
|----------|-------|
| **Type** | LangGraphAgent |
| **Graph ID** | giftscount_agent |
| **URL** | http://localhost:8123 |
| **Purpose** | Testing & fallback |
| **Routing** | Also uses giftscount_agent |

## 🔧 Configuration Details

### Public API Key
```
ck_pub_2f3c4528d076fade691d644551bac4d3
```
(Set in `page.tsx`)

### Runtime Endpoint
```
/api/copilotkit
```
(Backend POST handler)

### LangGraph Deployment
```
http://localhost:8123 (development)
process.env.LANGGRAPH_DEPLOYMENT_URL (production)
```

## ✨ Features Enabled

| Feature | Status | Details |
|---------|--------|---------|
| OpenAI LLM | ✅ | GPT-4o via OpenAI Adapter |
| Agent Routing | ✅ | 2 agents registered |
| Social Trends | ✅ | Via Tavily API search |
| Product Search | ✅ | Via Tavily API integration |
| Caching | ✅ | Redis session storage |
| Preferences | ✅ | User preference tracking |
| Sidebar Chat | ✅ | Full UI included |

## 📝 Required Environment Variables

```env
# OpenAI (for adapter)
OPENAI_API_KEY=sk_...

# LangGraph (optional, defaults to localhost:8123)
LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123

# Tavily Search
TAVILY_API_KEY=tvly-...

# Redis
REDIS_URL=redis://localhost:6379

# LangSmith (optional)
LANGSMITH_API_KEY=ls_...
```

## 🐛 Troubleshooting

### Agents not showing up?
- Check: Agents are registered as object keys in runtime
- Solution: Verify `/src/app/api/copilotkit/route.ts` has both agents

### "Agent fetch failed"?
- Check: LangGraph server running on 8123
- Solution: Run `npm run dev:agent` in separate terminal

### No LLM responses?
- Check: OPENAI_API_KEY is set
- Solution: Add to `.env` file

### Sidebar not appearing?
- Check: CopilotKit wrapper and runtimeUrl correct
- Solution: Verify `page.tsx` has publicApiKey prop

## 📚 Files Modified

| File | Changes |
|------|---------|
| `src/app/api/copilotkit/route.ts` | Added OpenAI adapter + 2 agents |
| `src/app/page.tsx` | Added public API key to CopilotKit wrapper |
| `COPILOTKIT_SETUP.md` | Full configuration guide |

## 🎯 Next: Test the Setup

```bash
# Terminal 1
npm run dev

# Terminal 2 (optional, for monitoring)
curl http://localhost:8123/docs
```

Then open http://localhost:3003 and start chatting!
