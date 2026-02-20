"""Chatbot service for handling chat interactions."""
import os
from typing import Dict, Any
from sqlmodel import Session
from openai import OpenAI
from src.core.database import get_todos_by_user
from src.models.todo import TodoTask


class ChatbotService:
    """Service for chatbot functionality."""

    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. LLM features will not work.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    async def handle_task_intent(
        self,
        intent: Dict[str, Any],
        user_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Handle task-related intents by calling existing task APIs.

        This does NOT modify task logic - it uses existing functions.
        """
        action = intent["action"]
        entities = intent["entities"]

        if action == "create":
            return await self._handle_create_task(entities, user_id, db)
        elif action == "list":
            return await self._handle_list_tasks(user_id, db)
        elif action == "complete":
            return {"message": "To complete a task, please use the task list interface."}
        elif action == "delete":
            return {"message": "To delete a task, please use the task list interface."}
        elif action == "update":
            return {"message": "To update a task, please use the task list interface."}
        else:
            return {"message": "I can help you manage tasks. Try 'add task' or 'show my tasks'."}

    async def _handle_create_task(
        self,
        entities: Dict[str, Any],
        user_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Create a new task using existing task creation logic."""
        title = entities.get("title")

        if not title:
            return {"message": "Please specify what task you'd like to add."}

        # Use existing TodoTask model (not modifying existing logic)
        new_task = TodoTask(
            user_id=user_id,
            title=title,
            description=None,
            completed=False
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {
            "message": f"✓ Task created: {title}",
            "action": "task_created",
            "data": {"task_id": new_task.id, "title": new_task.title}
        }

    async def _handle_list_tasks(self, user_id: str, db: Session) -> Dict[str, Any]:
        """List user's tasks using existing database function."""
        # Use existing function from database.py
        tasks = get_todos_by_user(db, user_id)

        if not tasks:
            return {"message": "You don't have any tasks yet."}

        # Format task list
        task_list = []
        for task in tasks:
            status = "✓" if task.completed else "○"
            task_list.append(f"{status} {task.title}")

        message = f"You have {len(tasks)} task(s):\n" + "\n".join(task_list)

        return {
            "message": message,
            "action": "tasks_listed",
            "data": {"count": len(tasks)}
        }

    async def get_llm_response(self, message: str, user_email: str) -> str:
        """Get response from LLM for general conversation."""
        if not self.client:
            return "I'm a task management assistant. I can help you add tasks or show your task list. LLM features are not configured."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful task management assistant. Keep responses brief and friendly."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"LLM error: {e}")
            return "I'm having trouble processing that. Try asking about your tasks or adding a new task."
