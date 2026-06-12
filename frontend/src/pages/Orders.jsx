import { useState, useEffect } from 'react';
import API from '../api/axios';
import toast from 'react-hot-toast';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const username = localStorage.getItem('username');

  useEffect(() => {
    API.get(`/orders/${username}`)
      .then(res => {
        setOrders(res.data.orders);
        setLoading(false);
      })
      .catch(() => {
        toast.error('Failed to load orders');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">Loading orders...</div>;

  return (
    <div className="orders-page">
      <h2>Your Orders</h2>
      {orders.length === 0 ? (
        <p className="no-orders">No orders yet</p>
      ) : (
        <div className="orders-list">
          {orders.map((order, index) => (
            <div key={index} className="order-card">
              <div className="order-header">
                <h3>Order #{order.order_id}</h3>
                <span className={`order-status ${order.status}`}>
                  {order.status}
                </span>
              </div>
              <div className="order-items">
                {order.items.map((item, i) => (
                  <div key={i} className="order-item">
                    <span>{item.name}</span>
                    <span>₹{item.price.toLocaleString()}</span>
                  </div>
                ))}
              </div>
              <div className="order-total">
                <strong>Total: ₹{order.total.toLocaleString()}</strong>
              </div>
              <div className="order-date">
                <small>{new Date(order.created_at).toLocaleDateString()}</small>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Orders;
