"use client";

import React, { useState, useRef, useEffect } from "react";
import { CopilotChat } from "@copilotkit/react-ui";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  return (
    // <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      {/* <div className="bg-white border-b border-gray-200 shadow-sm"> */}
      <div className="bg-white">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-gray-900"></h1>
          <p className="text-sm text-gray-600 mt-1">
          </p>
        </div>
      </div>

      {/* Main Content */}
      {/* <div className="flex-1 overflow-auto flex flex-col justify-start items-center p-6 bg-gray-100"> */}
      <div className="flex-1 overflow-auto flex flex-col justify-start items-center p-6">
        <div className="w-full max-w-2xl">
          {/* Logo and Banner Section */}
          <div className="text-center mb-8 bg-white rounded-lg p-8 shadow-sm">
            <img 
              src="/loot-ninja.png" 
              alt="Loot Ninja Logo"
              className="h-48 w-auto mx-auto mb-6"
            />
            {/* <h2 className="text-2xl font-bold text-gray-900 mb-2"></h2>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8"> */}
              {/* <div className="bg-blue-50 rounded-lg p-4">
                <div className="text-3xl mb-2">🎬</div>
                <h3 className="font-semibold text-gray-900">TikTok Trends</h3>
                <p className="text-sm text-gray-600 mt-1">Finds what's trending right now</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-semibold text-gray-900">Perfect Matches</h3>
                <p className="text-sm text-gray-600 mt-1">Personalized gift recommendations</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="text-3xl mb-2">💰</div>
                <h3 className="font-semibold text-gray-900">Budget Friendly</h3>
                <p className="text-sm text-gray-600 mt-1">Gifts for any price range</p>
              </div> */}

            {/* </div> */}
            <CopilotChat
              instructions="You are Loot Ninja, an expert gift finder specializing in discovering trending gifts on TikTok. Always start by asking the user: 'Who are you buying the gift for?' to understand their needs. Then ask follow-up questions about age, interests, personality, and budget. Once you understand their needs, recommend viral gift ideas with shopping links. Be friendly, engaging, and provide specific product suggestions when possible."
              labels={{
                title: "Loot Ninja Chat",
                placeholder: "Tell me who you're buying for...",
              }}
            />
          </div>

          {/* Chat Section */}
          {/* <div className="bg-white rounded-lg shadow-sm overflow-hidden" style={{ height: "500px" }}>
          </div> */}
        </div>
      </div>
    </div>
  );
}
