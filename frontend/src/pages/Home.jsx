import { useState, useEffect } from 'react';
import API from '../api/axios';
import ProductCard from '../components/ProductCard';

function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('All');

  useEffect(() => {
    API.get('/products')
      .then(res => {
        setProducts(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const categories = ['All', ...new Set(products.map(p => p.category))];
  const filtered = category === 'All'
    ? products
    : products.filter(p => p.category === category);

  if (loading) return <div className="loading">Loading products...</div>;

  return (
    <div className="home">
      <h2>Our Products</h2>
      <div className="categories">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={`btn-category ${category === cat ? 'active' : ''}`}
          >
            {cat}
          </button>
        ))}
      </div>
      <div className="products-grid">
        {filtered.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}

export default Home;
