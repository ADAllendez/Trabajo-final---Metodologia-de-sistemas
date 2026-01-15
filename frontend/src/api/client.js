import axios from "axios";

// Asegurar que la URL siempre sea HTTPS
let apiUrl = process.env.REACT_APP_API_URL || "https://back-end-production-9732.up.railway.app";

// Reemplazar http:// con https:// si es necesario
if (apiUrl.startsWith("http://")) {
  apiUrl = apiUrl.replace("http://", "https://");
}

console.log("API URL =", apiUrl);

const api = axios.create({
  baseURL: apiUrl,
});

export default api;
