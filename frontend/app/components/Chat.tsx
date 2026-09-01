"use client";

import { useState } from "react";

import Message from "./Message";
import Status from "./Status";

type MessageType = {
  role: "user" | "assistant";
  content: string;
  agent?: string;
  category?: string;
  sources?: string[];
};

const SUGGESTIONS = [
  {
    label: "FAQ",
    query: "What is your refund policy?",
  },
  {
    label: "FAQ",
    query: "How do I track my order?",
  },
  {
    label: "FAQ",
    query: "What are your shipping options?",
  },
  {
    label: "Technical",
    query: "My payment failed and I cannot complete my order.",
  },
  {
    label: "Technical",
    query: "The app crashes when I try to upload a PDF.",
  },
  {
    label: "Escalation",
    query: "I have been waiting 3 weeks for my refund and I want to speak to a manager.",
  },
];

export default function Chat() {
  const [query, setQuery] = useState("");

  const [messages, setMessages] =
    useState<MessageType[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  async function sendMessage(text?: string) {
    const userMessage = text || query.trim();
    if (!userMessage) {
      return;
    }

    setQuery("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL
        }/api/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            query: userMessage,
            thread_id: "demo-user",
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Backend request failed."
        );
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          agent: data.agent,
          category: data.category,
          sources: data.sources,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  const showSuggestions =
    messages.length === 0 && !loading;

  return (
    <section className="chat">
      <Status />

      <div className="messages">
        {messages.map(
          (message, index) => (
            <Message
              key={index}
              message={message}
            />
          )
        )}
      </div>

      {showSuggestions && (
        <div className="suggestions">
          <p className="suggestions-label">
            Try a question:
          </p>
          <div className="suggestions-grid">
            {SUGGESTIONS.map(
              (suggestion, index) => (
                <button
                  key={index}
                  className="suggestion-btn"
                  onClick={() =>
                    sendMessage(
                      suggestion.query
                    )
                  }
                  disabled={loading}
                >
                  <span className="suggestion-tag">
                    {suggestion.label}
                  </span>
                  {suggestion.query}
                </button>
              )
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <div className="input-row">
        <input
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          onKeyDown={(event) => {
            if (
              event.key === "Enter"
            ) {
              sendMessage();
            }
          }}
          placeholder="Ask a support question..."
        />

        <button
          onClick={() => sendMessage()}
          disabled={loading}
        >
          {loading
            ? "Thinking..."
            : "Send"}
        </button>
      </div>
    </section>
  );
}
