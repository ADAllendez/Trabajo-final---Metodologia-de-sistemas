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

// Interceptor: forzar HTTPS en cualquier request (cubre casos con URLs absolutas)
api.interceptors.request.use(
  (config) => {
    try {
      if (config.url && config.url.startsWith("http://")) {
        config.url = config.url.replace("http://", "https://");
      }
      if (config.baseURL && config.baseURL.startsWith("http://")) {
        config.baseURL = config.baseURL.replace("http://", "https://");
      }
      // Asegurar que siempre haya baseURL (evita llamadas relativas que queden sin esquema)
      if (!config.baseURL) {
        config.baseURL = apiUrl;
      }
    } catch (e) {
      // no-op
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
