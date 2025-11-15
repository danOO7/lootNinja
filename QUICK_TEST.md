# Quick Start - Testing the Fixed Agent

## Prerequisites
- Agent virtual environment set up: `/agent/.venv/`
- Both `OPENAI_API_KEY` and `PYDANTIC_AI_URL` in `.env.local`

## Method 1: Run Simple Agent + UI Together

```bash
npm run dev:simple
```

This will start:
- **UI** on http://localhost:3000 (Next.js dev server)
- **Simple Agent** on http://localhost:8000 (Python/FastAPI)

Then:
1. Open http://localhost:3000
2. Type "Hello, agent!"
3. Agent should respond

## Method 2: Run Separately (Better for Debugging)

**Terminal 1 - Start the Agent:**
```bash
npm run dev:agent:simple
```
Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Terminal 2 - Start the UI:**
```bash
npm run dev:ui
```
Should see:
```
✓ Ready in 1.2s
```

Then open http://localhost:3000

## Method 3: Use GiftScout Agent

Instead of the simple agent, you can use the full GiftScout agent:

```bash
npm run dev
```

Or separately:
```bash
# Terminal 1
npm run dev:agent

# Terminal 2
npm run dev:ui
```

## Troubleshooting

### Error: "Address already in use"
Port 8000 or 3000 is in use. Kill the processes:
```bash
npm run kill:ports
```

### Error: "Ensure Pydantic AI agent is running"
The API route can't reach the agent. Check:
1. Agent is running on http://localhost:8000
2. `PYDANTIC_AI_URL` in `.env.local` is correct
3. No firewall blocking localhost connections

### Error: "No response from agent"
Check agent logs for errors. The agent should log all requests:
```
INFO:     127.0.0.1:12345 - "POST / HTTP/1.1" 200 OK
```

### GraphQL Error Still Appearing
This should be fixed now, but if you see it:
1. Clear browser cache (Cmd+Shift+Del / Ctrl+Shift+Del)
2. Restart both agent and UI
3. Check `.env.local` has correct API keys

## Message Flow

```
Your Message
    ↓
Browser sends to /api/copilotkit
    ↓
Next.js route.ts proxies to http://localhost:8000/
    ↓
Pydantic AI agent processes
    ↓
Returns response
    ↓
Displayed in chat
```

## Available Agents

| Command | Agent | Purpose |
|---------|-------|---------|
| `npm run dev:agent:simple` | Simple Request | Basic Q&A with message history |
| `npm run dev:agent` | GiftScout | Gift discovery with web search |
| `npm run dev` | GiftScout + UI | Full application |
| `npm run dev:simple` | Simple Agent + UI | Simple chat application |

## Testing Queries

### Simple Agent
- "Hello!"
- "What's your name?"
- "Tell me a joke"
- "Help me find a gift"

### GiftScout Agent
- "Find me a gift for a 25-year-old gamer with a $100 budget"
- "What's trending for teenagers on TikTok?"
- "Search for DIY gift ideas under $50"

## Logs to Watch

### Agent Logs
```
INFO:agent:Redis connection established
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### UI Logs (in browser console)
Should show successful fetch to `/api/copilotkit`

### API Route Logs (browser console or Next.js terminal)
```
[CopilotKit POST] Incoming request
[CopilotKit POST] Response from agent received
```
