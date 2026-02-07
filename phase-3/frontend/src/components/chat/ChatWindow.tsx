"use client";
import { useState, useRef, useEffect } from 'react';
import { todosAPI } from '@/lib/api';
import { useTheme } from '@/lib/theme-context';

interface ChatWindowProps {
  onClose: () => void;
}

const ChatWindow = ({ onClose }: ChatWindowProps) => {
  const { theme } = useTheme(); // Get current theme
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (input.trim() === '' || isLoading) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await todosAPI.chat({ message: input, conversation_id: conversationId });
      setConversationId(response.conversation_id);
      const assistantMessage = { role: 'assistant' as const, content: response.message };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={`chat-window ${theme}`}>
      <div className="chat-header">
        <h3>AI Assistant</h3>
        <button onClick={onClose} className="chat-close-btn" aria-label="Close chat">✕</button>
      </div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${msg.role} ${theme}`}
          >
            {msg.content}
          </div>
        ))}
        {isLoading && (
          <div className={`chat-message assistant ${theme}`}>
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message..."
          className="chat-input"
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          className="chat-send-btn"
          disabled={input.trim() === '' || isLoading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
