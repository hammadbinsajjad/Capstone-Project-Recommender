"""
Capstone Project AI Agent Package

This package provides an AI Agent using LLamaIndex FunctionAgent 
with Pinecone vector database integration for capstone project recommendations.
"""

from .agent import CapstoneProjectAgent, create_capstone_agent
from .application import CapstoneAgentApp, create_app

__all__ = [
    'CapstoneProjectAgent',
    'create_capstone_agent', 
    'CapstoneAgentApp',
    'create_app'
]

__version__ = '1.0.0'