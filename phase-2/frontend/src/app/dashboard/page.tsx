"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { todosAPI } from "@/lib/api";
import { TodoTask } from "@/types";
import TaskCard from "@/components/todo/TaskCard";
import AddTaskForm from "@/components/todo/AddTaskForm";
import { useAuth } from "@/lib/auth-context";
import ThemeToggleButton from "@/components/ui/ThemeToggleButton";

export default function DashboardPage() {
  const router = useRouter();
  const { logout, user, isAuthenticated, isLoading: authLoading } = useAuth();

  // If user is not authenticated, redirect to login
  if (!authLoading && !isAuthenticated) {
    // We can't use router.push here in the same render cycle,
    // so we'll handle the redirect in a useEffect or return early
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    return null;
  }
  const [todos, setTodos] = useState<TodoTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });

  const loadTodos = async () => {
    try {
      const data = await todosAPI.list();
      setTodos(data);
      updateStats(data);
    } catch (err) {
      console.error("Failed to load todos:", err);
      setError("Failed to load tasks. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const updateStats = (todos: TodoTask[]) => {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;
    const pending = total - completed;
    setStats({ total, completed, pending });
  };

  useEffect(() => {
    loadTodos();
  }, []);

  useEffect(() => {
    updateStats(todos);
  }, [todos]);

  const handleAddTask = async (data: { title: string; description?: string }) => {
    try {
      const newTodo = await todosAPI.addTodo(data);
      setTodos([newTodo, ...todos]);
      setShowAddForm(false);
    } catch (err) {
      console.error("Failed to create task:", err);
      throw err;
    }
  };

  const handleUpdateTask = async (id: string, data: Partial<TodoTask>) => {
    try {
      // Convert Partial<TodoTask> to UpdateTodoData to match API expectations
      const updateData: Partial<Record<string, unknown>> = { ...data };
      if ('description' in updateData && updateData.description === null) {
        delete updateData.description; // Remove null values to match UpdateTodoData
      }

      const typedData: Partial<Omit<TodoTask, 'id' | 'user_id' | 'created_at' | 'updated_at'>> = updateData;
      const transformedData: { title?: string; description?: string; completed?: boolean } = {};

      if ('title' in typedData && typedData.title !== undefined) {
        transformedData.title = typedData.title;
      }
      if ('description' in typedData && typedData.description !== undefined && typedData.description !== null) {
        transformedData.description = typedData.description;
      }
      if ('completed' in typedData && typedData.completed !== undefined) {
        transformedData.completed = typedData.completed;
      }

      const updated = await todosAPI.update(id, transformedData);
      setTodos(todos.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      console.error("Failed to update task:", err);
      throw err;
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await todosAPI.delete(id);
      setTodos(todos.filter((t) => t.id !== id));
    } catch (err) {
      console.error("Failed to delete task:", err);
      throw err;
    }
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      const updated = await todosAPI.update(id, { completed });
      setTodos(todos.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      console.error("Failed to toggle task:", err);
      throw err;
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (isLoading) {
    return (
      <div className="dashboard-layout">
        <nav className="navbar">
          <div className="navbar-brand">
            <div className="navbar-logo">
  <img src="/todopro-logo.png" alt="TodoPro Logo" width="40" height="40" />
  <h1>TodoPro</h1>
</div>
          </div>
          <div className="navbar-user">
            <span className="user-email">{user?.email}</span>
            <ThemeToggleButton />
            <button className="btn btn-secondary" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </nav>
        <div className="dashboard-content">
          <div className="loading">Loading your tasks...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <div className="navbar-logo">
  <img src="/todopro-logo.png" alt="TodoPro Logo" width="40" height="40" />
  <h1>TodoPro</h1>
</div>
        </div>
        <div className="navbar-user">
          <span className="user-email">{user?.email}</span>
          <ThemeToggleButton />
          <button className="btn btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </nav>

      <main className="dashboard-main">
        <div className="dashboard-header">
          <div className="dashboard-title">
            <h1>My Tasks</h1>
            <p className="dashboard-subtitle">Manage your daily activities</p>
          </div>
          <div className="dashboard-stats">
            <div className="stat-card">
              <div className="stat-value">{stats.total}</div>
              <div className="stat-label">Total</div>
            </div>
            <div className="stat-card">
              <div className="stat-value completed">{stats.completed}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-card">
              <div className="stat-value pending">{stats.pending}</div>
              <div className="stat-label">Pending</div>
            </div>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showAddForm ? (
          <AddTaskForm
            onAdd={handleAddTask}
          />
        ) : (
          <div className="header-actions">
            <button
              className="btn btn-primary"
              onClick={() => setShowAddForm(true)}
            >
              + Add New Task
            </button>
          </div>
        )}

        {todos.length === 0 ? (
          <div className="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            <h3>No tasks yet</h3>
            <p>Create your first task to get started!</p>
          </div>
        ) : (
          <ul className="todo-list">
            {todos.map((todo) => (
              <TaskCard
                key={todo.id}
                todo={todo}
                onUpdate={handleUpdateTask}
                onDelete={handleDeleteTask}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
