# LangGraph LangSmith Deployment Configuration

This file contains instructions for deploying GiftScout to LangSmith.

## Prerequisites

1. **LangSmith Account**: Sign up at https://smith.langchain.com
2. **API Key**: Get your LangSmith API key from https://smith.langchain.com/settings/api-keys
3. **GitHub Account**: For connecting your repository (optional)

## Deployment Methods

### Method 1: Using `langgraph` CLI (Recommended)

```bash
# Install langgraph CLI
pip install langgraph-cli

# Login to LangSmith
langgraph auth set

# Deploy from the agent directory
cd agent
langgraph deploy

# Follow the prompts to select deployment options
```

### Method 2: Using LangSmith Web UI

1. Go to https://smith.langchain.com/deployments
2. Click "Create Deployment"
3. Connect your GitHub repository or upload files directly
4. Select Python 3.12
5. Set working directory to `/agent`
6. Configure environment variables
7. Deploy

### Method 3: Docker Deployment

```bash
# Build the image
docker build -t giftscount-agent .

# Run locally with docker-compose
docker-compose up

# Deploy to cloud (AWS, GCP, Azure, etc.)
docker push your-registry/giftscount-agent:latest
```

## Environment Variables

Set these in your LangSmith deployment:

```
OPENAI_API_KEY=sk_...
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=tvly-...
LANGSMITH_API_KEY=ls_...
REDIS_URL=redis://your-redis-host:6379
```

## Configuration Files

- `langgraph.json`: Defines graphs and Python version
- `requirements.txt`: Python dependencies
- `agent.py`: Main agent implementation
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Local development setup

## Verifying Deployment

After deployment, test your agent:

```bash
# Get your deployment URL from LangSmith
# Usually: https://your-deployment-id.api.smith.langchain.com

curl -X POST https://your-deployment-id.api.smith.langchain.com/runs \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "giftscount_agent",
    "input": {"messages": [{"role": "user", "content": "Find a gaming gift under $50"}]}
  }'
```

## Scaling & Monitoring

1. **Monitor**: LangSmith provides built-in monitoring dashboard
2. **Scale**: Adjust worker count in deployment settings
3. **Logs**: View real-time logs in LangSmith UI
4. **Traces**: Analyze execution traces for debugging

## Production Checklist

- ✅ Python version: 3.12
- ✅ Dependencies locked in requirements.txt
- ✅ Environment variables configured
- ✅ Health checks enabled
- ✅ Error handling implemented
- ✅ Logging configured
- ✅ Rate limiting (optional)
- ✅ Authentication/authorization (optional)

## Rollback

If deployment fails:

```bash
# View deployment history
langgraph deployments list

# Rollback to previous version
langgraph deployment rollback <deployment-id> <version-id>
```

## Cost Optimization

- Monitor API usage (Tavily, OpenAI/Google, LangSmith)
- Implement caching with Redis
- Use batch processing for multiple requests
- Monitor vector DB costs (if applicable)

## Support

- LangSmith Docs: https://docs.smith.langchain.com
- GitHub Issues: https://github.com/langchain-ai/langgraph/issues
- Community: https://discord.gg/6adMJt42V5
