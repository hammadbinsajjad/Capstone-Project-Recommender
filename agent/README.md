# Capstone Project AI Agent

An intelligent AI Agent built with LLamaIndex FunctionAgent and Pinecone vector database integration for providing personalized capstone project recommendations.

## 🚀 Features

- **LLamaIndex FunctionAgent**: Uses advanced function-calling capabilities for tool integration
- **Pinecone Vector Database**: Efficient similarity search and retrieval of project information
- **Flexible LLM Support**: Works with OpenAI models or HuggingFace embeddings
- **Django Backend Integration**: Seamlessly integrates with existing Django chat system
- **Interactive CLI**: Command-line interface for easy testing and interaction
- **Batch Processing**: Handle multiple recommendation requests simultaneously
- **Error Handling**: Robust error handling and fallback mechanisms

## 📁 Project Structure

```
agent/
├── __init__.py              # Package initialization
├── agent.py                 # Core CapstoneProjectAgent implementation
├── application.py           # Application wrapper and CLI interface
└── test_agent.py           # Unit tests and validation

backend/chat/
└── ai_agent.py             # Updated AIAgent class with LLamaIndex integration

ingestion/readme_embedder/
├── vector_store.py         # Pinecone vector store configuration (updated)
└── config.py              # Configuration settings

demo.py                     # Demonstration script
```

## 🔧 Installation & Setup

### Prerequisites

1. **Python 3.8+**
2. **API Keys** (at least one required):
   - `OPENAI_API_KEY` - For OpenAI models and embeddings
   - `PINECONE_API_KEY` - For Pinecone vector database
3. **Internet Connection** - For downloading HuggingFace models

### Dependencies

Install the required packages:

```bash
cd ingestion
pip install -r requirements.txt
pip install google-generativeai  # Optional for Gemini integration
```

### Environment Variables

Set up your environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export PINECONE_API_KEY="your_pinecone_api_key"
```

Or create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## 🎯 Usage

### Basic Usage

```python
from agent import create_capstone_agent

# Create the agent
agent = create_capstone_agent(
    use_openai_embeddings=True,  # Set to False for HuggingFace
    max_retrieved_docs=10
)

# Chat with the agent
response = agent.chat("I need machine learning project ideas for healthcare")
print(response)

# Get structured recommendations
recommendations = agent.get_recommendations(
    interests="artificial intelligence and robotics",
    skill_level="intermediate", 
    technologies="Python, TensorFlow, ROS",
    duration="two semesters"
)
print(recommendations)
```

### Application Wrapper

```python
from agent import create_app

# Create application with configuration
config = {
    'use_openai_embeddings': True,
    'max_retrieved_docs': 15
}
app = create_app(config)

# Single query
response = app.chat("Show me web development projects")

# Batch processing
requests = [
    {
        'id': 'student1',
        'interests': 'machine learning',
        'skill_level': 'beginner'
    },
    {
        'id': 'student2', 
        'message': 'I want cybersecurity projects'
    }
]
results = app.batch_recommendations(requests)
```

### Interactive CLI

```bash
# Start interactive session
python -m agent.application --interactive

# Single query
python -m agent.application --query "I need data science project ideas"

# Structured request
python -m agent.application \
    --interests "machine learning and computer vision" \
    --skill-level "advanced" \
    --technologies "Python, PyTorch, OpenCV" \
    --duration "full academic year"
```

### Django Backend Integration

The `AIAgent` class in `backend/chat/ai_agent.py` has been updated to use the LLamaIndex implementation:

```python
from backend.chat.ai_agent import AIAgent

# Create agent instance
agent = AIAgent(use_openai_embeddings=False)

# Generate response (integrates with Django chat system)
response = agent.generate_response(
    "I need capstone project ideas for computer science",
    chat_id="session_123"
)

# Get structured recommendations
recommendations = agent.get_structured_recommendations(
    interests="web development",
    skill_level="intermediate",
    technologies="React, Node.js, MongoDB"
)
```

## 🛠️ Architecture

### Core Components

1. **CapstoneProjectAgent**: Main agent class using LLamaIndex FunctionAgent
2. **Function Tools**: 
   - `retrieve_project_context`: Searches Pinecone vector database
   - `generate_project_recommendations`: Creates personalized recommendations
3. **Vector Store Integration**: Uses existing Pinecone configuration
4. **LLM Integration**: Supports OpenAI and HuggingFace models

### Data Flow

1. User submits query/requirements
2. Agent determines which tools to use
3. `retrieve_project_context` searches vector database
4. Retrieved context is processed and formatted
5. LLM generates personalized recommendations
6. Response is returned to user

## 🧪 Testing

Run the test suite:

```bash
python agent/test_agent.py
```

Run the demonstration:

```bash
python demo.py
```

## 🔍 Configuration Options

### Agent Configuration

- `llm_model`: OpenAI model to use (default: "gpt-3.5-turbo")
- `use_openai_embeddings`: Use OpenAI vs HuggingFace embeddings
- `max_retrieved_docs`: Number of documents to retrieve from Pinecone

### Vector Store Configuration

Settings in `ingestion/readme_embedder/config.py`:
- `INDEX_NAME`: Pinecone index name
- `EMBEDDING_DIMENSION`: Vector dimension (1024 for HuggingFace model)
- `EMBEDDINGS_MODEL_NAME`: HuggingFace model name

## 📊 Error Handling & Fallbacks

The implementation includes robust error handling:

1. **Missing API Keys**: Falls back to MockLLM for testing
2. **Network Issues**: Graceful degradation with informative messages
3. **Vector Store Errors**: Clear error messages and retry logic
4. **Backend Integration**: Fallback to basic responses when agent unavailable

## 🚦 Limitations & Requirements

### Current Limitations

1. Requires internet connection for HuggingFace model downloads
2. Depends on Pinecone vector store containing project data
3. OpenAI API usage incurs costs
4. Performance depends on vector store index quality

### Future Enhancements

1. Local embedding model caching
2. Alternative vector store support (Chroma, Weaviate)
3. Additional LLM provider support (Anthropic, Cohere)
4. Enhanced memory management
5. Project similarity scoring

## 🤝 Integration Points

### Existing System Integration

- **Pinecone Vector Store**: Reuses existing `ingestion/readme_embedder/vector_store.py`
- **Django Backend**: Integrates with `backend/chat/ai_agent.py`
- **Configuration**: Uses `ingestion/readme_embedder/config.py`
- **Chat Storage**: Integrates with PostgreSQL chat store

### API Endpoints (Django)

The updated `AIAgent` class can be used in Django views:

```python
from backend.chat.ai_agent import AIAgent

def chat_api(request):
    agent = AIAgent()
    response = agent.generate_response(
        request.data['message'],
        request.data['chat_id']
    )
    return JsonResponse({'response': response})
```

## 📝 License

This implementation follows the same license as the parent project.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Errors**: Check environment variables are set correctly
3. **Network Errors**: Verify internet connection for model downloads
4. **Pinecone Errors**: Confirm API key and index exist
5. **Memory Issues**: Reduce `max_retrieved_docs` for large datasets

### Debug Mode

Enable verbose logging:

```python
agent = create_capstone_agent()
agent.agent.verbose = True  # Enable detailed logging
```

For additional help, check the demo script and test files for working examples.