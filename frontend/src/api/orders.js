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