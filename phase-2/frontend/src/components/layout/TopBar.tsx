"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "@/lib/auth-context";
import ThemeToggleButton from "@/components/ui/ThemeToggleButton";

interface TopBarProps {
  title: string;
}

export default function TopBar({ title }: TopBarProps) {
  const { user, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const getInitials = (email: string) => {
    return email.charAt(0).toUpperCase();
  };

  const getUsername = (email: string) => {
    return email.split('@')[0];
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  return (
    <div className="top-bar">
      <h1 className="page-title">{title}</h1>
      <div className="top-bar-actions">
        <ThemeToggleButton />
        <div className="user-menu" ref={dropdownRef}>
          <button
            className="user-avatar"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            title={user?.email}
          >
            {user && getInitials(user.email)}
          </button>

          {isDropdownOpen && (
            <div className="user-dropdown">
              <div className="dropdown-header">
                <div className="dropdown-avatar">
                  {user && getInitials(user.email)}
                </div>
                <div className="dropdown-user-info">
                  <div className="dropdown-username">{user && getUsername(user.email)}</div>
                  <div className="dropdown-email">{user?.email}</div>
                </div>
              </div>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item logout-item" onClick={logout}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" y1="12" x2="9" y2="12" />
                </svg>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
