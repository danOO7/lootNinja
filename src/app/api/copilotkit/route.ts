import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
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

// Initialize service adapter
const serviceAdapter = new ExperimentalEmptyAdapter();
 
// Create the CopilotRuntime with LangGraph integration
const runtime = new CopilotRuntime({
  agents: {
    // GiftScout agent configuration
    "giftscount_agent": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
      graphId: "giftscount_agent",
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
    // Fallback to sample agent for compatibility
    "sample_agent": new LangGraphAgent({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
      graphId: "giftscount_agent", // Use GiftScout agent
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
  }
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