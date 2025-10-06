import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (pin) => api.post("/auth/login", { pin });
export const getBalance = () => api.get("/account/balance");
export const withdraw = (amount) => api.post("/account/withdraw", { amount });
export const deposit = (amount) => api.post("/account/deposit", { amount });
export const getDailyLimit = () => api.get("/account/daily-limit");
