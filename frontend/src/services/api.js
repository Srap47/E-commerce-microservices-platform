const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
};

// Product Service
export const productService = {
  getAll: () => apiCall('/products'),
  getById: (id) => apiCall(`/products/${id}`),
  search: (query) => apiCall(`/products/search?q=${query}`),
  getRecommended: () => apiCall('/products/recommended'),
};

// Cart Service
export const cartService = {
  getCart: (userId) => apiCall(`/cart/${userId}`),
  addItem: (userId, item) => apiCall(`/cart/${userId}/items`, {
    method: 'POST',
    body: JSON.stringify(item),
  }),
  removeItem: (userId, productId) => apiCall(`/cart/${userId}/items/${productId}`, {
    method: 'DELETE',
  }),
  updateItem: (userId, productId, quantity) => apiCall(`/cart/${userId}/items/${productId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  }),
  clear: (userId) => apiCall(`/cart/${userId}`, { method: 'DELETE' }),
};

// Auth Service
export const authService = {
  login: (credentials) => apiCall('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),
  register: (userData) => apiCall('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  logout: () => {
    localStorage.removeItem('token');
  },
  getToken: () => localStorage.getItem('token'),
  setToken: (token) => localStorage.setItem('token', token),
};

export default {
  productService,
  cartService,
  authService,
};
