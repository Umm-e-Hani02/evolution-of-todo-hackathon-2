"""Intent detection service for chatbot."""
import re
from typing import Dict, Any


class IntentDetector:
    """Detects user intent from chat messages."""

    def __init__(self):
        # Task-related keywords
        self.task_keywords = {
            "create": ["add", "create", "make", "new task", "todo"],
            "list": ["show", "list", "display", "what are", "my tasks"],
            "update": ["update", "edit", "change", "modify"],
            "delete": ["delete", "remove", "clear"],
            "complete": ["complete", "done", "finish", "mark as done"]
        }

    def detect_intent(self, message: str) -> Dict[str, Any]:
        """
        Detect if message is task-related and what action is intended.

        Returns:
            {
                "is_task_related": bool,
                "action": str | None,  # "create", "list", "update", "delete", "complete"
                "entities": dict  # Extracted information (task title, etc.)
            }
        """
        message_lower = message.lower().strip()

        # Check for task-related keywords
        for action, keywords in self.task_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return {
                        "is_task_related": True,
                        "action": action,
                        "entities": self._extract_entities(message, action)
                    }

        # Not task-related
        return {
            "is_task_related": False,
            "action": None,
            "entities": {}
        }

    def _extract_entities(self, message: str, action: str) -> Dict[str, Any]:
        """Extract relevant information from message based on action."""
        entities = {}

        if action == "create":
            # Extract task title after keywords
            patterns = [
                r"(?:add|create|make|new)\s+(?:task|todo)?\s*[:\-]?\s*(.+)",
                r"(?:add|create|make)\s+(.+)",
            ]
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    entities["title"] = match.group(1).strip()
                    break

        elif action in ["delete", "complete", "update"]:
            # Extract task number (e.g., "delete task 1", "complete 2")
            number_match = re.search(r"(?:task|number)?\s*(\d+)", message, re.IGNORECASE)
            if number_match:
                entities["task_number"] = int(number_match.group(1))

            # Extract task name/title (e.g., "delete 'buy groceries'", "complete the hackathon task")
            # Look for quoted text first
            quoted_match = re.search(r"['\"](.+?)['\"]", message)
            if quoted_match:
                entities["task_name"] = quoted_match.group(1).strip()
            else:
                # Try to extract task name after action keywords
                name_patterns = [
                    r"(?:delete|remove|complete|done|finish|update|edit)\s+(?:the\s+)?(?:task\s+)?(?:named\s+)?(.+)",
                ]
                for pattern in name_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        potential_name = match.group(1).strip()
                        # Filter out common words that aren't task names
                        if potential_name and potential_name.lower() not in ["task", "it", "this", "that"]:
                            entities["task_name"] = potential_name
                            break

        return entities
