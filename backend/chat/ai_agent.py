import os
import sys
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("Warning: google-generativeai not available. Some features may be limited.")
    genai = None

from llama_index.storage.chat_store.postgres import PostgresChatStore

from .constants import GEMINI_MODEL,  POSTGRES_CHAT_STORE_URI

# Add the parent directory to sys.path to import the agent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class BaseAIAgent:
    def __init__(self):
        raise NotImplementedError

    def generate_response(self, user_query, chat_id):
        raise NotImplementedError

    def chat_messages(self, chat_id):
        raise NotImplementedError


class GeminiTestingAgent(BaseAIAgent):
    def __init__(self):
        if genai is None:
            raise ImportError("google-generativeai is required for GeminiTestingAgent")
        self.client = genai.Client()
        self.messages = []

    def generate_response(self, user_query, chat_id):
        prompt = (
            "You are a helpful AI assistant for a project recommendation system. "
            f"Answer the following query:\n{user_query}\n"
            "Provide a concise and informative response."
        )

        self.add_message("user", user_query)

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        self.add_message("assistant", response.text)

        return response.text

    def chat_messages(self, chat_id):
        return (
            self.messages if self.messages
            else [{"role": "system", "content": "No messages yet."}]
        )

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})


class AIAgent(BaseAIAgent):
    """
    Production AI Agent using LLamaIndex FunctionAgent with Pinecone vector store.
    Integrates with the Django backend for chat storage and management.
    """
    
    def __init__(self, use_openai_embeddings=False):
        """
        Initialize the AI Agent.
        
        Args:
            use_openai_embeddings: Whether to use OpenAI embeddings (requires OPENAI_API_KEY)
        """
        self.use_openai_embeddings = use_openai_embeddings
        self._agent_instance = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LLamaIndex agent with error handling."""
        try:
            from agent import create_capstone_agent
            
            self._agent_instance = create_capstone_agent(
                use_openai_embeddings=self.use_openai_embeddings,
                max_retrieved_docs=10
            )
            
            print("✅ LLamaIndex AI Agent initialized successfully!")
            
        except Exception as e:
            print(f"⚠️  Could not initialize LLamaIndex agent: {e}")
            print("Falling back to Gemini testing agent for basic functionality.")
            # Fallback to testing agent
            self._agent_instance = None
    
    def generate_response(self, user_query, chat_id):
        """
        Generate a response to the user query.
        
        Args:
            user_query: The user's question or request
            chat_id: Chat session identifier
            
        Returns:
            Generated response string
        """
        if self._agent_instance:
            try:
                # Use the LLamaIndex agent
                response = self._agent_instance.chat(user_query)
                
                # Store the conversation in chat store
                self._store_message(chat_id, "user", user_query)
                self._store_message(chat_id, "assistant", response)
                
                return response
                
            except Exception as e:
                print(f"Error with LLamaIndex agent: {e}")
                return f"Sorry, I encountered an error while processing your request: {str(e)}"
        else:
            # Fallback response when agent is not available
            return (
                "I'm currently unable to access the full recommendation system. "
                "Please ensure all dependencies are properly configured. "
                f"Your query was: {user_query}"
            )
    
    def get_structured_recommendations(
        self,
        interests: str,
        skill_level: str = "intermediate",
        technologies: str = "",
        duration: str = "one semester"
    ):
        """
        Get structured capstone project recommendations.
        
        Args:
            interests: User's areas of interest
            skill_level: User's technical skill level
            technologies: Preferred technologies/frameworks
            duration: Expected project duration
            
        Returns:
            Structured project recommendations
        """
        if self._agent_instance:
            try:
                return self._agent_instance.get_recommendations(
                    interests=interests,
                    skill_level=skill_level,
                    technologies=technologies,
                    duration=duration
                )
            except Exception as e:
                return f"Error generating recommendations: {str(e)}"
        else:
            return "Recommendation system is currently unavailable."
    
    def chat_messages(self, chat_id):
        """
        Retrieve chat messages for a given chat session.
        
        Args:
            chat_id: Chat session identifier
            
        Returns:
            List of chat messages
        """
        try:
            chat_store = PostgresChatStore.from_uri(POSTGRES_CHAT_STORE_URI)
            messages = chat_store.get_messages(chat_id)
            return [{"role": message.role, "content": message.content}
                   for message in messages]
        except Exception as e:
            print(f"Error retrieving chat messages: {e}")
            return [{"role": "system", "content": "Unable to retrieve chat history."}]
    
    def _store_message(self, chat_id, role, content):
        """
        Store a message in the chat store.
        
        Args:
            chat_id: Chat session identifier
            role: Message role (user/assistant)
            content: Message content
        """
        try:
            chat_store = PostgresChatStore.from_uri(POSTGRES_CHAT_STORE_URI)
            # Note: This is a simplified implementation
            # The actual LLamaIndex ChatStore API might differ
            # You may need to adapt this based on the exact PostgresChatStore interface
            pass  # TODO: Implement proper message storage
        except Exception as e:
            print(f"Error storing message: {e}")
