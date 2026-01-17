/**
 * Cart Component
 * Displays and manages shopping cart items
 */
import { useState, useEffect } from 'react';
import { cartAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

function Cart() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updating, setUpdating] = useState({});
  const { isAuthenticated, user } = useAuth();

  useEffect(() => {
    if (isAuthenticated()) {
      loadCart();
    } else {
      setLoading(false);
    }
  }, []);

  const loadCart = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await cartAPI.getCart();
      setCart(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) return;

    try {
      setUpdating(prev => ({ ...prev, [productId]: true }));
      await cartAPI.updateCartItem(productId, newQuantity);
      await loadCart(); // Reload cart to get updated totals
    } catch (err) {
      alert(`Failed to update quantity: ${err.message}`);
    } finally {
      setUpdating(prev => ({ ...prev, [productId]: false }));
    }
  };

  const handleRemoveItem = async (productId) => {
    if (!confirm('Remove this item from cart?')) return;

    try {
      setUpdating(prev => ({ ...prev, [productId]: true }));
      await cartAPI.removeFromCart(productId);
      await loadCart();
    } catch (err) {
      alert(`Failed to remove item: ${err.message}`);
    } finally {
      setUpdating(prev => ({ ...prev, [productId]: false }));
    }
  };

  const handleClearCart = async () => {
    if (!confirm('Clear entire cart? This cannot be undone.')) return;

    try {
      setLoading(true);
      await cartAPI.clearCart();
      await loadCart();
    } catch (err) {
      alert(`Failed to clear cart: ${err.message}`);
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  // Not authenticated
  if (!isAuthenticated()) {
    return (
      <div className="cart-container">
        <div className="container">
          <div className="empty-state">
            <h2>🔒 Login Required</h2>
            <p>Please login to view your shopping cart.</p>
          </div>
        </div>
      </div>
    );
  }

  // Loading state
  if (loading) {
    return (
      <div className="cart-container">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading your cart...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="cart-container">
        <div className="container">
          <div className="error-message">
            <p>❌ Failed to load cart: {error}</p>
            <button onClick={loadCart}>Retry</button>
          </div>
        </div>
      </div>
    );
  }

  // Empty cart
  if (!cart || cart.items.length === 0) {
    return (
      <div className="cart-container">
        <div className="container">
          <div className="page-header">
            <h1>🛒 Shopping Cart</h1>
            <p className="subtitle">Welcome, {user?.name}</p>
          </div>
          <div className="empty-state">
            <div className="empty-cart-icon">🛒</div>
            <h2>Your cart is empty</h2>
            <p>Browse our products and add items to your cart.</p>
          </div>
        </div>
      </div>
    );
  }

  // Cart with items
  return (
    <div className="cart-container">
      <div className="container">
        <div className="page-header">
          <h1>🛒 Shopping Cart</h1>
          <p className="subtitle">Welcome, {user?.name}</p>
        </div>

        <div className="cart-content">
          {/* Cart Items */}
          <div className="cart-items">
            <div className="cart-header">
              <h2>{cart.total_items} {cart.total_items === 1 ? 'Item' : 'Items'}</h2>
              <button 
                className="clear-cart-btn" 
                onClick={handleClearCart}
                disabled={loading}
              >
                Clear Cart
              </button>
            </div>

            {cart.items.map((item) => (
              <div key={item.product_id} className="cart-item">
                <div className="cart-item-details">
                  <h3 className="cart-item-name">{item.product_name}</h3>
                  <p className="cart-item-price">{formatPrice(item.price)} each</p>
                </div>

                <div className="cart-item-actions">
                  <div className="quantity-controls">
                    <button
                      className="quantity-btn"
                      onClick={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}
                      disabled={item.quantity <= 1 || updating[item.product_id]}
                    >
                      −
                    </button>
                    <span className="quantity-display">{item.quantity}</span>
                    <button
                      className="quantity-btn"
                      onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                      disabled={updating[item.product_id]}
                    >
                      +
                    </button>
                  </div>

                  <div className="cart-item-subtotal">
                    {formatPrice(item.price * item.quantity)}
                  </div>

                  <button
                    className="remove-btn"
                    onClick={() => handleRemoveItem(item.product_id)}
                    disabled={updating[item.product_id]}
                    title="Remove from cart"
                  >
                    {updating[item.product_id] ? '⏳' : '🗑️'}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Cart Summary */}
          <div className="cart-summary">
            <h2>Order Summary</h2>
            
            <div className="summary-row">
              <span>Items ({cart.total_items})</span>
              <span>{formatPrice(cart.total_price)}</span>
            </div>

            <div className="summary-row">
              <span>Shipping</span>
              <span className="free-shipping">FREE</span>
            </div>

            <div className="summary-row">
              <span>Tax (estimated)</span>
              <span>{formatPrice(cart.total_price * 0.08)}</span>
            </div>

            <hr />

            <div className="summary-row total">
              <span>Total</span>
              <span>{formatPrice(cart.total_price * 1.08)}</span>
            </div>

            <button className="checkout-btn">
              Proceed to Checkout
            </button>

            <p className="summary-note">
              💳 This is a demo application. No actual payment will be processed.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Cart;