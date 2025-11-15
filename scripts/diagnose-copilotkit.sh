#!/bin/bash
# Quick diagnostic script to check CopilotKit setup

echo "🔍 GiftScout Setup Diagnostic"
echo "================================"

# Check environment variables
echo ""
echo "✓ Checking environment variables..."
if [ -f ".env.local" ]; then
    echo "  ✓ .env.local found"
    if grep -q "GOOGLE_API_KEY" .env.local; then
        echo "  ✓ GOOGLE_API_KEY is set"
    else
        echo "  ✗ GOOGLE_API_KEY is missing"
    fi
    
    if grep -q "TAVILY_API_KEY" .env.local; then
        echo "  ✓ TAVILY_API_KEY is set"
    else
        echo "  ✗ TAVILY_API_KEY is missing"
    fi
    
    if grep -q "REDIS_URL" .env.local; then
        echo "  ✓ REDIS_URL is set"
    else
        echo "  ✗ REDIS_URL is missing"
    fi
else
    echo "  ✗ .env.local not found - create it first!"
    exit 1
fi

# Check if Redis is running
echo ""
echo "✓ Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "  ✓ Redis is running"
else
    echo "  ✗ Redis is not running on localhost:6379"
    echo "    Start it with: docker run -d -p 6379:6379 redis:latest"
fi

# Check Node version
echo ""
echo "✓ Checking Node.js..."
node_version=$(node --version)
echo "  ✓ Node.js $node_version"

# Summary
echo ""
echo "================================"
echo "✓ Diagnostic Complete!"
echo ""
echo "Next steps:"
echo "1. Ensure Redis is running"
echo "2. Run: npm run dev"
echo "3. Open http://localhost:3000"
echo "4. Type a message in the sidebar"
echo ""
echo "If you still get GraphQL errors, check the browser console and server logs."
