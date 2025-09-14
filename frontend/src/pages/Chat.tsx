import { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { SyncLoader } from 'react-spinners';

import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Layout from '../components/Layout';
import { Message } from '../types';
import { chatMessages, sendMessage } from '../utils/api';

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isPageLoading, setIsPageLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatId = Number(useParams<{ chatId: string }>().chatId);


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const fetchChatMessages = async () => {
      try {
        const messages = await chatMessages(chatId);
        setMessages(messages);
      } catch (error) {
        console.error("Error fetching chat messages:", error);
        setMessages([]);
      } finally {
        setIsPageLoading(false);
      }
    };

    fetchChatMessages();
  }, [chatId]);

  const handleSendMessage = async (query: string) => {
    const userMessage: Message = {
      id: messages.length,
      content: query,
      isUser: true,
    };

    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    const response = await sendMessage(chatId, query);

    if (response) {
      const ai_message: Message = {
        id: messages.length,
        content: response,
        isUser: false,
      };

      setMessages(previousMessages => [...previousMessages, ai_message]);
    }

    setIsLoading(false);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  if (isPageLoading) {
    return (
      <div className="grid place-items-center min-h-screen rotate-90">
        <SyncLoader color="#2563EB" />
      </div>
    );
  }

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
