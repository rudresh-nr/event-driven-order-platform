
import { getOrderByUser, cancelOrder } from "../api/orders";
import OrderTable from "./OrderTable";
import { useState, useEffect } from "react";

function OrderList() {
    const [userId, setUserId] = useState("44444444-4444-4444-4444-444444444445");
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadOrders = async () => {
        try{
            setLoading(true);
            const data = await getOrderByUser(userId);
            setOrders(data);
        }catch(error){
            console.error(error);
            alert("Failed to load orders")
        }finally {
            setLoading(false);
        }
    }
    useEffect(() => {loadOrders();}, []);

    const handleCancel = async (orderId) => {
        try{
            await cancelOrder(orderId);
            //load orders after cancellation
            loadOrders();
        }catch(error) {
            console.error(error)
            alert("failed to cancel order");
        }
    }

return (
    <div className="card">
        <h2>Order List</h2>
            <div className="search-bar">
                <input
                    placeholder="User ID"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                />

                <button onClick={loadOrders}>
                    Load Orders
                </button>
                
            </div>

        <hr />
        {loading && <p>Loading...</p>}

        {orders.length === 0 && (
            <p>No orders found</p>
        )}

        {orders.length > 0 && (
            <OrderTable orders={orders} onCancel={handleCancel}/>
        )}
    </div>
);

}

export default OrderList;