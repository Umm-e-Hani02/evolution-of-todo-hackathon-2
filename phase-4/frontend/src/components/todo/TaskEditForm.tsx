"use client";

import { useState } from "react";
import { TodoTask } from "@/types";

interface TaskEditFormProps {
  todo: TodoTask;
  onCancel: () => void;
  onSave: (data: Partial<TodoTask>) => Promise<void>;
}

export default function TaskEditForm({ todo, onCancel, onSave }: TaskEditFormProps) {
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description || "");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ title?: string }>({});

  const validate = () => {
    const newErrors: { title?: string } = {};
    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length > 500) {
      newErrors.title = "Title must be 500 characters or less";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await onSave({
        title: title.trim(),
        description: description.trim() || undefined,
      });
    } catch (error) {
      console.error("Failed to update task:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <li className="todo-item">
      <form onSubmit={handleSubmit} style={{ width: "100%" }}>
        <div className="form-group" style={{ marginBottom: "0.75rem" }}>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
            maxLength={500}
            disabled={isSubmitting}
            style={{ fontWeight: 500 }}
          />
          {errors.title && (
            <span className="error-message" style={{ marginTop: "0.25rem", display: "block" }}>
              {errors.title}
            </span>
          )}
        </div>
        <div className="form-group" style={{ marginBottom: "0.75rem" }}>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            rows={2}
            disabled={isSubmitting}
          />
        </div>
        <div className="todo-actions" style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end", marginLeft: 0 }}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={onCancel}
            disabled={isSubmitting}
            title="Cancel editing"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M6 18L18 6M6 6l12 12" />
            </svg>
            <span>Cancel</span>
          </button>
          <button type="submit" className="btn btn-primary btn-sm" disabled={isSubmitting}>
            {isSubmitting ? (
              <span>Saving...</span>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
                  <polyline points="17 21 17 13 7 13 7 21" />
                  <polyline points="7 3 7 8 15 8" />
                </svg>
                <span>Save</span>
              </>
            )}
          </button>
        </div>
      </form>
    </li>
  );
}
