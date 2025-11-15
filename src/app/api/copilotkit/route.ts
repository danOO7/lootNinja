import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  OpenAIAdapter,
} from "@copilotkit/runtime";

import { LangGraphAgent } from "@ag-ui/langgraph"
import { NextRequest } from "next/server";
 
/**
 * GiftScout CopilotKit Runtime Configuration
 * 
 * This endpoint orchestrates the AI agent that:
 * 1. Searches social trends using Tavily API
 * 2. Finds products with pricing and links
 * 3. Caches results in Redis for performance
 * 4. Returns curated gift recommendations
 */

// Create the OpenAI adapter for LLM calls (uses OPENAI_API_KEY)
const serviceAdapter = new OpenAIAdapter({
  model: "gpt-4o", // Uses GPT-4o for best gift discovery reasoning
});
 
// Create the CopilotRuntime with LangGraph integration
const runtime = new CopilotRuntime({
  agents: {
    // GiftScout agent - primary gift discovery agent
    "giftscount_agent": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
      graphId: "giftscount_agent",
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
    // Sample agent - fallback for compatibility
    "sample_agent": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
      graphId: "giftscount_agent", // Also uses GiftScout agent
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
  },
});
 
/**
 * Handle POST requests to the CopilotKit runtime endpoint.
 * Processes messages, tool calls, and agent state management.
 */
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });
 
  return handleRequest(req);
};