"""
Tests for the Capstone Project AI Agent.
Basic functionality tests that work without external API dependencies.
"""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_agent_imports():
    """Test that all required imports work correctly."""
    try:
        from agent.agent import CapstoneProjectAgent, create_capstone_agent
        from agent.application import CapstoneAgentApp, create_app
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_agent_structure():
    """Test the basic structure of the agent class."""
    from agent.agent import CapstoneProjectAgent
    
    # Check that the class has expected methods
    expected_methods = ['chat', 'get_recommendations', '_create_function_agent']
    
    for method in expected_methods:
        if not hasattr(CapstoneProjectAgent, method):
            print(f"❌ Missing method: {method}")
            return False
    
    print("✅ Agent structure validation passed")
    return True


def test_application_structure():
    """Test the basic structure of the application class."""
    from agent.application import CapstoneAgentApp
    
    # Check that the class has expected methods
    expected_methods = ['chat', 'get_recommendations', 'interactive_session', 'batch_recommendations']
    
    for method in expected_methods:
        if not hasattr(CapstoneAgentApp, method):
            print(f"❌ Missing method: {method}")
            return False
    
    print("✅ Application structure validation passed")
    return True


def test_mock_agent_creation():
    """Test agent creation with mocked dependencies."""
    from agent.agent import CapstoneProjectAgent
    
    # Mock the vector store and related components
    with patch('agent.agent.load_vector_store') as mock_vector_store, \
         patch('agent.agent.VectorStoreIndex') as mock_index, \
         patch('agent.agent.HuggingFaceEmbedding') as mock_embedding, \
         patch('agent.agent.OpenAI') as mock_llm:
        
        # Setup mocks
        mock_vector_store.return_value = Mock()
        mock_index_instance = Mock()
        mock_index.from_vector_store.return_value = mock_index_instance
        mock_retriever = Mock()
        mock_index_instance.as_retriever.return_value = mock_retriever
        mock_embedding_instance = Mock()
        mock_embedding.return_value = mock_embedding_instance
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        with patch('agent.agent.FunctionAgent') as mock_function_agent:
            mock_agent_instance = Mock()
            mock_function_agent.from_tools.return_value = mock_agent_instance
            
            try:
                agent = CapstoneProjectAgent()
                
                # Verify initialization
                assert agent.max_retrieved_docs == 10
                assert agent.vector_store is not None
                assert agent.index is not None
                assert agent.retriever is not None
                assert agent.agent is not None
                
                print("✅ Mock agent creation successful")
                return True
                
            except Exception as e:
                print(f"❌ Mock agent creation failed: {e}")
                return False


def test_chat_error_handling():
    """Test error handling in chat method."""
    from agent.agent import CapstoneProjectAgent
    
    # Mock the vector store and related components
    with patch('agent.agent.load_vector_store'), \
         patch('agent.agent.VectorStoreIndex'), \
         patch('agent.agent.HuggingFaceEmbedding'), \
         patch('agent.agent.OpenAI'), \
         patch('agent.agent.FunctionAgent'):
        
        agent = CapstoneProjectAgent()
        
        # Mock the agent.chat to raise an exception
        agent.agent = Mock()
        agent.agent.chat.side_effect = Exception("Test error")
        
        result = agent.chat("test message")
        
        assert "Sorry, I encountered an error" in result
        assert "Test error" in result
        
        print("✅ Error handling test passed")
        return True


def test_application_config():
    """Test application configuration."""
    from agent.application import CapstoneAgentApp
    
    config = {
        'llm_model': 'gpt-4',
        'use_openai_embeddings': True,
        'max_retrieved_docs': 15
    }
    
    with patch('agent.application.create_capstone_agent') as mock_create:
        mock_agent = Mock()
        mock_create.return_value = mock_agent
        
        try:
            app = CapstoneAgentApp(config)
            
            # Verify configuration was passed
            mock_create.assert_called_once_with(
                llm_model='gpt-4',
                use_openai_embeddings=True,
                max_retrieved_docs=15
            )
            
            print("✅ Application configuration test passed")
            return True
            
        except Exception as e:
            print(f"❌ Application configuration test failed: {e}")
            return False


def run_all_tests():
    """Run all tests and return overall result."""
    print("🧪 Running Capstone Project Agent Tests")
    print("=" * 50)
    
    tests = [
        test_agent_imports,
        test_agent_structure,
        test_application_structure,
        test_mock_agent_creation,
        test_chat_error_handling,
        test_application_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. This may be due to missing dependencies or API keys.")
        return False


if __name__ == "__main__":
    run_all_tests()