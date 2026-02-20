"use client";

import { useState } from "react";
import Chatbot from "./Chatbot";

export default function ChatbotButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating chat button */}
      <button
        className="chatbot-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open chat assistant"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
      </button>

      {/* Chatbot modal */}
      {isOpen && <Chatbot onClose={() => setIsOpen(false)} />}
    </>
  );
}
