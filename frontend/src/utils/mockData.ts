import { Chat, Message } from '../types';

export const mockChats: Chat[] = [
  {
    id: '1',
    title: 'ML Engineering Capstone Ideas',
    lastMessage: new Date('2024-01-15T10:30:00'),
    preview: 'Looking for machine learning project ideas...',
    messages: [
      {
        id: '1',
        content: 'Hi! I\'m looking for some capstone project ideas for the ML Engineering course. Can you help?',
        isUser: true,
        timestamp: new Date('2024-01-15T10:30:00'),
      },
      {
        id: '2',
        content: 'Absolutely! Here are some great ML Engineering capstone project ideas:\n\n1. **Real-time Fraud Detection System** - Build an ML pipeline that detects fraudulent transactions in real-time\n2. **Recommendation Engine** - Create a personalized recommendation system for e-commerce or content\n3. **MLOps Pipeline** - Develop a complete MLOps solution with model versioning, monitoring, and automated retraining\n\nWhich area interests you most?',
        isUser: false,
        timestamp: new Date('2024-01-15T10:30:30'),
      }
    ]
  },
  {
    id: '2',
    title: 'Data Engineering Project Scope',
    lastMessage: new Date('2024-01-14T15:45:00'),
    preview: 'Need help scoping a data pipeline project...',
    messages: [
      {
        id: '3',
        content: 'I want to build a data engineering project but I\'m not sure about the scope. Any suggestions?',
        isUser: true,
        timestamp: new Date('2024-01-14T15:45:00'),
      },
      {
        id: '4',
        content: 'Great question! For a data engineering capstone, consider these project scopes:\n\n**Beginner-friendly:**\n- ETL pipeline with batch processing\n- Data warehouse design and implementation\n\n**Intermediate:**\n- Real-time streaming data pipeline\n- Data lake architecture with multiple sources\n\n**Advanced:**\n- Multi-cloud data platform\n- Event-driven data architecture\n\nWhat\'s your experience level with data engineering tools?',
        isUser: false,
        timestamp: new Date('2024-01-14T15:45:30'),
      }
    ]
  },
  {
    id: '3',
    title: 'Analytics Project Ideas',
    lastMessage: new Date('2024-01-13T09:15:00'),
    preview: 'Exploring analytics capstone options...',
    messages: [
      {
        id: '5',
        content: 'What are some good analytics capstone project ideas?',
        isUser: true,
        timestamp: new Date('2024-01-13T09:15:00'),
      }
    ]
  }
];

export const getCurrentChat = (): Chat => ({
  id: 'current',
  title: 'New Chat',
  lastMessage: new Date(),
  preview: 'Start a new conversation...',
  messages: [
    {
      id: 'welcome',
      content: 'Hello! I\'m your DataTalksClub capstone project assistant. I\'m here to help you brainstorm and develop ideas for your capstone project across any of our courses - ML Engineering, Data Engineering, Analytics Engineering, and more!\n\nWhat course are you taking, and what kind of project are you thinking about?',
      isUser: false,
      timestamp: new Date(),
    }
  ]
});