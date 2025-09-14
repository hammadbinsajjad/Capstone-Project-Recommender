import React, { useState, useEffect } from 'react';

import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Chat from './pages/Chat';
import ChatHistory from './pages/ChatHistory';
import Login from './pages/Login';
import Register from './pages/Register';
import { isLoggedIn } from './utils/helpers';
import { SyncLoader } from 'react-spinners';
import { chatMessages } from './utils/api';


interface PrivateRouteProps {
  isAuthenticated: boolean;
  children: React.ReactNode;
}


const PrivateRoute = ({ isAuthenticated, children }: PrivateRouteProps) => {
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    const checkAuth = async () => {
      setIsAuthenticated(await isLoggedIn());
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return (
      <div className="grid place-items-center min-h-screen rotate-90">
        <SyncLoader color="#2563EB" />
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register setIsAuthenticated={setIsAuthenticated} />} />
          <Route
            path="/chat"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <Chat />
              </PrivateRoute>
            }
          />
          <Route
            path="/chat/:chatId"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <Chat />
              </PrivateRoute>
            }
          />
          <Route
            path="/history"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <ChatHistory />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/chat" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
