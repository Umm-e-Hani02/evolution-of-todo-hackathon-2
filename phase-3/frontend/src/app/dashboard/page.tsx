"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { todosAPI } from "@/lib/api";
import { TodoTask } from "@/types";
import { useAuth } from "@/lib/auth-context";
import Sidebar from "@/components/layout/Sidebar";
import TopBar from "@/components/layout/TopBar";
import ChatbotButton from "@/components/chat/ChatbotButton";

export default function DashboardPage() {
  const router = useRouter();
  const { logout, user, isAuthenticated, isLoading: authLoading } = useAuth();

  if (!authLoading && !isAuthenticated) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    return null;
  }

  const [todos, setTodos] = useState<TodoTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [activeFilter, setActiveFilter] = useState<"all" | "completed" | "pending">("all");
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState<TodoTask | null>(null);

  // Form states
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isEditSubmitting, setIsEditSubmitting] = useState(false);

  // Operation loading states
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);
  const [togglingTaskId, setTogglingTaskId] = useState<string | null>(null);

  const loadTodos = async () => {
    try {
      const data = await todosAPI.list();
      setTodos(data);
    } catch (err) {
      console.error("Failed to load todos:", err);
      setError("Failed to load tasks. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTodos();

    // Listen for task modifications from chatbot
    const handleTasksModified = () => {
      console.log("[Dashboard] Tasks modified event received, reloading...");
      loadTodos();
    };

    window.addEventListener("tasksModified", handleTasksModified);

    return () => {
      window.removeEventListener("tasksModified", handleTasksModified);
    };
  }, []);

  const filteredTodos = todos.filter((todo) => {
    if (activeFilter === "completed") return todo.completed;
    if (activeFilter === "pending") return !todo.completed;
    return true;
  });

  const stats = {
    total: todos.length,
    completed: todos.filter((t) => t.completed).length,
    pending: todos.filter((t) => !t.completed).length,
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    setError("");
    setSuccessMessage("");

    try {
      const newTodo = await todosAPI.addTodo({
        title: title.trim(),
        description: description.trim() || undefined,
      });
      setTodos([newTodo, ...todos]);
      setTitle("");
      setDescription("");
      setShowAddForm(false);
      setSuccessMessage("Task created successfully!");

      // Auto-dismiss success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to create task. Please try again.";
      setError(errorMsg);

      // Auto-dismiss error message after 5 seconds
      setTimeout(() => setError(""), 5000);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateTask = async (id: string, data: Partial<TodoTask>) => {
    setError("");
    setSuccessMessage("");

    // Store original state for rollback
    const originalTodos = [...todos];

    // Optimistic update
    const optimisticTodos = todos.map((t) =>
      t.id === id ? { ...t, ...data } : t
    );
    setTodos(optimisticTodos);

    try {
      const updateData: { title?: string; description?: string; completed?: boolean } = {};
      if ('title' in data && data.title !== undefined) updateData.title = data.title;
      if ('description' in data && data.description !== undefined && data.description !== null) {
        updateData.description = data.description;
      }
      if ('completed' in data && data.completed !== undefined) updateData.completed = data.completed;

      const updated = await todosAPI.update(id, updateData);

      // Update with server response (use functional update to avoid stale closure)
      setTodos(prevTodos => prevTodos.map((t) => (t.id === id ? updated : t)));
      setEditingTask(null);
      setSuccessMessage("Task updated successfully!");

      // Auto-dismiss success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      // Rollback on failure
      setTodos(originalTodos);

      const errorMsg = err instanceof Error ? err.message : "Failed to update task. Please try again.";
      setError(errorMsg);

      // Auto-dismiss error message after 5 seconds
      setTimeout(() => setError(""), 5000);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      setError("");
      setSuccessMessage("");
      setDeletingTaskId(id);

      // Store original state for rollback
      const originalTodos = [...todos];

      // Optimistic update
      setTodos(todos.filter((t) => t.id !== id));

      try {
        await todosAPI.delete(id);
        setSuccessMessage("Task deleted successfully!");

        // Auto-dismiss success message after 3 seconds
        setTimeout(() => setSuccessMessage(""), 3000);
      } catch (err) {
        // Rollback on failure
        setTodos(originalTodos);

        const errorMsg = err instanceof Error ? err.message : "Failed to delete task. Please try again.";
        setError(errorMsg);

        // Auto-dismiss error message after 5 seconds
        setTimeout(() => setError(""), 5000);
      } finally {
        setDeletingTaskId(null);
      }
    }
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    setError("");
    setSuccessMessage("");
    setTogglingTaskId(id);

    // Store original state for rollback
    const originalTodos = [...todos];

    // Optimistic update
    const optimisticTodos = todos.map((t) =>
      t.id === id ? { ...t, completed } : t
    );
    setTodos(optimisticTodos);

    try {
      const updated = await todosAPI.update(id, { completed });

      // Update with server response (use functional update to avoid stale closure)
      setTodos(prevTodos => prevTodos.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      // Rollback on failure
      setTodos(originalTodos);

      const errorMsg = err instanceof Error ? err.message : "Failed to update task status. Please try again.";
      setError(errorMsg);

      // Auto-dismiss error message after 5 seconds
      setTimeout(() => setError(""), 5000);
    } finally {
      setTogglingTaskId(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  if (isLoading) {
    return (
      <div className="dashboard-container">
        <Sidebar activeFilter={activeFilter} onFilterChange={setActiveFilter} />
        <div className="main-content">
          <TopBar title="Dashboard" />
          <div className="content-area">
            <div className="loading-state">Loading your tasks...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar activeFilter={activeFilter} onFilterChange={setActiveFilter} />

      <div className="main-content">
        <TopBar title="Dashboard" />

        <div className="content-area">
          {/* Stats Section */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon stat-total">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div className="stat-info">
                <div className="stat-value">{stats.total}</div>
                <div className="stat-label">Total Tasks</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon stat-completed">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              </div>
              <div className="stat-info">
                <div className="stat-value">{stats.completed}</div>
                <div className="stat-label">Completed</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon stat-pending">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <div className="stat-info">
                <div className="stat-value">{stats.pending}</div>
                <div className="stat-label">Pending</div>
              </div>
            </div>
          </div>

          {/* Add Task Button */}
          {!showAddForm && (
            <button
              className="add-task-btn"
              onClick={() => setShowAddForm(true)}
              disabled={isSubmitting}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              Add New Task
            </button>
          )}

          {/* Add Task Form */}
          {showAddForm && (
            <div className="task-form-card">
              <div className="form-header">
                <h3>Add New Task</h3>
                <button className="close-btn" onClick={() => setShowAddForm(false)}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
              <form onSubmit={handleAddTask}>
                <div className="form-group">
                  <label htmlFor="title">Title</label>
                  <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="What needs to be done?"
                    required
                    disabled={isSubmitting}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Add more details..."
                    rows={3}
                    disabled={isSubmitting}
                  />
                </div>
                <div className="form-actions">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setShowAddForm(false)}
                    disabled={isSubmitting}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                    {isSubmitting ? (
                      <>
                        <span className="loading-spinner small"></span>
                        Adding...
                      </>
                    ) : (
                      "Add Task"
                    )}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Task List */}
          {error && (
            <div className="error-message">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
            </div>
          )}

          {successMessage && (
            <div className="success-message">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
              {successMessage}
            </div>
          )}

          {filteredTodos.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3>No tasks found</h3>
              <p>
                {activeFilter === "completed" && "You haven't completed any tasks yet."}
                {activeFilter === "pending" && "You don't have any pending tasks."}
                {activeFilter === "all" && "Create your first task to get started!"}
              </p>
            </div>
          ) : (
            <div className="tasks-grid">
              {filteredTodos.map((todo) => (
                <div key={todo.id} className={`task-card ${todo.completed ? "completed" : "pending"} ${togglingTaskId === todo.id || deletingTaskId === todo.id ? "loading" : ""}`}>
                  <div className="task-header">
                    <div className="task-checkbox-wrapper">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => handleToggleComplete(todo.id, !todo.completed)}
                        className="task-checkbox"
                        disabled={togglingTaskId === todo.id || deletingTaskId === todo.id}
                      />
                      {togglingTaskId === todo.id && (
                        <span className="loading-spinner"></span>
                      )}
                    </div>
                    <span className={`task-status ${todo.completed ? "status-completed" : "status-pending"}`}>
                      {todo.completed ? "Completed" : "Pending"}
                    </span>
                  </div>

                  <div className="task-body">
                    <h4 className="task-title">{todo.title}</h4>
                    {todo.description && (
                      <p className="task-description">{todo.description}</p>
                    )}
                  </div>

                  <div className="task-footer">
                    <span className="task-date">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="12 6 12 12 16 14" />
                      </svg>
                      {formatDate(todo.created_at)}
                    </span>
                    <div className="task-actions">
                      <button
                        className="action-btn edit-btn"
                        onClick={() => setEditingTask(todo)}
                        title="Edit task"
                        disabled={togglingTaskId === todo.id || deletingTaskId === todo.id}
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 02 2h14a2 2 0 0 02-2v-7" />
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                        </svg>
                      </button>
                      <button
                        className="action-btn delete-btn"
                        onClick={() => handleDeleteTask(todo.id)}
                        title="Delete task"
                        disabled={togglingTaskId === todo.id || deletingTaskId === todo.id}
                      >
                        {deletingTaskId === todo.id ? (
                          <span className="loading-spinner small"></span>
                        ) : (
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                          </svg>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Edit Task Modal */}
          {editingTask && (
            <div className="modal-overlay" onClick={() => setEditingTask(null)}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="form-header">
                  <h3>Edit Task</h3>
                  <button className="close-btn" onClick={() => setEditingTask(null)}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18" />
                      <line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                  </button>
                </div>
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    setIsEditSubmitting(true);
                    const formData = new FormData(e.currentTarget);
                    handleUpdateTask(editingTask.id, {
                      title: formData.get("title") as string,
                      description: formData.get("description") as string,
                    }).finally(() => setIsEditSubmitting(false));
                  }}
                >
                  <div className="form-group">
                    <label htmlFor="edit-title">Title</label>
                    <input
                      type="text"
                      id="edit-title"
                      name="title"
                      defaultValue={editingTask.title}
                      required
                      disabled={isEditSubmitting}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="edit-description">Description</label>
                    <textarea
                      id="edit-description"
                      name="description"
                      defaultValue={editingTask.description || ""}
                      rows={3}
                      disabled={isEditSubmitting}
                    />
                  </div>
                  <div className="form-actions">
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => setEditingTask(null)}
                      disabled={isEditSubmitting}
                    >
                      Cancel
                    </button>
                    <button type="submit" className="btn btn-primary" disabled={isEditSubmitting}>
                      {isEditSubmitting ? (
                        <>
                          <span className="loading-spinner small"></span>
                          Saving...
                        </>
                      ) : (
                        "Save Changes"
                      )}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Chatbot Assistant */}
      <ChatbotButton />
    </div>
  );
}
