import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // Change if your backend uses another URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
},
(eror)=> Promise.reject(error)
);

export default api;