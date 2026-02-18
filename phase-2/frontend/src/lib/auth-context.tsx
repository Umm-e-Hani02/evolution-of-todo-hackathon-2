"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI, tokenManager } from '@/lib/api';
import { User } from '@/types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check for existing session on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = tokenManager.getToken();
      const savedUser = tokenManager.getUser();

      if (token && savedUser) {
        try {
          // Verify token is still valid
          const currentUser = await authAPI.me();
          setUser(currentUser);
        } catch {
          // Token is invalid
          tokenManager.removeToken();
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      tokenManager.setToken(response.token);
      tokenManager.setUser(response.user);
      setUser(response.user);
      router.push('/dashboard');
    } catch (error) {
      // Re-throw the error so the form can display it
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await authAPI.register(email, password);
      tokenManager.setToken(response.token);
      tokenManager.setUser(response.user);
      setUser(response.user);
      router.push('/dashboard');
    } catch (error) {
      // Re-throw the error so the form can display it
      throw error;
    }
  };

  const logout = () => {
    tokenManager.removeToken();
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
