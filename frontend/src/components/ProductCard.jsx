/**
 * Product Card Component
 * Displays individual product with ranking information
 */
function ProductCard({ product, onAddToCart, isAddingToCart }) {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={`full-${i}`} className="star filled">★</span>);
    }
    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star">★</span>);
    }
    return stars;
  };

  const getStockStatus = (stock) => {
    if (stock === 0) return { text: 'Out of Stock', class: 'out-of-stock' };
    if (stock < 5) return { text: 'Low Stock', class: 'low-stock' };
    return { text: 'In Stock', class: 'in-stock' };
  };

  const stockStatus = getStockStatus(product.stock);

  return (
    <div className="product-card">
      {product.rank && (
        <div className="rank-badge">#{product.rank}</div>
      )}

      <div className="product-image">
        <img
          src={product.image_url || 'https://via.placeholder.com/300x200?text=No+Image'}
          alt={product.name}
          loading="lazy"
        />
      </div>

      <div className="product-details">
        <div className="product-category">{product.category}</div>
        <h3 className="product-name">{product.name}</h3>
        
        {product.description && (
          <p className="product-description">{product.description}</p>
        )}

        <div className="product-rating">
          <div className="stars">
            {renderStars(product.rating)}
          </div>
          <span className="rating-value">
            {product.rating.toFixed(1)} ({product.sales_count} sales)
          </span>
        </div>

        <div className="product-metrics">
          <div className="metric">
            <span className="metric-label">Popularity</span>
            <span className="metric-value">{product.popularity}/100</span>
          </div>
          {product.ranking_score && (
            <div className="metric">
              <span className="metric-label">Rank Score</span>
              <span className="metric-value">{product.ranking_score.toFixed(1)}</span>
            </div>
          )}
        </div>

        <div className="product-footer">
          <div className="price-stock">
            <div className="product-price">{formatPrice(product.price)}</div>
            <div className={`stock-status ${stockStatus.class}`}>
              {stockStatus.text} ({product.stock})
            </div>
          </div>

          <button
            className="add-to-cart-btn"
            onClick={() => onAddToCart(product)}
            disabled={product.stock === 0 || isAddingToCart}
          >
            {isAddingToCart ? (
              <>
                <span className="spinner-small"></span> Adding...
              </>
            ) : product.stock === 0 ? (
              'Out of Stock'
            ) : (
              '🛒 Add to Cart'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;