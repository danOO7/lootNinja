# Production Deployment Configuration

## Frontend Changes for Production

When you deploy LangGraph to production, update your frontend configuration:

### Option 1: Environment Variables

Create `.env.production` in the root:

```env
# Production LangGraph deployment URL
NEXT_PUBLIC_LANGGRAPH_URL=https://your-deployment-id.api.smith.langchain.com
NEXT_PUBLIC_API_URL=https://your-frontend-domain.com/api
```

### Option 2: Update Code

In `src/app/api/copilotkit/route.ts`, add:

```typescript
const deploymentUrl = process.env.NODE_ENV === 'production'
  ? process.env.LANGGRAPH_DEPLOYMENT_URL || 'https://your-deployment-id.api.smith.langchain.com'
  : 'http://localhost:8123';
```

### Option 3: Dynamic Configuration

Create a config file: `src/config/deployment.ts`

```typescript
export const getDeploymentConfig = () => {
  const isProduction = process.env.NODE_ENV === 'production';
  
  return {
    langgraphUrl: isProduction
      ? process.env.LANGGRAPH_DEPLOYMENT_URL
      : 'http://localhost:8123',
    apiUrl: isProduction
      ? process.env.NEXT_PUBLIC_API_URL
      : 'http://localhost:3000/api',
    environment: process.env.NODE_ENV,
  };
};
```

Then use in `route.ts`:

```typescript
import { getDeploymentConfig } from '@/config/deployment';

const config = getDeploymentConfig();
const deploymentUrl = config.langgraphUrl || 'http://localhost:8123';
```

## Deployment Steps

### Step 1: Deploy LangGraph to LangSmith

```bash
cd agent
langgraph deploy
# Note the deployment URL provided
```

### Step 2: Get Your Deployment URL

From LangSmith dashboard:
```
https://your-deployment-id.api.smith.langchain.com
```

### Step 3: Update Environment Variables

In your hosting platform (Vercel, Netlify, etc.):

```
LANGGRAPH_DEPLOYMENT_URL=https://your-deployment-id.api.smith.langchain.com
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### Step 4: Deploy Frontend

```bash
# Vercel
vercel deploy --prod

# Netlify
netlify deploy --prod

# Custom server
git push heroku main
```

## Verify Production Setup

1. **Test Agent Endpoint**:
   ```bash
   curl https://your-deployment-id.api.smith.langchain.com/docs
   ```

2. **Test Frontend API**:
   ```bash
   curl https://your-frontend-url.com/api/copilotkit
   ```

3. **End-to-End Test**:
   - Open frontend
   - Open CopilotKit sidebar
   - Send a message
   - Check LangSmith traces

## Monitoring Production

### LangSmith Dashboard
- View all agent runs
- Analyze traces
- Monitor performance
- Set up alerts

### Application Monitoring
- Use Sentry for error tracking
- Monitor API response times
- Track user sessions
- Set up uptime monitoring

### Logs
- LangSmith logs: Built-in traces
- Frontend logs: Application dashboard
- API logs: Cloud provider logs

## Troubleshooting

### "Agent unreachable"
- Verify deployment URL is correct
- Check LangSmith deployment status
- Ensure environment variables are set
- Test endpoint directly

### "Timeout"
- Increase timeout in CopilotKit config
- Check LangGraph worker count
- Monitor Redis connection
- Check API rate limits

### "CORS errors"
- Verify deployment allows CORS
- Check frontend domain in CORS settings
- Test from different origins

## Cost Optimization Tips

1. **Caching**: Reduce API calls with Redis
2. **Batching**: Process multiple requests together
3. **Pruning**: Remove unused dependencies
4. **Monitoring**: Track and optimize expensive operations
5. **Rate Limiting**: Prevent abuse

## Rollback Procedure

If something goes wrong:

```bash
# View deployment history
langgraph deployments list

# Rollback to previous version
langgraph deployment rollback <deployment-id> <version-id>

# Or redeploy from git
cd agent
langgraph deploy
```

## Support & Resources

- LangSmith Docs: https://docs.smith.langchain.com/deployment
- LangGraph CLI: https://docs.langchain.com/langgraph/deploy/cli
- Architecture Guide: See ARCHITECTURE_DIAGRAMS.md
- Setup Guide: See COPILOTKIT_SETUP.md
