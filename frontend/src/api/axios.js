import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

let isRefreshing = false;
let pendingRequests = [];

const processQueue = (error) => {
  pendingRequests.forEach(({ resolve, reject }) => {
    error ? reject(error) : resolve();
  });
  pendingRequests = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Alleen proberen te refreshen bij 401, en niet voor het refresh-endpoint zelf
    // (anders oneindige loop), en maar één keer per originele request.
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes("/auth/refresh") &&
      !originalRequest.url?.includes("/auth/login")
    ) {
      if (isRefreshing) {
        // Er loopt al een refresh — wacht daarop en probeer daarna opnieuw
        return new Promise((resolve, reject) => {
          pendingRequests.push({ resolve, reject });
        }).then(() => api(originalRequest));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        await api.post("/auth/refresh");
        processQueue(null);
        return api(originalRequest); // originele request opnieuw doen
      } catch (refreshError) {
        processQueue(refreshError);
        // Refresh mislukt -> echt uitgelogd, laat de rest van de app dit oppakken
        window.dispatchEvent(new Event("authExpired"));
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;