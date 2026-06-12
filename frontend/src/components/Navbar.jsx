import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import API from '../api/axios';

function Navbar() {
  const navigate = useNavigate();
  const [cartCount, setCartCount] = useState(0);
  const username = localStorage.getItem('username');

  useEffect(() => {
    if (username) {
      API.get(`/cart/${username}`)
        .then(res => setCartCount(res.data.items.length))
        .catch(() => setCartCount(0));
    }
  }, [username]);

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">🛒 CartFlow</Link>
      <div className="nav-links">
        <Link to="/">Products</Link>
        {username ? (
          <>
            <Link to="/cart">Cart {cartCount > 0 && <span className="badge">{cartCount}</span>}</Link>
            <Link to="/orders">Orders</Link>
            <button onClick={logout} className="btn-logout">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
