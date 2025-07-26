import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-xl font-bold">
              Project Management Assistant
            </Link>
            <div className="hidden md:flex space-x-6">
              <Link 
                to="/dashboard" 
                className="hover:text-blue-200 transition-colors"
              >
                Dashboard
              </Link>
              <Link 
                to="/projects" 
                className="hover:text-blue-200 transition-colors"
              >
                Projects
              </Link>
              <Link 
                to="/tasks" 
                className="hover:text-blue-200 transition-colors"
              >
                Tasks
              </Link>
              <Link 
                to="/teams" 
                className="hover:text-blue-200 transition-colors"
              >
                Teams
              </Link>
              <Link 
                to="/reports" 
                className="hover:text-blue-200 transition-colors"
              >
                Reports
              </Link>
              <Link 
                to="/ai-chat" 
                className="hover:text-blue-200 transition-colors"
              >
                AI Assistant
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm">
              Welcome, {user?.full_name || user?.username}
            </span>
            <button
              onClick={handleLogout}
              className="bg-blue-700 hover:bg-blue-800 px-3 py-1 rounded text-sm transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;