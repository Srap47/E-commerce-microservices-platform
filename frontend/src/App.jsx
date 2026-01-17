/**
 * Main App Component
 * Handles routing and layout
 */
import { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './components/Login';
import ProductList from './components/ProductList';
import Cart from './components/Cart';
import './App.css';

function AppContent() {
  const { isAuthenticated } = useAuth();
  const [currentView, setCurrentView] = useState('products'); // 'products' or 'cart'
  const [showLogin, setShowLogin] = useState(false);

  return (
    <div className="app">
      <Navbar
        currentView={currentView}
        onNavigate={setCurrentView}
        onShowLogin={() => setShowLogin(true)}
      />

      <main className="main-content">
        {showLogin && !isAuthenticated() && (
          <Login onClose={() => setShowLogin(false)} />
        )}

        {currentView === 'products' && (
          <ProductList />
        )}

        {currentView === 'cart' && (
          <Cart />
        )}
      </main>

      <footer className="footer">
        <div className="container">
          <p>&copy; 2026 E-Commerce Microservices Platform. Built with Python FastAPI + React.</p>
          <p className="footer-note">
            Demo Assignment - Microservices Architecture with API Gateway
          </p>
        </div>
      </footer>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;