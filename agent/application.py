"""
Application wrapper for the Capstone Project AI Agent.
Provides easy-to-use interfaces for integrating the agent into web applications,
APIs, or command-line interfaces.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to sys.path to import the agent
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.agent import CapstoneProjectAgent, create_capstone_agent


class CapstoneAgentApp:
    """
    Application wrapper for the Capstone Project AI Agent.
    Provides convenient methods for different usage patterns.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the application with optional configuration.
        
        Args:
            config: Dictionary containing agent configuration options
        """
        self.config = config or {}
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the AI agent with the provided configuration."""
        try:
            # Extract configuration parameters
            llm_model = self.config.get('llm_model', 'gpt-3.5-turbo')
            use_openai_embeddings = self.config.get('use_openai_embeddings', False)
            max_retrieved_docs = self.config.get('max_retrieved_docs', 10)
            
            # Create the agent
            self.agent = create_capstone_agent(
                llm_model=llm_model,
                use_openai_embeddings=use_openai_embeddings,
                max_retrieved_docs=max_retrieved_docs
            )
            
            print("✅ Capstone Project Agent initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            print("Please check your configuration and ensure all dependencies are installed.")
            raise
    
    def chat(self, message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: User's message or query
            
        Returns:
            Agent's response
        """
        if not self.agent:
            return "Error: Agent not initialized properly."
        
        return self.agent.chat(message)
    
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
        if not self.agent:
            return "Error: Agent not initialized properly."
        
        return self.agent.get_recommendations(
            interests=interests,
            skill_level=skill_level,
            technologies=technologies,
            duration=duration
        )
    
    def interactive_session(self):
        """Run an interactive chat session with the agent."""
        print("🤖 Welcome to the Capstone Project Recommendation Agent!")
        print("Type 'quit', 'exit', or 'bye' to end the session.")
        print("Type 'help' for usage examples.")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for using the Capstone Project Agent! Good luck with your project!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if not user_input:
                    print("Please enter a message or type 'help' for examples.")
                    continue
                
                print("\n🤔 Agent is thinking...")
                response = self.chat(user_input)
                print(f"\n🎯 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different query.")
    
    def _show_help(self):
        """Display help information and usage examples."""
        help_text = """
🔍 Usage Examples:

1. General project ideas:
   "I need capstone project ideas for computer science"

2. Specific interests:
   "I'm interested in machine learning and healthcare applications"

3. Technology preferences:
   "I want to build a web application using React and Python"

4. Structured request:
   "My interests: AI and robotics
    My skill level: advanced
    Preferred technologies: Python, ROS, TensorFlow
    Project duration: full academic year"

5. Specific domain:
   "Show me projects related to cybersecurity and blockchain"

💡 Tips:
- Be specific about your interests and requirements
- Mention your skill level (beginner/intermediate/advanced)
- Include preferred programming languages or frameworks
- Specify any constraints (time, resources, etc.)
        """
        print(help_text)
    
    def batch_recommendations(self, requests: list) -> Dict[str, str]:
        """
        Process multiple recommendation requests at once.
        
        Args:
            requests: List of dictionaries containing request parameters
            
        Returns:
            Dictionary mapping request IDs to responses
        """
        results = {}
        
        for i, request in enumerate(requests):
            request_id = request.get('id', f'request_{i+1}')
            
            try:
                if 'message' in request:
                    # Direct chat message
                    response = self.chat(request['message'])
                else:
                    # Structured recommendation request
                    response = self.get_recommendations(
                        interests=request.get('interests', ''),
                        skill_level=request.get('skill_level', 'intermediate'),
                        technologies=request.get('technologies', ''),
                        duration=request.get('duration', 'one semester')
                    )
                
                results[request_id] = response
                
            except Exception as e:
                results[request_id] = f"Error processing request: {e}"
        
        return results


def create_app(config: Optional[Dict[str, Any]] = None) -> CapstoneAgentApp:
    """
    Create a CapstoneAgentApp instance with optional configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Initialized CapstoneAgentApp instance
    """
    return CapstoneAgentApp(config)


def main():
    """Command-line interface for the Capstone Project Agent."""
    parser = argparse.ArgumentParser(
        description="Capstone Project AI Agent - Get personalized project recommendations"
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start interactive chat session'
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Single query to process'
    )
    
    parser.add_argument(
        '--interests',
        type=str,
        help='Your areas of interest'
    )
    
    parser.add_argument(
        '--skill-level',
        choices=['beginner', 'intermediate', 'advanced'],
        default='intermediate',
        help='Your technical skill level'
    )
    
    parser.add_argument(
        '--technologies',
        type=str,
        default='',
        help='Preferred technologies or frameworks'
    )
    
    parser.add_argument(
        '--duration',
        type=str,
        default='one semester',
        help='Project duration'
    )
    
    parser.add_argument(
        '--use-openai-embeddings',
        action='store_true',
        help='Use OpenAI embeddings (requires OPENAI_API_KEY)'
    )
    
    args = parser.parse_args()
    
    # Configure the agent
    config = {
        'use_openai_embeddings': args.use_openai_embeddings,
        'max_retrieved_docs': 10
    }
    
    try:
        app = create_app(config)
        
        if args.interactive:
            app.interactive_session()
        
        elif args.query:
            print(f"\n🤔 Processing query: {args.query}")
            response = app.chat(args.query)
            print(f"\n🎯 Response:\n{response}")
        
        elif args.interests:
            print("\n🤔 Generating personalized recommendations...")
            response = app.get_recommendations(
                interests=args.interests,
                skill_level=args.skill_level,
                technologies=args.technologies,
                duration=args.duration
            )
            print(f"\n🎯 Recommendations:\n{response}")
        
        else:
            # Default to interactive mode
            app.interactive_session()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()