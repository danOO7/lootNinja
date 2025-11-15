"use client";

import React, { useEffect, useState } from "react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  return (
    <CopilotKit publicApiKey="ck_pub_2f3c4528d076fade691d644551bac4d3" runtimeUrl="/api/copilotkit">
      <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <main className="flex-1 overflow-auto">
          <div className="max-w-6xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                🎁 GiftScout
              </h1>
              <p className="text-lg text-gray-600">
                AI-powered gift finder that searches social trends and live products
              </p>
            </div>

            {/* Main Content Card */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
              <div className="grid md:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">
                    Find the Perfect Gift
                  </h2>
                  <p className="text-gray-600 mb-4">
                    Tell GiftScout about the person, your budget, and what they like.
                    The agent will search social media trends and find real products.
                  </p>

                  <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                    <h3 className="font-semibold text-blue-900 mb-2">
                      💡 How it works:
                    </h3>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>✓ Searches Reddit, TikTok, and trending blogs</li>
                      <li>✓ Finds actual products with prices and links</li>
                      <li>✓ Filters by your budget</li>
                      <li>✓ Returns shoppable recommendations</li>
                    </ul>
                  </div>

                  <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded mt-4">
                    <p className="text-sm text-green-800">
                      <strong>Pro Tip:</strong> You can ask GiftScout directly in the sidebar!
                      Example: "Find a gaming gift under $50 for a teenager"
                    </p>
                  </div>
                </div>

                {/* Features Section */}
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-gray-800">Features</h3>

                  <div className="space-y-3">
                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded">
                      <h4 className="font-semibold text-gray-800">
                        🌐 Live Web Search
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Real-time searches using Tavily for current products and trends
                      </p>
                    </div>

                    <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-4 rounded">
                      <h4 className="font-semibold text-gray-800">
                        💾 Smart Caching
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Redis-powered session storage for fast recommendations
                      </p>
                    </div>

                    <div className="bg-gradient-to-r from-orange-50 to-red-50 p-4 rounded">
                      <h4 className="font-semibold text-gray-800">
                        🤖 AI-Powered
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        GPT-4o analyzes trends and curates personalized suggestions
                      </p>
                    </div>

                    <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded">
                      <h4 className="font-semibold text-gray-800">
                        📱 Social Aware
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        Analyzes what's trending on TikTok, Reddit, and YouTube
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Recommendations */}
            {recommendations.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  Recommended Gifts
                </h2>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendations.map((rec, idx) => (
                    <a
                      key={idx}
                      href={rec.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-lg p-4 hover:shadow-md transition-shadow border border-blue-200"
                    >
                      <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">
                        {rec.title}
                      </h3>
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                        {rec.snippet}
                      </p>
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-indigo-600 font-medium">
                          {rec.source}
                        </span>
                        <span className="text-xs bg-indigo-200 text-indigo-800 px-2 py-1 rounded">
                          View
                        </span>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Stack Info */}
            <div className="mt-8 bg-gray-800 text-white rounded-lg p-6">
              <h3 className="text-lg font-bold mb-3">🛠 Tech Stack</h3>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                  <strong className="text-blue-400">Tavily</strong>
                  <p className="text-gray-300">Live web search for products & trends</p>
                </div>
                <div>
                  <strong className="text-red-400">Redis</strong>
                  <p className="text-gray-300">State management & session caching</p>
                </div>
                <div>
                  <strong className="text-green-400">CopilotKit</strong>
                  <p className="text-gray-300">AI orchestration & tool management</p>
                </div>
              </div>
            </div>
          </div>
        </main>

        <CopilotSidebar
          instructions="You are GiftScout, an expert at finding perfect gifts by researching social trends and live products. Help users find gifts by understanding their recipient's persona, budget, and interests. Use your tools to search social media trends, find products, and provide curated recommendations with direct shopping links."
          defaultOpen={true}
        />
      </div>
    </CopilotKit>
  );
}
