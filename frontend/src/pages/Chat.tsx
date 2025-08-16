import React, { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Layout from '../components/Layout';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import { Message } from '../types';
import { getCurrentChat } from '../utils/mockData';

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>(getCurrentChat().messages);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // TODO: Replace with actual API call when backend is ready
  const simulateAIResponse = (userMessage: string): string => {
    const responses = [
      `Great question about "${userMessage.slice(0, 50)}...". Here are some ideas based on what you're looking for:\n\n1. **Project Idea 1** - A comprehensive solution that addresses real-world problems\n2. **Project Idea 2** - An innovative approach using modern technologies\n3. **Project Idea 3** - A scalable system with practical applications\n\nWhich of these directions interests you most? I can provide more specific details and requirements.`,
      
      `That's an interesting direction! For your capstone project, consider these aspects:\n\n**Technical Requirements:**\n- Choose technologies that align with course objectives\n- Ensure the scope is manageable within the timeframe\n- Include proper documentation and testing\n\n**Business Value:**\n- Solve a real problem you're passionate about\n- Demonstrate practical skills employers value\n- Show impact with metrics and results\n\nWould you like me to dive deeper into any of these areas?`,
      
      `Based on your message about "${userMessage.slice(0, 30)}...", I'd recommend focusing on:\n\n🎯 **Core Focus:** Start with a clear problem statement\n📊 **Data Strategy:** Identify your data sources and quality requirements\n🛠️ **Tech Stack:** Choose tools that match your experience level\n📈 **Success Metrics:** Define how you'll measure project success\n\nWhat specific area would you like to explore further?`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: uuidv4(),
      content,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // TODO: Replace with actual API call when backend is ready
    // Example: const response = await fetch('/api/chat', { ... });
    
    // Simulate API delay
    setTimeout(() => {
      const aiResponse: Message = {
        id: uuidv4(),
        content: simulateAIResponse(content),
        isUser: false,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000 + Math.random() * 1000);
  };

  return (
    <Layout>
      <div className="h-[calc(100vh-120px)] bg-white rounded-xl shadow-lg flex flex-col overflow-hidden">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4">
          <h1 className="text-xl font-semibold">Capstone Project Assistant</h1>
          <p className="text-blue-100 text-sm">Get personalized project ideas and guidance for your DataTalks course</p>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(message => (
            <ChatMessage key={message.id} message={message} />
          ))}
          
          {isLoading && (
            <div className="flex gap-4 mb-6">
              <div className="flex gap-3 max-w-[80%]">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-blue-500 flex items-center justify-center">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </Layout>
  );
}