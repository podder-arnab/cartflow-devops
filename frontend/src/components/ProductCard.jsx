import { useState } from 'react';
import API from '../api/axios';
import toast from 'react-hot-toast';

function ProductCard({ product }) {
  const [loading, setLoading] = useState(false);
  const username = localStorage.getItem('username');

  const addToCart = async () => {
    if (!username) {
      toast.error('Please login to add items to cart');
      return;
    }
    setLoading(true);
    try {
      await API.post(`/cart/${username}`, {
        id: product.id,
        name: product.name,
        price: product.price
      });
      toast.success(`${product.name} added to cart!`);
    } catch (err) {
      toast.error('Failed to add item');
    }
    setLoading(false);
  };

  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <div className="product-info">
        <span className="product-category">{product.category}</span>
        <h3>{product.name}</h3>
        <p className="product-price">₹{product.price.toLocaleString()}</p>
        <button
          onClick={addToCart}
          disabled={loading}
          className="btn-add-cart"
        >
          {loading ? 'Adding...' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}

export default ProductCard;
