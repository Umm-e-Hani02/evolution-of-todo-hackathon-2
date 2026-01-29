"use client";

import { useAuth } from "@/lib/auth-context";
import ThemeToggleButton from "@/components/ui/ThemeToggleButton";
import Link from "next/link";

export default function Navbar() {
  const { user, logout, isLoading } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  if (isLoading) {
    return (
      <nav className="navbar">
        <div className="navbar-brand">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
          </svg>
          TodoApp
        </div>
      </nav>
    );
  }

  return (
    <nav className="navbar">
      <Link href="/dashboard" className="navbar-brand">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
        </svg>
        TodoApp
      </Link>
      {user && (
        <div className="navbar-user">
          <span className="user-email">{user.email}</span>
          <ThemeToggleButton />
          <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      )}
      {!user && (
        <div className="navbar-user">
          <ThemeToggleButton />
          <Link href="/login" className="btn btn-secondary btn-sm">
            Sign In
          </Link>
          <Link href="/register" className="btn btn-primary btn-sm">
            Sign Up
          </Link>
        </div>
      )}
    </nav>
  );
}
