import React, { useState, useEffect } from 'react';
import { cartService } from '../services/api';

const Cart = () => {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const userId = localStorage.getItem('userId') || 'guest';

  useEffect(() => {
    const fetchCart = async () => {
      try {
        setLoading(true);
        const data = await cartService.getCart(userId);
        setCart(data);
      } catch (error) {
        console.error('Failed to load cart:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, [userId]);

  const handleRemoveItem = async (productId) => {
    try {
      await cartService.removeItem(userId, productId);
      const updatedCart = await cartService.getCart(userId);
      setCart(updatedCart);
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  const handleUpdateQuantity = async (productId, quantity) => {
    try {
      await cartService.updateItem(userId, productId, quantity);
      const updatedCart = await cartService.getCart(userId);
      setCart(updatedCart);
    } catch (error) {
      console.error('Failed to update quantity:', error);
    }
  };

  if (loading) return <div className="loading">Loading cart...</div>;
  if (!cart || cart.items.length === 0) return <div className="empty-cart">Your cart is empty</div>;

  return (
    <div className="cart">
      <h2>Shopping Cart</h2>
      <div className="cart-items">
        {cart.items.map((item) => (
          <div key={item.product_id} className="cart-item">
            <div className="item-details">
              <h4>Product {item.product_id}</h4>
              <p>${item.price.toFixed(2)} each</p>
            </div>
            <div className="item-quantity">
              <button onClick={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}>-</button>
              <span>{item.quantity}</span>
              <button onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}>+</button>
            </div>
            <div className="item-subtotal">
              <p>${(item.price * item.quantity).toFixed(2)}</p>
            </div>
            <button className="remove-btn" onClick={() => handleRemoveItem(item.product_id)}>
              Remove
            </button>
          </div>
        ))}
      </div>
      <div className="cart-summary">
        <h3>Total: ${cart.total_price.toFixed(2)}</h3>
        <button className="checkout-btn">Proceed to Checkout</button>
      </div>
    </div>
  );
};

export default Cart;
