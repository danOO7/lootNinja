import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  GoogleGenerativeAIAdapter,
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

// Get deployment URL with fallback
const deploymentUrl = process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123";
console.log(`[CopilotKit] Connecting to LangGraph at: ${deploymentUrl}`);

// Create the Google Gemini adapter for fallback LLM calls
const serviceAdapter = new GoogleGenerativeAIAdapter({
  model: "gemini-2.5-pro",
});

// Create the CopilotRuntime with LangGraph integration
const runtime = new CopilotRuntime({
  agents: {
    // GiftScout agent - primary gift discovery agent
    "giftscount_agent": new LangGraphAgent({
      deploymentUrl: deploymentUrl,
      graphId: "giftscount_agent",
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
    }),
  },
});
 
/**
 * Handle POST requests to the CopilotKit runtime endpoint.
 * Processes messages, tool calls, and agent state management.
 */
export const POST = async (req: NextRequest) => {
  try {
    console.log("[CopilotKit POST] Incoming request");

    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: "/api/copilotkit",
    });
 
    const response = await handleRequest(req);
    console.log("[CopilotKit POST] Response status:", response.status);
    return response;
  } catch (error) {
    console.error("[CopilotKit] Error in POST handler:", error);
    const errorMessage = error instanceof Error ? error.message : String(error);
    const errorStack = error instanceof Error ? error.stack : "";
    
    console.error("[CopilotKit] Full error:", {
      message: errorMessage,
      stack: errorStack,
    });
    
    return new Response(
      JSON.stringify({
        error: "Failed to process request",
        message: errorMessage,
        stack: process.env.NODE_ENV === "development" ? errorStack : undefined,
        hint: `Ensure LangGraph agent is running at ${deploymentUrl}`,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
};

/**
 * Handle GET requests to the CopilotKit runtime endpoint.
 * Required for agent state retrieval and status checks.
 */
export const GET = async (req: NextRequest) => {
  try {
    console.log("[CopilotKit GET] Incoming request");

    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: "/api/copilotkit",
    });
 
    return handleRequest(req);
  } catch (error) {
    console.error("[CopilotKit] Error in GET handler:", error);
    const errorMessage = error instanceof Error ? error.message : String(error);
    const errorStack = error instanceof Error ? error.stack : "";
    
    return new Response(
      JSON.stringify({
        error: "Failed to process request",
        message: errorMessage,
        stack: process.env.NODE_ENV === "development" ? errorStack : undefined,
        hint: `Ensure LangGraph agent is running at ${deploymentUrl}`,
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
};