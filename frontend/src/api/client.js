import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

console.log("API_URL:", process.env.REACT_APP_API_URL);

export default api;
