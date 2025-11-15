# GiftScout - System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      GIFTSCOUNT SYSTEM                          │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │   Browser UI    │
                    │  (localhost:3000)│
                    └────────┬─────────┘
                             │
                    ┌────────▼────────┐
                    │  CopilotSidebar │
                    │  (React Component)
                    └────────┬────────┘
                             │ HTTP
                    ┌────────▼────────────────────┐
                    │  CopilotKit Runtime        │
                    │  /api/copilotkit (route.ts)│
                    └────────┬───────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
    ┌───▼────┐           ┌──▼──┐            ┌───▼────┐
    │ Tavily │           │Tavily │           │ Tavily │
    │ Search │           │Search │           │ Search │
    │ (Social)│           │(Store)│           │(Trends)│
    └────────┘           └──────┘            └────────┘
        API Call            API Call            API Call
        │                   │                   │
    ┌───▼─────────────────┐
    │   Tavily API        │ (Live Web Search)
    │ api.tavily.com:443  │
    └─────────────────────┘
        └──────────────────────┬──────────────────────┐
                               │                      │
                        ┌──────▼─────┐        ┌──────▼─────┐
                        │   Reddit   │        │   TikTok   │
                        │  YouTube   │        │   Stores   │
                        └────────────┘        └────────────┘
```

## Agent Architecture (ReAct Pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│              GIFTSCOUNT LANGGRAPH AGENT                         │
│                  (agent.py)                                      │
└─────────────────────────────────────────────────────────────────┘

  User Query: "Find gaming gift under $50 for teenager"
        │
        ▼
  ┌────────────────────────┐
  │   chat_node            │
  │  (ReAct Reasoning)     │
  │  ↓                     │
  │ Understand request     │
  │ Plan tool calls        │
  │ Bind GPT-4o model      │
  └────────┬───────────────┘
           │ Route tools?
           │
      ┌────┴───────────────────┬─────────────────┐
      │                        │                 │
    ✅ Tool Calls           ❌ No Tools        ✅ Response
      │                        │                 │
      ▼                        ▼                 ▼
  ┌──────────────┐      ┌─────────────┐   ┌──────────────┐
  │  tool_node   │      │ tool_node   │   │  End Node    │
  │ (Execution)  │      │  (None)     │   │ (Response)   │
  │              │      │             │   │              │
  │ Executes:    │      │             │   │ Returns:     │
  │              │      │             │   │              │
  │ 1. search_   │      │             │   │ "Here are    │
  │    social_   │      │             │   │  top gaming  │
  │    trends()  │──────┤             │   │  gifts with  │
  │    → Tavily  │      │             │   │  links..."   │
  │              │      │             │   │              │
  │ 2. search_   │──────┤   SKIP      │   └──────┬───────┘
  │    products_ │      │             │          │
  │    by_budget │      │             │          ▼
  │    → Tavily  │      │             │    ┌──────────────┐
  │              │      │             │    │  CopilotKit  │
  │ 3. filter_   │      │             │    │ Updates UI   │
  │    recomm.   │      │             │    │              │
  │    → Logic   │      │             │    │ Displays in  │
  │              │      │             │    │ Sidebar      │
  │ 4. save_     │      │             │    └──────────────┘
  │    session   │      │             │
  │    → Redis   │      │             │
  └──────┬───────┘      └─────────────┘
         │ Update state
         │
      ┌──▼────────────────────────┐
      │  Update GiftScoutState    │
      │  ✓ persona_description   │
      │  ✓ budget                │
      │  ✓ tiktok_trends         │
      │  ✓ product_results       │
      │  ✓ filtered_recs         │
      └──────────┬────────────────┘
                 │ Continue conversation
                 ▼
            [Loop Back to chat_node]
```

## Data Flow - Complete Request

```
┌─ User Input ─────────────────────────────────────────┐
│ "Find gaming gifts under $50 for teenagers"         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Frontend (page.tsx)  │
        │ CopilotSidebar       │
        └──────────┬───────────┘
                   │ POST /api/copilotkit
                   ▼
        ┌──────────────────────────────────────┐
        │ Backend (route.ts)                   │
        │ CopilotRuntime                       │
        └──────────┬──────────────────────────┘
                   │ Create agent context
                   ▼
        ┌──────────────────────────────────────┐
        │ GiftScout Agent (agent.py)           │
        │                                      │
        │ 1. chat_node                         │
        │    - Parse: persona, budget          │
        │    - Plan: 3 tool calls              │
        │    - State: Update GiftScoutState    │
        └──────────┬──────────────────────────┘
                   │ Call tools
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Tool 1   │  │ Tool 2   │  │ Tool 3   │
│          │  │          │  │          │
│search_   │  │search_   │  │filter_   │
│social_   │  │products_ │  │recomm.   │
│trends()  │  │by_budget()  │by_budget()
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │             │             │
     ▼             ▼             ▼
┌────────────────────────────────────┐
│  Tavily API (tavily_search.py)    │
│  - search_social_trends()         │
│  - search_products()              │
│  - _score_by_relevance()          │
└────────────┬─────────────────────┘
             │ HTTP Calls
    ┌────────┴─────────┬──────────┐
    │                  │          │
    ▼                  ▼          ▼
 ┌────────┐        ┌────────┐ ┌────────┐
 │ Reddit │        │ TikTok │ │ Stores │
 └────────┘        └────────┘ └────────┘
    │                  │          │
    └────────────┬─────┴──────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Results JSON   │
        │ [products, urls]│
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ Aggregate Results   │
        │ in chat_node        │
        └────────┬─────────────┘
                 │
                 ▼
        ┌─────────────────────────────┐
        │ Tool 4: save_session        │
        │ → Redis (redis_utils.py)    │
        └────────┬────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────┐
        │ Redis Server                │
        │ (localhost:6379)            │
        │                             │
        │ giftscount:results:{id}     │
        │ giftscount:history:{user}   │
        │ giftscount:preferences:{id} │
        └────────┬────────────────────┘
                 │ Cached for 1 hour
                 │
                 ▼
        ┌─────────────────────────────┐
        │ Return Response             │
        │ - Top 5 items               │
        │ - With URLs & prices        │
        │ - Relevance scored          │
        └────────┬────────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │ CopilotKit Runtime       │
        │ (route.ts)               │
        └────────┬─────────────────┘
                 │ JSON Response
                 ▼
        ┌──────────────────────────┐
        │ Frontend UI              │
        │ Display Recommendations  │
        │ Show Shopping Links      │
        └──────────────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Layer                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ page.tsx - Main UI                                         │ │
│  │ - Hero section                                             │ │
│  │ - Features grid                                            │ │
│  │ - Recommendations display                                  │ │
│  │ - CopilotSidebar integration                               │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTP POST
                        │ /api/copilotkit
┌───────────────────────▼─────────────────────────────────────────┐
│                    API Layer                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ route.ts - CopilotKit Runtime                              │ │
│  │ - Manages agents                                           │ │
│  │ - Routes requests                                          │ │
│  │ - Synchronizes state                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────────┘
                        │ LangGraph RPC
                        │ localhost:8123
┌───────────────────────▼─────────────────────────────────────────┐
│                    Agent Layer                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ agent.py - GiftScout Agent                                 │ │
│  │ - GiftScoutState (manages context)                         │ │
│  │ - chat_node (reasoning)                                    │ │
│  │ - tool_node (execution)                                    │ │
│  │ - Tool definitions                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Search Layer  │ │Logic Layer   │ │Storage Layer │
│              │ │              │ │              │
│tavily_search │ │agent.py      │ │redis_utils   │
│.py           │ │(tools)       │ │.py           │
│              │ │              │ │              │
│- search_     │ │- filter_     │ │- cache       │
│  social_     │ │  recomm.     │ │- history     │
│  trends()    │ │  by_budget() │ │- prefs       │
│- search_     │ │              │ │              │
│  products()  │ │              │ │              │
│- _parse_     │ │              │ │              │
│  results()   │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        │ HTTP          │               │ Network
        │ to            │               │ calls
        │ Tavily        │               │ to
        │ API           │               │ Redis
        │               │               │
        ▼               ▼               ▼
    [Web API]      [Logic]          [Redis]
    [External      [Internal]       [External]
    [Services]     [Processing]     [Cache]
```

## State Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│           GiftScoutState (agent.py)                             │
│                                                                  │
│  MessagesState (inherited)                                      │
│  ├─ messages: List[BaseMessage]                               │
│  └─ [CopilotKit fields]                                        │
│                                                                  │
│  GiftScoutState (custom)                                        │
│  ├─ persona_description: str                                    │
│  ├─ budget: float                                              │
│  ├─ tiktok_trends: List[str]                                   │
│  ├─ social_insights: List[str]                                 │
│  ├─ product_results: List[dict]                                │
│  ├─ filtered_recommendations: List[dict]                       │
│  ├─ search_session_id: str                                     │
│  └─ tools: List[Any]                                           │
│                                                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐   ┌─────────┐   ┌──────────┐
    │Session │   │Redis    │   │Frontend  │
    │Memory  │   │Cache    │   │State     │
    │(agent) │   │(persist)│   │(UI)      │
    └────────┘   └─────────┘   └──────────┘

1. Agent builds state during execution
2. Redis saves for persistence (via save_gift_search_session)
3. Frontend receives via CopilotKit
4. UI updates in real-time
```

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Redis Caching Layers                         │
└─────────────────────────────────────────────────────────────────┘

Layer 1: Session Results (1 hour TTL)
┌────────────────────────────────────────────┐
│ Key: giftscount:results:{session_id}      │
│ Value: {products, trends, recommendations}│
│ TTL: 3600 seconds (1 hour)                │
│ Usage: Quick re-access same session       │
└────────────────────────────────────────────┘

Layer 2: User Preferences (30 days TTL)
┌────────────────────────────────────────────┐
│ Key: giftscount:preferences:{user_id}     │
│ Value: {interests, past_budgets, etc}     │
│ TTL: 2592000 seconds (30 days)            │
│ Usage: Personalization                    │
└────────────────────────────────────────────┘

Layer 3: Search History (90 days, LIFO)
┌────────────────────────────────────────────┐
│ Key: giftscount:history:{user_id}         │
│ Type: List (LPUSH, LTRIM)                 │
│ Size: Last 100 entries                    │
│ TTL: 7776000 seconds (90 days)            │
│ Usage: Analytics, recommendations         │
└────────────────────────────────────────────┘

Layer 4: Search Counters (No expiry)
┌────────────────────────────────────────────┐
│ Key: giftscount:counter:{search_type}     │
│ Value: Integer counter                    │
│ Usage: Trending searches analytics        │
└────────────────────────────────────────────┘
```

This architecture enables:
- ✅ Fast response times (cached queries <100ms)
- ✅ Persistent state across sessions
- ✅ User personalization
- ✅ Analytics tracking
- ✅ Scalable design
