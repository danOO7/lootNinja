# Simple Request Agent

## Overview
A lightweight, flexible request agent built with Pydantic AI for handling general user requests and questions. This agent is simpler than the GiftScout agent and serves as a clean starting point for agent development.

## Features

✅ **Conversation Management** - Maintains message history
✅ **Simple Tools** - Add messages, retrieve history, set responses
✅ **Fast & Lightweight** - Minimal dependencies
✅ **Easy to Extend** - Clean architecture for adding new tools

## File Structure

- **`agent/src/simple_agent.py`** - Agent definition with tools
- **`agent/src/main_simple.py`** - Server entry point
- **`run-agent-simple.sh`** - Shell script to run the agent

## State Model

### RequestState
```python
{
    "user_request": str,      # User's current request
    "messages": [              # Conversation history
        {"role": str, "content": str}
    ],
    "response": str           # Agent's current response
}
```

## Available Tools

### 1. `add_message(role, content)`
Add a message to the conversation history.

**Parameters:**
- `role`: 'user' or 'assistant'
- `content`: Message text

**Returns:** Updated state snapshot

### 2. `get_messages()`
Retrieve the conversation history.

**Returns:** List of messages with role and content

### 3. `set_response(response)`
Set the agent's response to the user request.

**Parameters:**
- `response`: Response text

**Returns:** Updated state snapshot

### 4. `get_response()`
Get the current response.

**Returns:** Response text

## Running the Agent

### Option 1: Simple Agent Only
```bash
npm run dev:agent:simple
```

### Option 2: UI + Simple Agent
```bash
npm run dev:simple
```

### Option 3: GiftScout Agent (Original)
```bash
npm run dev:agent
# or
npm run dev
```

## How It Works

1. **User sends message** → Stored in state via `add_message()`
2. **Agent processes** → Uses tools to access/modify state
3. **Agent responds** → Sets response via `set_response()`
4. **Conversation continues** → New messages added to history

## Extending the Agent

To add a new tool, simply add a function decorated with `@agent.tool`:

```python
@agent.tool
def my_new_tool(ctx: RunContext[StateDeps[RequestState]], param: str) -> str:
    """Tool description."""
    # Do something
    return result
```

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key for GPT-4 Mini model

Optional:
- `REDIS_HOST` - Redis host (default: localhost)
- `REDIS_PORT` - Redis port (default: 6379)
- `LOG_LEVEL` - Logging level

## Switching Between Agents

| Command | Agent | UI |
|---------|-------|-----|
| `npm run dev` | GiftScout | Yes |
| `npm run dev:simple` | Simple Request | Yes |
| `npm run dev:agent` | GiftScout | No |
| `npm run dev:agent:simple` | Simple Request | No |

## API Endpoint

When running, the agent is available at:
```
http://0.0.0.0:8000
```

Access the web UI at:
```
http://localhost:3000
```
