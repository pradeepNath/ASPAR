/**
 * utils/api.js
 * -------------
 * A single pre-configured Axios instance used by every page and component.
 *
 * Two things it does automatically:
 *   1. Sets baseURL to "/api" — combined with the Vite proxy in vite.config.js
 *      this means every call goes to Flask on port 5000 in dev, and to the
 *      same origin in production.
 *   2. Request interceptor: reads the JWT from localStorage and injects it as
 *      "Authorization: Bearer <token>" on every request — so individual pages
 *      never have to handle this manually.
 *
 * Usage in any page:
 *   import api from "../utils/api";
 *   const res = await api.post("/auth/login", { email, password });
 */

import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

// --- Request interceptor: attach JWT if present ---
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Response interceptor: auto-logout on 401 ---
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;