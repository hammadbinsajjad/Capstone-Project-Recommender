import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className={`flex gap-4 mb-6 animate-fade-in ${message.isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex gap-3 max-w-[80%] ${message.isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          message.isUser
            ? 'bg-gradient-to-r from-purple-500 to-purple-500'
            : 'bg-gradient-to-r from-blue-500 to-blue-500'
        }`}>
          {message.isUser ? (
            <User className="h-4 w-4 text-white" />
          ) : (
            <Bot className="h-4 w-4 text-white" />
          )}
        </div>

        <div className={`rounded-2xl px-4 py-3 ${
          message.isUser
            ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
            : 'bg-white border border-gray-200 text-gray-800 shadow-sm'
        }`}>
          <ReactMarkdown
            components={{
              p: (props) => (
                <p className="whitespace-pre-wrap leading-relaxed" {...props} />
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
          <p className={`text-xs mt-2 ${
            message.isUser ? 'text-blue-100' : 'text-gray-500'
          }`}>
          </p>
        </div>
      </div>
    </div>
  );
}
