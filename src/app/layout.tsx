import type { Metadata } from "next";

import { CopilotKit } from "@copilotkit/react-core";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

export const metadata: Metadata = {
  title: "Simple Agent - AI Assistant",
  description: "AI-powered simple agent for answering queries",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <CopilotKit 
          runtimeUrl="/api/copilotkit"
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
