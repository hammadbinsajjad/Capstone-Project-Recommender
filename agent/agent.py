"""
AI Agent using LLamaIndex FunctionAgent with Pinecone vector database integration.
This agent provides capstone project recommendations by retrieving relevant information 
from the Pinecone vector store and using an LLM to generate personalized suggestions.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add the parent directory to sys.path to import from ingestion module
sys.path.insert(0, str(Path(__file__).parent.parent))

from llama_index.core import VectorStoreIndex
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Import the existing Pinecone vector store configuration
from ingestion.readme_embedder.vector_store import load_vector_store
from ingestion.readme_embedder.config import EMBEDDINGS_MODEL_NAME


class CapstoneProjectAgent:
    """
    AI Agent for capstone project recommendations using LLamaIndex FunctionAgent
    with Pinecone vector database for retrieval.
    """
    
    def __init__(
        self,
        llm_model: str = "gpt-3.5-turbo",
        use_openai_embeddings: bool = False,
        max_retrieved_docs: int = 10
    ):
        """
        Initialize the Capstone Project Agent.
        
        Args:
            llm_model: The LLM model to use (default: gpt-3.5-turbo)
            use_openai_embeddings: Whether to use OpenAI embeddings (requires OPENAI_API_KEY)
            max_retrieved_docs: Maximum number of documents to retrieve from Pinecone
        """
        self.max_retrieved_docs = max_retrieved_docs
        
        # Initialize embeddings
        if use_openai_embeddings and os.getenv("OPENAI_API_KEY"):
            self.embeddings = OpenAIEmbedding()
            self.llm = OpenAI(model=llm_model)
        else:
            # Use HuggingFace embeddings as fallback (same as ingestion pipeline)
            self.embeddings = HuggingFaceEmbedding(model_name=EMBEDDINGS_MODEL_NAME)
            
            # For non-OpenAI LLM, we can use a mock or local model
            # In this case, we'll still try OpenAI but with better error handling
            try:
                self.llm = OpenAI(model=llm_model)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI LLM: {e}")
                print("Using mock LLM for demonstration. Please set OPENAI_API_KEY for full functionality.")
                from llama_index.core.llms.mock import MockLLM
                self.llm = MockLLM()
        
        # Set global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embeddings
        
        # Initialize Pinecone vector store
        self.vector_store = load_vector_store()
        self.index = VectorStoreIndex.from_vector_store(self.vector_store)
        
        # Create retriever
        self.retriever = self.index.as_retriever(similarity_top_k=max_retrieved_docs)
        
        # Initialize the FunctionAgent with tools
        self.agent = self._create_function_agent()
    
    def _create_function_agent(self) -> FunctionAgent:
        """Create and configure the FunctionAgent with retrieval tools."""
        
        # Define retrieval tool
        def retrieve_project_context(query: str) -> str:
            """
            Retrieve relevant project information from the vector database.
            
            Args:
                query: The search query to find relevant projects
                
            Returns:
                Formatted context with relevant project information
            """
            try:
                nodes = self.retriever.retrieve(query)
                if not nodes:
                    return "No relevant project information found."
                
                context_parts = []
                for i, node in enumerate(nodes[:self.max_retrieved_docs], 1):
                    content = node.node.text if hasattr(node.node, 'text') else str(node.node)
                    metadata = getattr(node.node, 'metadata', {})
                    
                    # Format the context with metadata if available
                    project_info = f"[Project {i}]\n"
                    if metadata:
                        if 'title' in metadata:
                            project_info += f"Title: {metadata['title']}\n"
                        if 'description' in metadata:
                            project_info += f"Description: {metadata['description']}\n"
                        if 'technologies' in metadata:
                            project_info += f"Technologies: {metadata['technologies']}\n"
                    
                    project_info += f"Content: {content[:500]}...\n"  # Limit content length
                    project_info += f"Relevance Score: {node.score:.3f}\n\n"
                    
                    context_parts.append(project_info)
                
                return "\n".join(context_parts)
                
            except Exception as e:
                return f"Error retrieving context: {str(e)}"
        
        def generate_project_recommendations(
            user_interests: str,
            skill_level: str = "intermediate",
            preferred_technologies: str = "",
            project_duration: str = "one semester"
        ) -> str:
            """
            Generate personalized capstone project recommendations.
            
            Args:
                user_interests: User's areas of interest
                skill_level: User's skill level (beginner, intermediate, advanced)
                preferred_technologies: Technologies the user wants to use
                project_duration: Expected project duration
                
            Returns:
                Formatted project recommendations
            """
            # Combine user inputs into a comprehensive query
            query_parts = [user_interests]
            if preferred_technologies:
                query_parts.append(f"technologies: {preferred_technologies}")
            
            search_query = " ".join(query_parts)
            
            # Retrieve relevant context
            context = retrieve_project_context(search_query)
            
            # Create a detailed prompt for recommendations
            prompt = f"""
            Based on the following project information and user requirements, provide 5 detailed capstone project recommendations:
            
            User Requirements:
            - Interests: {user_interests}
            - Skill Level: {skill_level}
            - Preferred Technologies: {preferred_technologies or 'No specific preference'}
            - Project Duration: {project_duration}
            
            Relevant Project Context:
            {context}
            
            Please provide 5 project recommendations with:
            1. Project Title
            2. Brief Description (2-3 sentences)
            3. Key Technologies/Tools
            4. Learning Outcomes
            5. Estimated Difficulty Level
            6. Suggested Dataset/Resources (if applicable)
            
            Format each recommendation clearly and make them diverse in scope and approach.
            """
            
            return prompt
        
        # Create function tools
        retrieval_tool = FunctionTool.from_defaults(
            fn=retrieve_project_context,
            name="retrieve_project_context",
            description="Search for relevant capstone project information from the database"
        )
        
        recommendation_tool = FunctionTool.from_defaults(
            fn=generate_project_recommendations,
            name="generate_project_recommendations", 
            description="Generate personalized capstone project recommendations based on user requirements"
        )
        
        # Create and return FunctionAgent
        agent = FunctionAgent.from_tools(
            tools=[retrieval_tool, recommendation_tool],
            llm=self.llm,
            verbose=True,
            system_prompt="""
            You are an expert capstone project advisor AI assistant. Your role is to help students 
            find suitable capstone project ideas based on their interests, skills, and requirements.
            
            Use the available tools to:
            1. Search for relevant project information from the database
            2. Generate personalized recommendations that match the user's criteria
            
            Always provide detailed, actionable advice and consider factors like:
            - User's technical skill level
            - Available time and resources
            - Learning objectives
            - Career goals
            - Feasibility of implementation
            
            Be encouraging and provide practical next steps for each recommendation.
            """
        )
        
        return agent
    
    def chat(self, message: str) -> str:
        """
        Chat with the agent to get capstone project recommendations.
        
        Args:
            message: User's message/query
            
        Returns:
            Agent's response with recommendations
        """
        try:
            response = self.agent.chat(message)
            return str(response)
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try rephrasing your question."
    
    def get_recommendations(
        self,
        interests: str,
        skill_level: str = "intermediate",
        technologies: str = "",
        duration: str = "one semester"
    ) -> str:
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
        query = f"""
        I need capstone project recommendations with the following requirements:
        - My interests: {interests}
        - My skill level: {skill_level}
        - Preferred technologies: {technologies if technologies else 'No specific preference'}
        - Project duration: {duration}
        
        Please provide detailed recommendations with clear explanations.
        """
        
        return self.chat(query)


# Convenience function to create an agent instance
def create_capstone_agent(**kwargs) -> CapstoneProjectAgent:
    """Create a CapstoneProjectAgent with default or custom configuration."""
    return CapstoneProjectAgent(**kwargs)


# Example usage and testing
if __name__ == "__main__":
    # Create the agent
    agent = create_capstone_agent()
    
    # Test with a sample query
    test_query = """
    I'm interested in machine learning and data science projects. 
    I have intermediate Python skills and would like to work on something 
    related to natural language processing or computer vision. 
    I prefer using PyTorch or TensorFlow.
    """
    
    print("Testing Capstone Project Agent...")
    print("=" * 50)
    print(f"Query: {test_query}")
    print("=" * 50)
    
    try:
        response = agent.chat(test_query)
        print("Agent Response:")
        print(response)
    except Exception as e:
        print(f"Error during testing: {e}")
        print("This might be due to missing API keys or vector store data.")