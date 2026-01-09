"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import ThemeToggleButton from "@/components/ui/ThemeToggleButton";

interface AuthFormProps {
  type: "login" | "register";
  onSubmit: (data: { email: string; password: string }) => Promise<void>;
}

export default function AuthForm({ type, onSubmit }: AuthFormProps) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  const validate = () => {
    const newErrors: { email?: string; password?: string } = {};
    if (!email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Please enter a valid email address";
    }
    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await onSubmit({ email, password });
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <header className="auth-header">
          <div className="auth-brand">
            <h1>{type === "login" ? "Welcome Back" : "Create Account"}</h1>
            <p>
              {type === "login"
                ? "Sign in to access your todos"
                : "Start organizing your tasks today"}
            </p>
          </div>
          <ThemeToggleButton />
        </header>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={isSubmitting}
              autoComplete="email"
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={isSubmitting}
              autoComplete={type === "login" ? "current-password" : "new-password"}
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? type === "login"
                ? "Signing in..."
                : "Creating account..."
              : type === "login"
              ? "Sign In"
              : "Sign Up"}
          </button>
        </form>

        <footer className="auth-footer">
          {type === "login" ? (
            <>
              Don&apos;t have an account?{" "}
              <Link href="/register">Sign up</Link>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <Link href="/login">Sign in</Link>
            </>
          )}
        </footer>
      </div>
    </div>
  );
}
