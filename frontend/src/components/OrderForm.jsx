import { useState } from "react";
import { createOrder } from "../api/orders";


function OrderForm() {
  const [userId, setUserId] = useState("");
  const [amount, setAmount] = useState("");
  const [orderID, setOrderId] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async () => {
    try{
        const data = await createOrder({
            user_id: userId,
            total_amount : amount,
            currency : "INR",
        });

        setOrderId(data.order_id);
        setStatus(data.status);
    } catch(error) {
        console.error(error);
        alert("failed to create order");
    }
  };


  return (
    <div>
      <h2>Create Order</h2>

      <input
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSubmit}>Create Order</button>

      <br></br>
      {orderID && (
        <div>
            <p>Order ID: {orderID}</p>
            <p>Status: {status}</p>
        </div>
      )}
    </div>
  );
}

export default OrderForm;