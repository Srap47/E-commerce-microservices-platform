/**
 * Product List Component
 * Displays ranked products with filtering options
 */
import { useState, useEffect } from 'react';
import { productsAPI, cartAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ProductCard from './ProductCard';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    sort_by: 'ranking',
    min_price: '',
    max_price: '',
    min_rating: '',
  });
  const [addingToCart, setAddingToCart] = useState({});
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    loadProducts();
  }, [filters]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);

      // Build query params (only include non-empty values)
      const params = {};
      if (filters.sort_by) params.sort_by = filters.sort_by;
      if (filters.min_price) params.min_price = filters.min_price;
      if (filters.max_price) params.max_price = filters.max_price;
      if (filters.min_rating) params.min_rating = filters.min_rating;

      const data = await productsAPI.getProducts(params);
      setProducts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (product) => {
    if (!isAuthenticated()) {
      alert('Please login to add items to cart');
      return;
    }

    try {
      setAddingToCart(prev => ({ ...prev, [product.id]: true }));
      await cartAPI.addToCart(product, 1);
      alert(`${product.name} added to cart!`);
    } catch (err) {
      alert(`Failed to add to cart: ${err.message}`);
    } finally {
      setAddingToCart(prev => ({ ...prev, [product.id]: false }));
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="product-list-container">
      <div className="container">
        <div className="page-header">
          <h1>Products</h1>
          <p className="subtitle">Intelligently ranked using multi-factor algorithm</p>
        </div>

        {/* Filters */}
        <div className="filters">
          <div className="filter-group">
            <label htmlFor="sort_by">Sort By:</label>
            <select
              id="sort_by"
              value={filters.sort_by}
              onChange={(e) => handleFilterChange('sort_by', e.target.value)}
            >
              <option value="ranking">Smart Ranking</option>
              <option value="price">Price</option>
              <option value="popularity">Popularity</option>
              <option value="rating">Rating</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="min_price">Min Price:</label>
            <input
              id="min_price"
              type="number"
              placeholder="$0"
              value={filters.min_price}
              onChange={(e) => handleFilterChange('min_price', e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="max_price">Max Price:</label>
            <input
              id="max_price"
              type="number"
              placeholder="Any"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="min_rating">Min Rating:</label>
            <input
              id="min_rating"
              type="number"
              step="0.1"
              min="0"
              max="5"
              placeholder="0"
              value={filters.min_rating}
              onChange={(e) => handleFilterChange('min_rating', e.target.value)}
            />
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading products...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error-message">
            <p>❌ Failed to load products: {error}</p>
            <button onClick={loadProducts}>Retry</button>
          </div>
        )}

        {/* Products Grid */}
        {!loading && !error && (
          <>
            <div className="results-info">
              <p>Found {products.length} products</p>
              {filters.sort_by === 'ranking' && (
                <p className="ranking-note">
                  ⭐ Sorted by intelligent ranking algorithm
                </p>
              )}
            </div>

            <div className="products-grid">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={handleAddToCart}
                  isAddingToCart={addingToCart[product.id]}
                />
              ))}
            </div>
          </>
        )}

        {/* Empty State */}
        {!loading && !error && products.length === 0 && (
          <div className="empty-state">
            <p>No products found matching your filters.</p>
            <button onClick={() => setFilters({
              sort_by: 'ranking',
              min_price: '',
              max_price: '',
              min_rating: '',
            })}>
              Clear Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductList;