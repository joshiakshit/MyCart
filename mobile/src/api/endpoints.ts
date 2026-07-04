import apiClient from './client';
import type {SearchResponse} from '../types/product';
import type {AuthTokens, LinkedAccount} from '../types/platform';

export const authApi = {
  requestOtp: (phoneNumber: string) =>
    apiClient.post('/auth/request-otp', {phone_number: phoneNumber}),

  verifyOtp: (phoneNumber: string, otp: string) =>
    apiClient.post<AuthTokens>('/auth/verify-otp', {
      phone_number: phoneNumber,
      otp,
    }),

  refresh: (refreshToken: string) =>
    apiClient.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    }),
};

export const searchApi = {
  search: (query: string, platforms: string[] = ['blinkit', 'zepto']) =>
    apiClient.get<SearchResponse>('/search', {
      params: {q: query, platforms: platforms.join(',')},
    }),
};

export const accountsApi = {
  list: () =>
    apiClient.get<{accounts: LinkedAccount[]}>('/accounts'),

  link: (platform: string, phoneNumber: string) =>
    apiClient.post('/accounts/link', {
      platform,
      phone_number: phoneNumber,
    }),

  verifyLink: (platform: string, phoneNumber: string, otp: string) =>
    apiClient.post('/accounts/verify-otp', {
      platform,
      phone_number: phoneNumber,
      otp,
    }),

  unlink: (platform: string) => apiClient.delete(`/accounts/${platform}`),
};

export const productsApi = {
  getProduct: (platform: string, productId: string) =>
    apiClient.get(`/products/${platform}/${productId}`),
};

export const pricesApi = {
  history: (platform: string, productId: string, days: number = 30) =>
    apiClient.get('/prices/history', {
      params: {platform, product_id: productId, days},
    }),
};
