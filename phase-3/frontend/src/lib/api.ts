// API client with JWT token handling
import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { AuthResponse, CreateTodoData, UpdateTodoData, TodoTask } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Extract friendly error message from response
    let errorMessage = 'An unexpected error occurred. Please try again.';

    if (error.response?.data?.detail) {
      // Backend returns error in 'detail' field
      errorMessage = error.response.data.detail;
    } else if (error.response?.status === 401) {
      errorMessage = 'Invalid email or password. Please try again.';
    } else if (error.response?.status === 409) {
      errorMessage = 'This email is already registered. Please log in or use a different email.';
    } else if (error.response?.status === 422) {
      errorMessage = 'Invalid input. Please fill all required fields correctly and ensure your email is valid.';
    } else if (error.response?.status === 429) {
      errorMessage = 'Too many login attempts. Please wait a moment and try again.';
    } else if (error.response?.status === 500) {
      errorMessage = 'Server error. Please try again later.';
    } else if (error.message === 'Network Error') {
      errorMessage = 'Unable to connect to the server. Please check your internet connection.';
    }

    // For 401 errors on protected routes, redirect to login
    if (error.response?.status === 401 && !error.config?.url?.includes('/auth/')) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    // Create a new error with the friendly message
    const friendlyError = new Error(errorMessage);
    return Promise.reject(friendlyError);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', { email, password });
    return response.data;
  },

  register: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/register', { email, password });
    return response.data;
  },

  me: async (): Promise<{ id: string; email: string; created_at: string }> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Todos API
export const todosAPI = {
  list: async (): Promise<TodoTask[]> => {
    const response = await api.get<TodoTask[]>('/todos');
    return response.data;
  },

  get: async (id: string): Promise<TodoTask> => {
    const response = await api.get<TodoTask>(`/todos/${id}`);
    return response.data;
  },

  addTodo: async (data: CreateTodoData): Promise<TodoTask> => {
    const response = await api.post<TodoTask>('/todos', data);
    return response.data;
  },

  update: async (id: string, data: UpdateTodoData): Promise<TodoTask> => {
    const response = await api.patch<TodoTask>(`/todos/${id}`, data);
    return response.data;
  },

  replace: async (id: string, data: CreateTodoData): Promise<TodoTask> => {
    const response = await api.put<TodoTask>(`/todos/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/todos/${id}`);
  },

  chat: async (data: { message: string; conversation_id?: number }): Promise<{
    conversation_id: number;
    response: string;
    tool_calls: Array<{ tool: string; arguments: any; result: any }>;
  }> => {
    const response = await api.post('/api/chat', data);
    return response.data;
  },

  getConversationHistory: async (conversationId: number): Promise<{
    conversation_id: number;
    messages: Array<{ id: number; role: string; content: string; created_at: string }>;
  }> => {
    const response = await api.get(`/api/conversations/${conversationId}/messages`);
    return response.data;
  },
};

// Token management
export const tokenManager = {
  getToken: (): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  },

  setToken: (token: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  },

  removeToken: (): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  setUser: (user: { id: string; email: string; created_at: string }): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('user', JSON.stringify(user));
    }
  },

  getUser: (): { id: string; email: string; created_at: string } | null => {
    if (typeof window !== 'undefined') {
      const user = localStorage.getItem('user');
      return user ? JSON.parse(user) : null;
    }
    return null;
  },

  isAuthenticated: (): boolean => {
    return tokenManager.getToken() !== null;
  },
};

export default api;
