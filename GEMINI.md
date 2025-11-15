# GEMINI.md

This document provides a comprehensive overview of the GiftScout project, its architecture, and development practices to be used as instructional context for future interactions.

## Project Overview

GiftScout is an AI-powered gift finder application. It provides a web interface where users can describe the person they want to buy a gift for, and the AI agent will search for suitable gift ideas.

The project is a starter template for building AI agents using LangGraph and CopilotKit. It consists of two main parts:

1.  **Frontend:** A Next.js application that provides the user interface. It uses the CopilotKit library to create a chat interface that communicates with the backend agent.
2.  **Backend:** A Python-based AI agent built with LangGraph. This agent is responsible for understanding the user's request, searching for information on the web, and providing gift recommendations.

### Technologies

*   **Frontend:**
    *   Next.js (React framework)
    *   TypeScript
    *   Tailwind CSS
    *   CopilotKit (for the AI chat interface)
*   **Backend:**
    *   Python
    *   LangGraph (for building the AI agent)
    *   Tavily (for web searches)
    *   Redis (for session management and caching)
*   **Other:**
    *   Node.js
    *   pnpm/npm/yarn/bun (package managers)
    *   ESLint (for code linting)

### Architecture

The application follows a client-server architecture:

1.  The user interacts with the Next.js frontend in their browser.
2.  The frontend uses the CopilotKit component to send the user's messages to a backend API route (`/api/copilotkit`).
3.  The API route, running on the Next.js server, forwards the request to the LangGraph agent, which is a separate Python process.
4.  The LangGraph agent processes the request, uses tools like Tavily to search the web, and returns a response.
5.  The response is sent back to the frontend and displayed to the user in the chat interface.

## Building and Running

### Prerequisites

*   Node.js 18+
*   Python 3.8+
*   A package manager (pnpm, npm, yarn, or bun)
*   OpenAI API Key
*   Tavily API Key

### Setup

1.  **Install dependencies:**
    ```bash
    pnpm install
    ```
    (or `npm install`, `yarn install`, `bun install`)

2.  **Set up environment variables:**
    Create a `.env` file in the `agent` directory and add your API keys:
    ```
    OPENAI_API_KEY=your-openai-api-key
    TAVILY_API_KEY=your-tavily-api-key
    ```

### Development

To run the application in development mode, which starts both the frontend and the backend agent:

```bash
pnpm dev
```

Other useful development scripts:

*   `pnpm dev:ui`: Starts only the Next.js frontend.
*   `pnpm dev:agent`: Starts only the Python agent.
*   `pnpm lint`: Runs ESLint to check for code quality.

### Production

To build and run the application in production:

1.  **Build the Next.js application:**
    ```bash
    pnpm build
    ```

2.  **Start the production server:**
    ```bash
    pnpm start
    ```
    You will also need to run the agent separately in a production environment.

## Development Conventions

*   **Package Manager:** The project is configured to work with pnpm, npm, yarn, and bun. Lockfiles are ignored to allow developers to use their preferred package manager.
*   **Code Style:** The project uses ESLint for linting. The configuration is in `eslint.config.mjs`.
*   **Frontend:** The frontend is built with React and Next.js. Components are located in the `src` directory. The main page is `src/app/page.tsx`.
*   **Backend:** The backend agent is in the `agent` directory. The main file is `agent/agent.py`. The agent is built using LangGraph and uses tools for web searches and data caching.
*   **API:** The frontend communicates with the backend via the `/api/copilotkit` endpoint, which is handled by the CopilotKit runtime.
