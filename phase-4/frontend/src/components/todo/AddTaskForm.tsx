"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface AddTaskFormProps {
  onAdd: (data: { title: string; description?: string }) => Promise<void>;
}

export default function AddTaskForm({ onAdd }: AddTaskFormProps) {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});

  const validate = () => {
    const newErrors: { title?: string; description?: string } = {};
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
      await onAdd({ title: title.trim(), description: description.trim() || undefined });
      setTitle("");
      setDescription("");
      setErrors({});
    } catch (error) {
      console.error("Failed to add task:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="task-form-card">
      <h2>Add New Task</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            maxLength={500}
            disabled={isSubmitting}
          />
          {errors.title && <span className="error-message" style={{ marginTop: "0.5rem", display: "block" }}>{errors.title}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="description">Description (optional)</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details..."
            rows={3}
            disabled={isSubmitting}
          />
          {errors.description && <span className="error-message" style={{ marginTop: "0.5rem", display: "block" }}>{errors.description}</span>}
        </div>
        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => router.push("/dashboard")}
            title="Cancel and return to dashboard"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M6 18L18 6M6 6l12 12" />
            </svg>
            <span>Cancel</span>
          </button>
          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? (
              <span>Adding...</span>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 5v14M5 12h14" />
                </svg>
                <span>Add Task</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
