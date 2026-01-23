import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const qualifyLead = async (leadData) => {
  const response = await api.post("/leads", leadData);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get("/health");
  return response.data;
};

export default api;
