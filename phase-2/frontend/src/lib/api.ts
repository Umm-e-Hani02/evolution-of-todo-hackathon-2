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
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
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
