import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import toast from 'react-hot-toast';

function CartPage() {
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [loading, setLoading] = useState(true);
  const [ordering, setOrdering] = useState(false);
  const username = localStorage.getItem('username');
  const navigate = useNavigate();

  const fetchCart = async () => {
    try {
      const res = await API.get(`/cart/${username}`);
      setCart(res.data);
    } catch (err) {
      toast.error('Failed to load cart');
    }
    setLoading(false);
  };

  useEffect(() => { fetchCart(); }, []);

  const removeItem = async (itemId) => {
    try {
      await API.delete(`/cart/${username}/${itemId}`);
      toast.success('Item removed');
      fetchCart();
    } catch (err) {
      toast.error('Failed to remove item');
    }
  };

  const placeOrder = async () => {
    setOrdering(true);
    try {
      const res = await API.post(`/orders/${username}`);
      toast.success(`Order ${res.data.order.order_id} placed successfully!`);
      navigate('/orders');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to place order');
    }
    setOrdering(false);
  };

  if (loading) return <div className="loading">Loading cart...</div>;

  return (
    <div className="cart-page">
      <h2>Your Cart</h2>
      {cart.items.length === 0 ? (
        <div className="empty-cart">
          <p>Your cart is empty</p>
          <button onClick={() => navigate('/')}>Shop Now</button>
        </div>
      ) : (
        <>
          <div className="cart-items">
            {cart.items.map((item, index) => (
              <div key={index} className="cart-item">
                <div className="cart-item-info">
                  <h3>{item.name}</h3>
                  <p>₹{item.price.toLocaleString()}</p>
                </div>
                <button
                  onClick={() => removeItem(item.id)}
                  className="btn-remove"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h3>Total: ₹{cart.total.toLocaleString()}</h3>
            <button
              onClick={placeOrder}
              disabled={ordering}
              className="btn-order"
            >
              {ordering ? 'Placing Order...' : 'Place Order'}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default CartPage;
