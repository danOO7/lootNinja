# Quick LangGraph Deployment Guide

## 1. Deploy with Docker Compose (Local/Server)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f langgraph

# Access at http://localhost:8123
```

## 2. Deploy to LangSmith (Recommended)

```bash
# 1. Install CLI
pip install langgraph-cli

# 2. Authenticate
langgraph auth set
# Paste your API key from https://smith.langchain.com/settings/api-keys

# 3. Deploy
cd /home/dbu/ai-hackaton/lootNinja/agent
langgraph deploy

# 4. Follow prompts to:
#    - Select deployment name (e.g., "giftscount-prod")
#    - Choose Python 3.12
#    - Set environment variables
#    - Review and confirm
```

## 3. Deploy to Cloud Platforms

### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag giftscount-agent 123456789.dkr.ecr.us-east-1.amazonaws.com/giftscount-agent:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/giftscount-agent:latest

# Create ECS task definition and service
# (Use AWS Console or CloudFormation)
```

### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/giftscount-agent

# Deploy
gcloud run deploy giftscount-agent \
  --image gcr.io/PROJECT_ID/giftscount-agent:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=YOUR_KEY,TAVILY_API_KEY=YOUR_KEY
```

### Heroku (if supported)
```bash
# Login
heroku login

# Create app
heroku create giftscount-agent

# Deploy
git push heroku main

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key
```

## Environment Setup

Create `.env.production` with:
```
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
REDIS_URL=redis://your-redis-host:6379
```

## Verify Deployment

```bash
# Check health
curl https://your-deployment-url/docs

# Test agent
curl -X POST https://your-deployment-url/runs \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "giftscount_agent",
    "input": {"messages": [{"role": "user", "content": "test"}]}
  }'
```

## Monitoring

- **LangSmith Dashboard**: https://smith.langchain.com/deployments
- **Docker Logs**: `docker-compose logs -f`
- **Health Endpoint**: `/docs` or `/health`

## Cost Estimates (Monthly)

- **LangSmith Pro**: $99/month
- **Google Gemini API**: $0.075/M input tokens, $0.30/M output tokens
- **Tavily API**: $10-50/month (depending on usage)
- **Redis (AWS ElastiCache)**: $10-30/month
- **Compute (Cloud Run/ECS)**: $0-20/month (pay-as-you-go)

**Total estimated cost**: $120-200/month for small deployments

## Next Steps

1. ✅ Create LangSmith account (if not done)
2. → Get API keys from all providers
3. → Run `langgraph deploy`
4. → Test production endpoint
5. → Update frontend to use production URL
6. → Monitor performance and costs

See `DEPLOYMENT.md` for detailed instructions.
