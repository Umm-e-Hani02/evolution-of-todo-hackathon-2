from openai import OpenAI
from src.core.config import settings
from typing import List, Dict, Any

class OpenAIService:
    def __init__(self):
        # Check if using OpenRouter API key (starts with sk-or-v1)
        if settings.openai_api_key.startswith("sk-or-v1-"):
            # Configure for OpenRouter
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.openai_api_key,
            )
            # Default to a model that works well with OpenRouter
            self.model = getattr(settings, 'openai_model', 'openai/gpt-3.5-turbo')
        else:
            # Standard OpenAI configuration
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = getattr(settings, 'openai_model', 'gpt-3.5-turbo')

    def get_chat_response(self, messages: List[Dict[str, str]]) -> str:
        if not settings.openai_api_key:
            return "Error: OpenAI API key is not configured. Please set OPENAI_API_KEY in environment variables."

        try:
            # Make the API call to OpenAI-compatible service (like OpenRouter)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Slightly creative but coherent responses
                max_tokens=500,   # Limit response length
            )
            
            # Extract the content from the response
            content = response.choices[0].message.content
            
            # Validate that we got a proper response
            if not content or content.strip() == "":
                return "I'm sorry, I couldn't generate a response. Please try again."
                
            return content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Return a more user-friendly error message
            return f"I'm having trouble connecting to the AI service. Error: {str(e)[:100]}..."  # Truncate long errors

openai_service = OpenAIService()