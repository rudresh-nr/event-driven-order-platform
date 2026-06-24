import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const createOrder = async (data) =>{
    const response = await API.post("/orders/", data);
    return response.data;
}

export const getOrderByUser = async (userID) => {
  const response = await API.get(
    `/users/${userID}/orders/`
  );

  return response.data;
}

export async function cancelOrder(orderId) {
    const response = await axios.post(
        `http://localhost:8000/orders/${orderId}/cancel/`
    );
    return response.data;
}