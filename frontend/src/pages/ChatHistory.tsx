import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MessageSquare, Clock, ChevronRight } from 'lucide-react';

import Layout from '../components/Layout';
import { chatHistory } from '../utils/api';
import { formatDate, isLoggedIn } from '../utils/helpers';


interface Chat {
  id: number;
  title: string;
  queryPreview: string;
  lastUpdated: string;
  messageCount: number;
}

export default function ChatHistory() {
  const [chats, setChats] = useState<Chat[]>([]);
  const navigate = useNavigate();

  if (!isLoggedIn()) {
    navigate('/login');
  }

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const chats = await chatHistory();
        setChats(chats);
      } catch (error) {
        console.error("Error fetching chat history:", error);
        setChats([]);
      }
    };

    fetchChatHistory();
  }, []);

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
            Chat History
          </h1>
          <p className="text-gray-600">Review and continue your previous conversations</p>
        </div>

        <div className="space-y-4">
          {chats.map((chat) => (
            <Link
              key={chat.id}
              to={`/chat/${chat.id}`}
              className="block bg-white rounded-xl border border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md transition-all duration-200 p-6 group"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-100 to-purple-100 rounded-xl flex items-center justify-center">
                    <MessageSquare className="h-6 w-6 text-blue-600" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
                      {chat.title.slice(0, 50)}
                    </h3>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                      {chat.queryPreview}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatDate(chat.lastUpdated)}
                      </div>
                      <span>{chat.messageCount} messages</span>
                    </div>
                  </div>
                </div>

                <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-blue-600 transition-colors flex-shrink-0" />
              </div>
            </Link>
          ))}
        </div>

        {chats.length !== 0 && (<div className="mt-8 text-center">
            <Link
              to="/chat"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-6 py-3 rounded-xl transition-all duration-200 font-medium"
            >
              <MessageSquare className="h-4 w-4" />
              Start New Chat
            </Link>
          </div>
      )}

        {chats.length === 0 && (
          <div className="text-center py-12">
            <MessageSquare className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No chat history yet</h3>
            <p className="text-gray-600 mb-6">Start your first conversation to see it appear here</p>
            <Link
              to="/chat"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-6 py-3 rounded-xl transition-all duration-200 font-medium"
            >
              <MessageSquare className="h-4 w-4" />
              Start Chatting
            </Link>
          </div>
        )}
      </div>
    </Layout>
  );
}
