export interface Message {
  id: number;
  content: string;
  isUser: boolean;
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
