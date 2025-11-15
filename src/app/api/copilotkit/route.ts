import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const serviceAdapter = new OpenAIAdapter({
  model: "gpt-4o",
});

const runtime = new CopilotRuntime({
  actions: [
    {
      name: "simple_agent",
      description: "A simple request agent for handling user queries",
      parameters: [
        {
          name: "message",
          type: "string",
          description: "The user's message or request",
          required: true,
        },
      ],
      handler: async ({ message }) => {
        console.log("[simple_agent] Processing:", message);
        try {
          const response = await fetch("http://localhost:8000/run", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              input: {
                user_request: message,
              },
            }),
          });
          
          if (!response.ok) {
            throw new Error(`Agent response: ${response.status}`);
          }
          
          const result = await response.json();
          console.log("[simple_agent] Response:", result);
          return result.response || JSON.stringify(result);
        } catch (error) {
          console.error("[simple_agent] Error:", error);
          throw error;
        }
      },
    },
  ],
});

export const POST = async (req: NextRequest) => {
  try {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter,
      endpoint: "/api/copilotkit",
    });

    const response = await handleRequest(req);

    return response;
  } catch (error) {
    console.error("[CopilotKit POST] Error:", error);
    const errorMessage = error instanceof Error ? error.message : String(error);

    return new Response(
      JSON.stringify({
        error: "Failed to process CopilotKit request",
        message: errorMessage,
        hint: "Ensure OpenAI API key is set and request is properly formatted",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
};