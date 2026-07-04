import axios from 'axios';

const API_BASE_URL = __DEV__
  ? 'http://10.0.2.2:8000/api/v1' // Android emulator -> host machine
  : 'https://api.mycart.app/api/v1'; // production URL (placeholder)

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(config => {
  // TODO: attach JWT from auth store
  return config;
});

apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // TODO: attempt token refresh
    }
    return Promise.reject(error);
  },
);

export default apiClient;
