'use client';

import { useState } from 'react';
import { TodoTask } from '@/types';
import TaskEditForm from './TaskEditForm';

interface TaskItemProps {
  todo: TodoTask;
  onToggle: (todo: TodoTask) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, data: Partial<TodoTask>) => Promise<void>;
}

export default function TaskItem({ todo, onToggle, onDelete, onEdit }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);

  if (isEditing) {
    return (
      <TaskEditForm
        todo={todo}
        onSave={async (data) => {
          await onEdit(todo.id, data);
          setIsEditing(false);
        }}
        onCancel={() => setIsEditing(false)}
      />
    );
  }

  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        className="todo-checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo)}
        aria-label={todo.completed ? 'Mark as incomplete' : 'Mark as complete'}
      />
      <div className="todo-content" style={{ flex: 1 }}>
        <div className="todo-title">{todo.title}</div>
        {todo.description && (
          <div className="todo-description">{todo.description}</div>
        )}
      </div>
      <div className="todo-actions">
        <button
          onClick={() => setIsEditing(true)}
          className="btn btn-secondary btn-sm"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(todo.id)}
          className="btn btn-danger btn-sm"
        >
          Delete
        </button>
      </div>
    </li>
  );
}
