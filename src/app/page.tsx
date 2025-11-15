"use client";

import React, { useState, useRef, useEffect } from "react";
import { CopilotSidebar } from "@copilotkit/react-ui";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <h1 className="text-3xl font-bold text-gray-900">🤖 Simple Agent</h1>
            <p className="text-sm text-gray-600 mt-1">
              AI-powered assistant for answering your questions
            </p>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-auto">
          <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🎁</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome to Simple Agent</h2>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Ask me anything! I'm here to help with your questions and provide thoughtful responses.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
                <div className="bg-white rounded-lg p-4 shadow">
                  <div className="text-3xl mb-2">💬</div>
                  <h3 className="font-semibold text-gray-900">Conversational</h3>
                  <p className="text-sm text-gray-600 mt-1">Natural language understanding</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow">
                  <div className="text-3xl mb-2">🧠</div>
                  <h3 className="font-semibold text-gray-900">Intelligent</h3>
                  <p className="text-sm text-gray-600 mt-1">Powered by advanced AI models</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow">
                  <div className="text-3xl mb-2">⚡</div>
                  <h3 className="font-semibold text-gray-900">Fast</h3>
                  <p className="text-sm text-gray-600 mt-1">Quick and accurate responses</p>
                </div>
              </div>
              <div className="mt-12 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  💡 <strong>Tip:</strong> Use the sidebar on the right to chat with the Simple Agent!
                </p>
              </div>
            </div>

            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>

      {/* CopilotKit Sidebar */}
      <CopilotSidebar 
        instructions="You are a helpful and friendly AI assistant. Your role is to listen carefully to user requests, provide clear and concise responses, ask clarifying questions when needed, and be conversational and engaging. Always aim to be helpful, honest, and direct in your responses."
        defaultOpen={true}
      />
    </div>
  );
}
