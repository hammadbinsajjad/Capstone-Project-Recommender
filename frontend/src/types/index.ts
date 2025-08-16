export interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  lastMessage: Date;
  preview: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
}