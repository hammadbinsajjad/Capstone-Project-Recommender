import React from 'react';

import { Link, useLocation, useNavigate } from 'react-router-dom';
import { MessageSquare, History, LogOut, GraduationCap } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <GraduationCap className="h-8 w-8 text-blue-600" />
                <span className="font-bold text-xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  DTC Assistant
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <Link
                to="/chat"
                className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                  location.pathname === '/chat'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <MessageSquare className="h-4 w-4" />
                <span>Chat</span>
              </Link>

              <Link
                to="/history"
                className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                  location.pathname === '/history'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <History className="h-4 w-4" />
                <span>History</span>
              </Link>

              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-lg flex items-center space-x-2 text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {children}
      </main>
    </div>
  );
}
