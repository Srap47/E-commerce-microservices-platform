/**
 * API Service
 * Centralized API calls to the backend API Gateway
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

/**
 * Get JWT token from localStorage
 */
const getAuthToken = () => {
  return localStorage.getItem('access_token');
};

/**
 * Create headers with optional authentication
 */
const createHeaders = (includeAuth = false) => {
  const headers = {
    'Content-Type': 'application/json',
  };

  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  return headers;
};

/**
 * Handle API errors
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// ============================================================================
// Authentication API
// ============================================================================

export const authAPI = {
  /**
   * Login user
   */
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: createHeaders(),
      body: JSON.stringify({ email, password }),
    });
    return handleResponse(response);
  },

  /**
   * Verify token
   */
  verifyToken: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/verify`, {
      method: 'POST',
      headers: createHeaders(),
      body: JSON.stringify({ token }),
    });
    return handleResponse(response);
  },

  /**
   * Get demo users (for testing)
   */
  getDemoUsers: async () => {
    const response = await fetch(`${API_BASE_URL}/auth/users`);
    return handleResponse(response);
  },
};

// ============================================================================
// Products API
// ============================================================================

export const productsAPI = {
  /**
   * Get all products with optional filters
   */
  getProducts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/products${queryString ? `?${queryString}` : ''}`;
    
    const response = await fetch(url, {
      headers: createHeaders(),
    });
    return handleResponse(response);
  },

  /**
   * Get single product by ID
   */
  getProduct: async (productId) => {
    const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
      headers: createHeaders(),
    });
    return handleResponse(response);
  },

  /**
   * Search products
   */
  searchProducts: async (query) => {
    const response = await fetch(`${API_BASE_URL}/products/search/${query}`, {
      headers: createHeaders(),
    });
    return handleResponse(response);
  },
};

// ============================================================================
// Cart API
// ============================================================================

export const cartAPI = {
  /**
   * Get user's cart
   */
  getCart: async () => {
    const response = await fetch(`${API_BASE_URL}/cart`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  /**
   * Add item to cart
   */
  addToCart: async (product, quantity = 1) => {
    const response = await fetch(`${API_BASE_URL}/cart/add`, {
      method: 'POST',
      headers: createHeaders(true),
      body: JSON.stringify({
        product_id: product.id,
        product_name: product.name,
        price: product.price,
        quantity,
      }),
    });
    return handleResponse(response);
  },

  /**
   * Update cart item quantity
   */
  updateCartItem: async (productId, quantity) => {
    const response = await fetch(
      `${API_BASE_URL}/cart/update/${productId}?quantity=${quantity}`,
      {
        method: 'PUT',
        headers: createHeaders(true),
      }
    );
    return handleResponse(response);
  },

  /**
   * Remove item from cart
   */
  removeFromCart: async (productId) => {
    const response = await fetch(`${API_BASE_URL}/cart/remove/${productId}`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  /**
   * Clear entire cart
   */
  clearCart: async () => {
    const response = await fetch(`${API_BASE_URL}/cart/clear`, {
      method: 'DELETE',
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },

  /**
   * Get cart item count
   */
  getCartCount: async () => {
    const response = await fetch(`${API_BASE_URL}/cart/count`, {
      headers: createHeaders(true),
    });
    return handleResponse(response);
  },
};