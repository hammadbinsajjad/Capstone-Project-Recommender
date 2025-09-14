#!/usr/bin/env python3
"""
Demonstration script for the Capstone Project AI Agent.
Shows various usage patterns and capabilities.
"""

import os
import sys
from pathlib import Path

# Add the current directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

def demo_basic_usage():
    """Demonstrate basic agent usage."""
    print("🚀 Capstone Project AI Agent Demo")
    print("=" * 50)
    
    # Import with error handling
    try:
        from agent import create_capstone_agent
        print("✅ Successfully imported agent")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test agent creation with error handling
    print("\n📦 Creating AI Agent...")
    try:
        # Set a test API key to avoid immediate failures
        os.environ.setdefault('PINECONE_API_KEY', 'test-key')
        
        agent = create_capstone_agent(
            use_openai_embeddings=False,  # Use HuggingFace embeddings by default
            max_retrieved_docs=5
        )
        print("✅ Agent created successfully!")
        
    except Exception as e:
        print(f"⚠️  Agent creation failed: {e}")
        print("This is expected without proper API keys and vector store data.")
        return
    
    # Test basic chat functionality
    print("\n💬 Testing chat functionality...")
    test_queries = [
        "What are some machine learning project ideas?",
        "I'm interested in web development projects using React",
        "Show me data science projects for healthcare"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        try:
            response = agent.chat(query)
            print(f"🤖 Response: {response[:200]}...")  # Truncate for demo
        except Exception as e:
            print(f"⚠️  Response generation failed: {e}")
    
    # Test structured recommendations
    print("\n📋 Testing structured recommendations...")
    try:
        recommendations = agent.get_recommendations(
            interests="artificial intelligence and robotics",
            skill_level="intermediate",
            technologies="Python, TensorFlow, ROS",
            duration="two semesters"
        )
        print(f"🎯 Recommendations: {recommendations[:200]}...")  # Truncate for demo
    except Exception as e:
        print(f"⚠️  Recommendation generation failed: {e}")


def demo_application_wrapper():
    """Demonstrate the application wrapper."""
    print("\n" + "=" * 50)
    print("🎯 Application Wrapper Demo")
    print("=" * 50)
    
    try:
        from agent import create_app
        
        config = {
            'use_openai_embeddings': False,
            'max_retrieved_docs': 5
        }
        
        # Set test API key
        os.environ.setdefault('PINECONE_API_KEY', 'test-key')
        
        app = create_app(config)
        print("✅ Application created successfully!")
        
        # Test batch processing
        test_requests = [
            {
                'id': 'req1',
                'interests': 'machine learning',
                'skill_level': 'beginner',
                'technologies': 'Python'
            },
            {
                'id': 'req2', 
                'message': 'What are some cybersecurity project ideas?'
            }
        ]
        
        print("\n📦 Testing batch processing...")
        results = app.batch_recommendations(test_requests)
        
        for req_id, response in results.items():
            print(f"📋 {req_id}: {response[:100]}...")
        
    except Exception as e:
        print(f"⚠️  Application demo failed: {e}")


def demo_backend_integration():
    """Demonstrate backend integration."""
    print("\n" + "=" * 50)
    print("🔗 Backend Integration Demo")
    print("=" * 50)
    
    try:
        from backend.chat.ai_agent import AIAgent
        
        print("✅ Backend AIAgent imported successfully")
        
        # Create agent instance
        agent = AIAgent(use_openai_embeddings=False)
        
        # Test response generation
        test_query = "I need capstone project ideas for computer science"
        print(f"\n🔍 Testing query: {test_query}")
        
        response = agent.generate_response(test_query, "test_chat_123")
        print(f"🤖 Response: {response}")
        
    except Exception as e:
        print(f"⚠️  Backend integration demo failed: {e}")


def show_usage_examples():
    """Show various usage examples."""
    print("\n" + "=" * 50)
    print("📚 Usage Examples")
    print("=" * 50)
    
    examples = [
        {
            "title": "Basic Chat",
            "code": '''
from agent import create_capstone_agent

agent = create_capstone_agent()
response = agent.chat("I need AI project ideas")
print(response)
            '''.strip()
        },
        {
            "title": "Structured Recommendations", 
            "code": '''
from agent import create_capstone_agent

agent = create_capstone_agent()
recommendations = agent.get_recommendations(
    interests="machine learning and healthcare",
    skill_level="advanced",
    technologies="Python, TensorFlow, Flask",
    duration="full academic year"
)
print(recommendations)
            '''.strip()
        },
        {
            "title": "Application Wrapper",
            "code": '''
from agent import create_app

app = create_app({
    'use_openai_embeddings': True,
    'max_retrieved_docs': 15
})

response = app.chat("Show me web development projects")
print(response)
            '''.strip()
        },
        {
            "title": "Interactive Session",
            "code": '''
from agent import create_app

app = create_app()
app.interactive_session()  # Starts CLI chat interface
            '''.strip()
        },
        {
            "title": "Backend Integration",
            "code": '''
from backend.chat.ai_agent import AIAgent

agent = AIAgent(use_openai_embeddings=False)
response = agent.generate_response(
    "Data science project ideas", 
    "chat_session_1"
)
print(response)
            '''.strip()
        }
    ]
    
    for example in examples:
        print(f"\n🔹 {example['title']}:")
        print(f"```python\n{example['code']}\n```")


def main():
    """Run the complete demonstration."""
    print("🎓 Capstone Project AI Agent - Complete Demonstration")
    print("🔬 This demo shows the agent functionality with and without API keys")
    
    # Run different demo sections
    demo_basic_usage()
    demo_application_wrapper() 
    demo_backend_integration()
    show_usage_examples()
    
    print("\n" + "=" * 60)
    print("🏁 Demo completed!")
    print("\n💡 To use the agent with full functionality:")
    print("   1. Set OPENAI_API_KEY environment variable")
    print("   2. Set PINECONE_API_KEY environment variable") 
    print("   3. Ensure your Pinecone index contains project data")
    print("   4. Run: python -m agent.application --interactive")
    print("\n📖 For more examples, see the documentation in the agent files.")


if __name__ == "__main__":
    main()