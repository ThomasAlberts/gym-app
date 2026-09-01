import api from "./axios";

export const register = (payload) => api.post("/auth/register", payload);

export const login = (email, password) =>
  api.post("/auth/login", { email, password });

export const refresh = () => api.post("/auth/refresh");

export const logout = () => api.post("/auth/logout");

export const me = () => api.get("/auth/me");

export const forgotPassword = (email) =>
  api.post("/auth/forgot-password", { email });