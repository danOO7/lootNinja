# GiftScout Agent - Fetch Failed Troubleshooting Guide

## Problem
```
Agent 'giftscount_agent' configuration issue: fetch failed
User configuration error: Agent 'giftscount_agent' failed to execute: fetch failed
```

## Root Causes

### 1. **LangGraph Agent Server Not Running**
The most common cause. The Next.js API route tries to reach the agent at `http://localhost:8123` but it's not running.

**Solution:**
```bash
# Start the agent server
npm run dev:agent

# Or with Docker
docker-compose up langgraph
```

**Verify:** Visit `http://localhost:8123/docs` in your browser. You should see the LangGraph API documentation.

---

### 2. **Missing LANGGRAPH_DEPLOYMENT_URL Environment Variable**
The `.env` file may not have the deployment URL configured.

**Solution:**
```bash
# Add to .env
export LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123
```

**Verify:** 
```bash
echo $LANGGRAPH_DEPLOYMENT_URL
# Should output: http://localhost:8123
```

---

### 3. **Redis Connection Failed**
The agent needs Redis for state management. Redis may not be running.

**Solution:**
```bash
# Start Redis locally
redis-server

# Or with Docker
docker-compose up redis
```

**Verify:**
```bash
redis-cli ping
# Should output: PONG
```

---

### 4. **Missing API Keys**
The agent requires API keys for Tavily and Google Gemini.

**Solution:**
Ensure these are set in `.env`:
```bash
export TAVILY_API_KEY=tvly-dev-...
export GOOGLE_API_KEY=AIzaSy...
export LANGSMITH_API_KEY=lsv2_pt_...
```

**Verify:**
```bash
echo $TAVILY_API_KEY
echo $GOOGLE_API_KEY
echo $LANGSMITH_API_KEY
```

---

## Diagnostic Steps

### Run the diagnostic script
```bash
bash scripts/diagnose.sh
```

This will check:
- ✓ Environment variables
- ✓ Redis connection
- ✓ LangGraph agent server
- ✓ Next.js dev server
- ✓ Docker containers

---

## Complete Setup

### Option 1: Development Mode (Local Services)
```bash
# Terminal 1: Start the agent
npm run dev:agent

# Terminal 2: Start the UI
npm run dev:ui

# Terminal 3: Start Redis (if not already running)
redis-server
```

### Option 2: Development Mode (Concurrently)
```bash
npm run dev
```

This automatically starts both the agent and UI in one command.

### Option 3: Docker (Recommended for Production-like Testing)
```bash
docker-compose up
```

This starts:
- LangGraph agent on `8123`
- Redis on `6379`
- Next.js app on `3000` (if built with Docker)

---

## Network Issues Checklist

### If using Docker
- Ensure services can reach each other by name:
  - Agent: `http://langgraph:8123` (from other Docker services)
  - Redis: `redis:6379` (from other Docker services)
  
### If using localhost
- Ensure all services are on the same machine
- Check firewall isn't blocking ports 3000, 8123, 6379

### If using remote deployment
- Update `LANGGRAPH_DEPLOYMENT_URL` to your production URL
- Example: `https://your-deployment-id.api.smith.langchain.com`

---

## Monitoring Logs

### Agent Server Logs
```bash
# Shows real-time logs from the agent
npm run dev:agent
```

### Next.js Logs
```bash
# Shows real-time logs from the UI
npm run dev:ui
```

### Docker Logs
```bash
# View all container logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f langgraph
docker-compose logs -f redis
```

---

## Quick Fix Checklist

- [ ] Redis is running (`redis-cli ping` returns `PONG`)
- [ ] Agent server is running (visiting `http://localhost:8123/docs` works)
- [ ] `.env` has `LANGGRAPH_DEPLOYMENT_URL=http://localhost:8123`
- [ ] All API keys are set in `.env`
- [ ] Next.js dev server is running on `http://localhost:3000`
- [ ] No firewall blocking ports 3000, 8123, 6379

---

## Still Having Issues?

1. **Check error messages in console logs**
   ```bash
   npm run dev:agent 2>&1 | tee agent.log
   npm run dev:ui 2>&1 | tee ui.log
   ```

2. **Test the agent endpoint directly**
   ```bash
   curl http://localhost:8123/docs
   # Should return HTML with API documentation
   ```

3. **Verify Redis connection**
   ```bash
   redis-cli
   > PING
   # Should output: PONG
   ```

4. **Check environment variables are loaded**
   ```bash
   source .env
   echo $LANGGRAPH_DEPLOYMENT_URL
   ```

5. **Rebuild containers if using Docker**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```
