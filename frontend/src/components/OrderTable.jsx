import StatusBadge from "./StatusBadge";

function OrderTable({ orders, onCancel }) {
    console.log("onCancel =", onCancel);
    return (
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Status</th>
                    <th>Amount</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>
                {orders.map((order) => (
                    <tr key={order.order_id}>
                        <td>{order.order_id}</td>
                        <td><StatusBadge status={order.status}/></td>
                        <td>{order.total_amount}</td>
                        <td><button onClick={()=> onCancel(order.order_id)}>Cancel</button></td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default OrderTable;