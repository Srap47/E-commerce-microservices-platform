/**
 * Login Component
 * Modal login form with demo credentials display
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';

function Login({ onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [demoUsers, setDemoUsers] = useState([]);
  const [showDemoUsers, setShowDemoUsers] = useState(false);
  const { login } = useAuth();

  useEffect(() => {
    loadDemoUsers();
  }, []);

  const loadDemoUsers = async () => {
    try {
      const data = await authAPI.getDemoUsers();
      setDemoUsers(data.demo_users || []);
    } catch (err) {
      console.error('Failed to load demo users:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(email, password);
      
      if (result.success) {
        // Close modal on success
        onClose();
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (demoEmail, demoPassword) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setShowDemoUsers(false);
  };

  const handleBackdropClick = (e) => {
    if (e.target.className === 'modal-backdrop') {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content login-modal">
        <div className="modal-header">
          <h2>🔐 Login</h2>
          <button 
            className="close-btn" 
            onClick={onClose}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="demo@example.com"
                required
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            <button 
              type="submit" 
              className="login-btn"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-small"></span> Logging in...
                </>
              ) : (
                'Login'
              )}
            </button>
          </form>

          <div className="divider">
            <span>OR</span>
          </div>

          <button
            className="demo-users-toggle"
            onClick={() => setShowDemoUsers(!showDemoUsers)}
          >
            {showDemoUsers ? '▼' : '▶'} Use Demo Credentials
          </button>

          {showDemoUsers && demoUsers.length > 0 && (
            <div className="demo-users-list">
              <p className="demo-note">
                Click any account to auto-fill credentials:
              </p>
              {demoUsers.map((user, index) => (
                <div 
                  key={index} 
                  className="demo-user-item"
                  onClick={() => handleDemoLogin(user.email, getDemoPassword(user.email))}
                >
                  <div className="demo-user-icon">👤</div>
                  <div className="demo-user-info">
                    <div className="demo-user-name">{user.name}</div>
                    <div className="demo-user-email">{user.email}</div>
                  </div>
                  <div className="demo-user-arrow">→</div>
                </div>
              ))}
            </div>
          )}

          {showDemoUsers && demoUsers.length === 0 && (
            <div className="demo-credentials">
              <h4>Demo Accounts:</h4>
              <div className="demo-account">
                <div><strong>Email:</strong> demo@example.com</div>
                <div><strong>Password:</strong> demo123</div>
              </div>
              <div className="demo-account">
                <div><strong>Email:</strong> john@example.com</div>
                <div><strong>Password:</strong> password123</div>
              </div>
              <div className="demo-account">
                <div><strong>Email:</strong> alice@example.com</div>
                <div><strong>Password:</strong> secure456</div>
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <p className="login-note">
            💡 This is a demo application with mock authentication.
          </p>
        </div>
      </div>
    </div>
  );
}

// Helper to get demo password (hardcoded for demo)
function getDemoPassword(email) {
  const passwords = {
    'demo@example.com': 'demo123',
    'john@example.com': 'password123',
    'alice@example.com': 'secure456'
  };
  return passwords[email] || 'demo123';
}

export default Login;