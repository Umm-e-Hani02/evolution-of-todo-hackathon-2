// TypeScript type definitions

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface TodoTask {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface CreateTodoData {
  title: string;
  description?: string;
  completed?: boolean; // For PUT operations (replace)
}

export interface UpdateTodoData {
  title?: string;
  description?: string | null;
  completed?: boolean;
}
