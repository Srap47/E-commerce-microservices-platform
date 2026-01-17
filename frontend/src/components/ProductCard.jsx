import React, { useState } from 'react';
import { cartService } from '../services/api';

const ProductCard = ({ product }) => {
  const [addingToCart, setAddingToCart] = useState(false);

  const handleAddToCart = async () => {
    try {
      setAddingToCart(true);
      const userId = localStorage.getItem('userId') || 'guest';
      await cartService.addItem(userId, {
        product_id: product.id,
        quantity: 1,
        price: product.price,
      });
      alert(`${product.name} added to cart!`);
    } catch (error) {
      console.error('Failed to add to cart:', error);
      alert('Failed to add to cart');
    } finally {
      setAddingToCart(false);
    }
  };

  return (
    <div className="product-card">
      <img src={`/images/product-${product.id}.jpg`} alt={product.name} className="product-image" />
      <div className="product-info">
        <h3>{product.name}</h3>
        <p className="description">{product.description}</p>
        <div className="price-rating">
          <span className="price">${product.price.toFixed(2)}</span>
          <span className="rating">⭐ {product.rating}/5 ({product.reviews_count} reviews)</span>
        </div>
        <div className="stock-status">
          {product.stock > 0 ? (
            <span className="in-stock">In Stock ({product.stock})</span>
          ) : (
            <span className="out-of-stock">Out of Stock</span>
          )}
        </div>
        <button
          className="add-to-cart-btn"
          onClick={handleAddToCart}
          disabled={addingToCart || product.stock === 0}
        >
          {addingToCart ? 'Adding...' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
