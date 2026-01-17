/**
 * Navbar Component
 * Main navigation with authentication and cart count
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { cartAPI } from '../services/api';

function Navbar({ currentView, onNavigate, onShowLogin }) {
  const { user, isAuthenticated, logout } = useAuth();
  const [cartCount, setCartCount] = useState(0);
  const [showUserMenu, setShowUserMenu] = useState(false);

  useEffect(() => {
    if (isAuthenticated()) {
      loadCartCount();
      // Poll cart count every 30 seconds
      const interval = setInterval(loadCartCount, 30000);
      return () => clearInterval(interval);
    } else {
      setCartCount(0);
    }
  }, [isAuthenticated()]);

  const loadCartCount = async () => {
    try {
      const data = await cartAPI.getCartCount();
      setCartCount(data.count || 0);
    } catch (err) {
      console.error('Failed to load cart count:', err);
    }
  };

  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
    setCartCount(0);
    onNavigate('products');
  };

  const handleCartClick = () => {
    if (!isAuthenticated()) {
      onShowLogin();
      return;
    }
    onNavigate('cart');
  };

  return (
    <nav className="navbar">
      <div className="container navbar-content">
        {/* Logo */}
        <div className="navbar-brand" onClick={() => onNavigate('products')}>
          <span className="logo-icon">🛍️</span>
          <span className="logo-text">E-Commerce</span>
          <span className="logo-badge">Microservices</span>
        </div>

        {/* Navigation Links */}
        <div className="navbar-links">
          <button
            className={`nav-link ${currentView === 'products' ? 'active' : ''}`}
            onClick={() => onNavigate('products')}
          >
            🏠 Products
          </button>
          
          <button
            className={`nav-link cart-link ${currentView === 'cart' ? 'active' : ''}`}
            onClick={handleCartClick}
          >
            🛒 Cart
            {cartCount > 0 && (
              <span className="cart-badge">{cartCount}</span>
            )}
          </button>
        </div>

        {/* User Section */}
        <div className="navbar-user">
          {isAuthenticated() ? (
            <div className="user-menu">
              <button 
                className="user-button"
                onClick={() => setShowUserMenu(!showUserMenu)}
              >
                <span className="user-icon">👤</span>
                <span className="user-name">{user?.name || 'User'}</span>
                <span className="dropdown-arrow">{showUserMenu ? '▲' : '▼'}</span>
              </button>

              {showUserMenu && (
                <div className="user-dropdown">
                  <div className="user-dropdown-header">
                    <div className="user-dropdown-name">{user?.name}</div>
                    <div className="user-dropdown-email">{user?.email}</div>
                  </div>
                  <hr />
                  <button 
                    className="user-dropdown-item"
                    onClick={() => {
                      onNavigate('cart');
                      setShowUserMenu(false);
                    }}
                  >
                    🛒 My Cart {cartCount > 0 && `(${cartCount})`}
                  </button>
                  <button 
                    className="user-dropdown-item logout"
                    onClick={handleLogout}
                  >
                    🚪 Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button className="login-button" onClick={onShowLogin}>
              🔐 Login
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;