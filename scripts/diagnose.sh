#!/bin/bash

# Diagnostic script for troubleshooting giftscount_agent fetch issues

echo "================================"
echo "GiftScout Agent Diagnostics"
echo "================================"
echo ""

# Check environment variables
echo "1. Checking environment variables..."
echo "   LANGGRAPH_DEPLOYMENT_URL: ${LANGGRAPH_DEPLOYMENT_URL:-NOT SET}"
echo "   REDIS_URL: ${REDIS_URL:-NOT SET}"
echo "   GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:20}..."
echo "   TAVILY_API_KEY: ${TAVILY_API_KEY:0:20}..."
echo "   LANGSMITH_API_KEY: ${LANGSMITH_API_KEY:0:20}..."
echo ""

# Check if Redis is running
echo "2. Checking Redis connection..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "   ✓ Redis is running"
    else
        echo "   ✗ Redis is NOT running"
        echo "     Start it with: redis-server"
    fi
else
    echo "   ⚠ redis-cli not found, cannot test Redis"
fi
echo ""

# Check if LangGraph agent is running
echo "3. Checking LangGraph agent server..."
DEPLOYMENT_URL="${LANGGRAPH_DEPLOYMENT_URL:-http://localhost:8123}"
if curl -s "$DEPLOYMENT_URL/docs" > /dev/null 2>&1; then
    echo "   ✓ LangGraph agent is running at $DEPLOYMENT_URL"
else
    echo "   ✗ LangGraph agent is NOT running at $DEPLOYMENT_URL"
    echo "     Start it with: npm run dev:agent"
fi
echo ""

# Check if Next.js dev server is running
echo "4. Checking Next.js dev server..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "   ✓ Next.js dev server is running"
else
    echo "   ✗ Next.js dev server is NOT running"
    echo "     Start it with: npm run dev:ui"
fi
echo ""

# Check if Docker containers are running
echo "5. Checking Docker containers..."
if command -v docker &> /dev/null; then
    RUNNING_CONTAINERS=$(docker ps --filter "name=langgraph\|redis" --format "{{.Names}}" 2>/dev/null | wc -l)
    if [ "$RUNNING_CONTAINERS" -gt 0 ]; then
        echo "   ✓ Docker containers found:"
        docker ps --filter "name=langgraph\|redis" --format "  - {{.Names}} ({{.Status}})" 2>/dev/null
    else
        echo "   - No Docker containers found (using local services)"
    fi
else
    echo "   - Docker not available (using local services)"
fi
echo ""

# Summary
echo "================================"
echo "Summary:"
echo "================================"
echo "To run the complete stack:"
echo "  1. Start all services: npm run dev"
echo "  2. Or start individually:"
echo "     - Agent: npm run dev:agent"
echo "     - UI: npm run dev:ui"
echo ""
echo "To use Docker:"
echo "  docker-compose up -d"
echo ""
