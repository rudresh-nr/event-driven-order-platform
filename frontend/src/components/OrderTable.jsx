import StatusBadge from "./StatusBadge";

function OrderTable({ orders }) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Status</th>
                    <th>Amount</th>
                </tr>
            </thead>

            <tbody>
                {orders.map((order) => (
                    <tr key={order.order_id}>
                        <td>{order.order_id}</td>
                        <td><StatusBadge status={order.status}/></td>
                        <td>{order.total_amount}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default OrderTable;