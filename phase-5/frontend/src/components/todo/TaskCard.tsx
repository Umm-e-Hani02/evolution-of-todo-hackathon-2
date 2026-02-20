"use client";

import { useState } from "react";
import { TodoTask } from "@/types";
import TaskEditForm from "./TaskEditForm";

interface TaskCardProps {
  todo: TodoTask;
  onUpdate: (id: string, data: Partial<TodoTask>) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onToggleComplete: (id: string, completed: boolean) => Promise<void>;
}

export default function TaskCard({
  todo,
  onUpdate,
  onDelete,
  onToggleComplete,
}: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggle = async () => {
    await onToggleComplete(todo.id, !todo.completed);
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      setIsDeleting(true);
      await onDelete(todo.id);
      setIsDeleting(false);
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

  if (isEditing) {
    return (
      <TaskEditForm
        todo={todo}
        onCancel={() => setIsEditing(false)}
        onSave={async (data) => {
          await onUpdate(todo.id, data);
          setIsEditing(false);
        }}
      />
    );
  }

  return (
    <li className={`todo-item ${todo.completed ? "completed" : ""}`}>
      <input
        type="checkbox"
        className="todo-checkbox"
        checked={todo.completed}
        onChange={handleToggle}
        aria-label={todo.completed ? "Mark as incomplete" : "Mark as complete"}
      />
      <div className="todo-content">
        <h3 className="todo-title">{todo.title}</h3>
        {todo.description && (
          <p className="todo-description">{todo.description}</p>
        )}
        <div className="todo-meta">
          <span className={`status-badge ${todo.completed ? "completed" : "pending"}`}>
            {todo.completed ? "Completed" : "Pending"}
          </span>
          <span className="todo-date">
            Created: {formatDate(todo.created_at)}
          </span>
        </div>
      </div>
      <div className="todo-actions">
        <button
          className="btn btn-edit"
          onClick={() => setIsEditing(true)}
          disabled={isDeleting}
          title="Edit task"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 02 2h14a2 2 0 0 02-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          <span>Edit</span>
        </button>
        <button
          className="btn btn-complete"
          onClick={handleToggle}
          title={todo.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 6L9 17l-5-5" />
          </svg>
          <span>{todo.completed ? "Undo" : "Complete"}</span>
        </button>
        <button
          className="btn btn-delete"
          onClick={handleDelete}
          disabled={isDeleting}
          title="Delete task"
        >
          {isDeleting ? (
            <span>...</span>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
              <span>Delete</span>
            </>
          )}
        </button>
      </div>
    </li>
  );
}
