"use client";

import { useState } from 'react';
import ChatWindow from './ChatWindow';

const ChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        className="chat-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open chat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>
      {isOpen && <ChatWindow onClose={() => setIsOpen(false)} />}
    </>
  );
};

export default ChatButton;
