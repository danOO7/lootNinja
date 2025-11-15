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
      description: "A simple request agent for finding trending gifts on TikTok",
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
          // Direct response generation instead of calling external agent
          // Generate gift recommendations based on user message
          
          const giftData = {
            "tech": {
              items: [
                { name: "AirPods Pro Max", link: "https://www.apple.com/airpods-pro/", price: "$549" },
                { name: "Phone cooling fans", link: "https://www.amazon.com/s?k=phone+cooling+fan", price: "$15-30" },
                { name: "Portable phone chargers", link: "https://www.amazon.com/s?k=portable+phone+charger", price: "$20-50" },
                { name: "Smart home devices", link: "https://www.amazon.com/s?k=smart+home+devices", price: "$50-200" },
              ]
            },
            "aesthetic": {
              items: [
                { name: "Ring lights with stands", link: "https://www.amazon.com/s?k=ring+light+with+stand", price: "$20-60" },
                { name: "Neon signs", link: "https://www.amazon.com/s?k=neon+signs", price: "$30-80" },
                { name: "Fairy lights", link: "https://www.amazon.com/s?k=fairy+lights", price: "$10-25" },
                { name: "Plants and plant pots", link: "https://www.amazon.com/s?k=plants+plant+pots", price: "$10-40" },
              ]
            },
            "funny": {
              items: [
                { name: "Meme t-shirts and hoodies", link: "https://www.amazon.com/s?k=funny+meme+shirts", price: "$15-40" },
                { name: "Funny socks with jokes", link: "https://www.amazon.com/s?k=funny+novelty+socks", price: "$10-25" },
                { name: "Novelty mugs", link: "https://www.amazon.com/s?k=funny+novelty+mugs", price: "$12-25" },
                { name: "Hilarious card games", link: "https://www.amazon.com/s?k=funny+card+games", price: "$20-35" },
              ]
            },
            "default": {
              items: [
                { name: "Pop It fidget toys", link: "https://www.amazon.com/s?k=pop+it+fidget+toys", price: "$5-20" },
                { name: "Funny socks and slippers", link: "https://www.amazon.com/s?k=funny+socks", price: "$10-30" },
                { name: "Phone tripods and ring lights", link: "https://www.amazon.com/s?k=phone+tripod+ring+light", price: "$15-50" },
                { name: "Bluetooth speakers", link: "https://www.amazon.com/s?k=bluetooth+speakers", price: "$20-100" },
                { name: "LED strip lights", link: "https://www.amazon.com/s?k=led+strip+lights", price: "$10-40" },
              ]
            }
          };
          
          const messageLower = message.toLowerCase();
          let category = "default";
          
          if (messageLower.includes("tech") || messageLower.includes("gadget") || messageLower.includes("device")) {
            category = "tech";
          } else if (messageLower.includes("aesthetic") || messageLower.includes("decor") || messageLower.includes("room")) {
            category = "aesthetic";
          } else if (messageLower.includes("funny") || messageLower.includes("laugh") || messageLower.includes("joke")) {
            category = "funny";
          }
          
          const items = giftData[category as keyof typeof giftData].items;
          
          let responseText = "🎁 **Trending Gifts on TikTok:**\n\n";
          items.forEach((item) => {
            responseText += `**${item.name}**\n`;
            responseText += `💰 Price: ${item.price}\n`;
            responseText += `🛒 [Buy Now on Amazon](${item.link})\n\n`;
          });
          
          console.log("[simple_agent] Response:", responseText);
          return responseText;
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