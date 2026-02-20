"use client";

import { useState, useRef, useEffect } from "react";
import { todosAPI } from "@/lib/api";
import "./chatbot.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatbotProps {
  onClose: () => void;
}

const CONVERSATION_KEY = "chatbot_conversation_id";

export default function Chatbot({ onClose }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history on mount
  useEffect(() => {
    const loadConversationHistory = async () => {
      try {
        // Check if there's a stored conversation_id
        const storedConversationId = localStorage.getItem(CONVERSATION_KEY);

        if (storedConversationId) {
          const convId = parseInt(storedConversationId, 10);
          setConversationId(convId);

          // Fetch conversation history from database
          const history = await todosAPI.getConversationHistory(convId);

          if (history.messages.length > 0) {
            // Restore messages from database
            setMessages(
              history.messages.map((msg) => ({
                role: msg.role as "user" | "assistant",
                content: msg.content,
              }))
            );
          } else {
            // Empty conversation - get AI greeting
            await sendInitialGreeting();
          }
        } else {
          // New conversation - get AI greeting
          await sendInitialGreeting();
        }
      } catch (error) {
        console.error("Error loading conversation history:", error);
        // On error, get AI greeting
        await sendInitialGreeting();
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadConversationHistory();
  }, []);

  const sendInitialGreeting = async () => {
    try {
      // Send a greeting to the AI to get a natural response
      const response = await todosAPI.chat({
        message: "hi",
        conversation_id: conversationId || undefined,
      });

      // Store conversation_id
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
        localStorage.setItem(CONVERSATION_KEY, response.conversation_id.toString());
      }

      // Add AI's response (don't show the "hi" message)
      setMessages([
        { role: "assistant", content: response.response },
      ]);
    } catch (error) {
      console.error("Error sending initial greeting:", error);
      // Fallback to default message only on error
      setMessages([
        {
          role: "assistant",
          content: "Hey! I'm here to help you manage your tasks. What would you like to do?",
        },
      ]);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");

    // Add user message to UI immediately
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // Call stateless chat API with conversation_id
      const response = await todosAPI.chat({
        message: userMessage,
        conversation_id: conversationId || undefined,
      });

      // Store conversation_id if this is the first message
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
        localStorage.setItem(CONVERSATION_KEY, response.conversation_id.toString());
      }

      // Add assistant response to UI
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.response },
      ]);

      // If tasks were modified, trigger refresh
      if (response.tool_calls && response.tool_calls.length > 0) {
        const hasTaskOperation = response.tool_calls.some((tc) =>
          ["create_task", "delete_task", "update_task", "complete_task"].includes(tc.tool)
        );

        if (hasTaskOperation) {
          console.log("[Chatbot] Task operation detected, triggering refresh");
          window.dispatchEvent(new Event("tasksModified"));
        }
      }
    } catch (error) {
      console.error("[Chatbot] Error sending message:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewConversation = async () => {
    // Clear conversation and start fresh
    localStorage.removeItem(CONVERSATION_KEY);
    setConversationId(null);
    setMessages([]);

    // Get AI greeting for new conversation
    await sendInitialGreeting();
  };

  if (isLoadingHistory) {
    return (
      <div className="chatbot-container">
        <div className="chatbot-header">
          <h3>Task Assistant</h3>
          <button className="chatbot-close" onClick={onClose} aria-label="Close chat">
            ×
          </button>
        </div>
        <div className="chatbot-messages">
          <div className="chatbot-message assistant">
            <div className="message-content">Loading conversation...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Task Assistant</h3>
        <button
          className="chatbot-new-conversation"
          onClick={handleNewConversation}
          aria-label="New conversation"
          title="Start new conversation"
        >
          +
        </button>
        <button className="chatbot-close" onClick={onClose} aria-label="Close chat">
          ×
        </button>
      </div>

      <div className="chatbot-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chatbot-message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="chatbot-message assistant">
            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chatbot-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}
