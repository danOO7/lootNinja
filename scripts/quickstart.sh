#!/bin/bash

# Quick start script for GiftScout development

set -e

echo "🚀 GiftScout Development Setup"
echo "================================"
echo ""

# Check dependencies
echo "1️⃣  Checking dependencies..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi
echo "✅ Node.js: $(node --version)"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed"
    exit 1
fi
echo "✅ npm: $(npm --version)"

echo ""

# Source environment
echo "2️⃣  Loading environment variables..."
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "✅ Environment loaded from .env"
else
    echo "⚠️  .env file not found"
fi
echo ""

# Check critical environment variables
echo "3️⃣  Validating configuration..."
ERRORS=0

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ GOOGLE_API_KEY not set"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ GOOGLE_API_KEY configured"
fi

if [ -z "$TAVILY_API_KEY" ]; then
    echo "❌ TAVILY_API_KEY not set"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ TAVILY_API_KEY configured"
fi

if [ -z "$LANGGRAPH_DEPLOYMENT_URL" ]; then
    echo "⚠️  LANGGRAPH_DEPLOYMENT_URL not set (using default: http://localhost:8123)"
else
    echo "✅ LANGGRAPH_DEPLOYMENT_URL: $LANGGRAPH_DEPLOYMENT_URL"
fi

echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ Configuration incomplete. Please check .env file"
    echo ""
    echo "Required variables:"
    echo "  - GOOGLE_API_KEY"
    echo "  - TAVILY_API_KEY"
    echo "  - LANGSMITH_API_KEY"
    echo ""
    echo "Optional variables:"
    echo "  - LANGGRAPH_DEPLOYMENT_URL (default: http://localhost:8123)"
    exit 1
fi

echo ""

# Install dependencies
echo "4️⃣  Installing dependencies..."
if [ ! -d node_modules ]; then
    npm install
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""

# Check Redis
echo "5️⃣  Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis is not running"
        echo "   Start with: redis-server"
    fi
else
    echo "⚠️  redis-cli not found"
fi

echo ""

# Ready to start
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo ""
echo "Option 1 - Start everything at once:"
echo "  npm run dev"
echo ""
echo "Option 2 - Start services separately (3 terminals):"
echo "  Terminal 1: npm run dev:agent"
echo "  Terminal 2: npm run dev:ui"
echo "  Terminal 3: redis-server"
echo ""
echo "Option 3 - Use Docker:"
echo "  docker-compose up"
echo ""
echo "To diagnose issues:"
echo "  bash scripts/diagnose.sh"
echo ""
