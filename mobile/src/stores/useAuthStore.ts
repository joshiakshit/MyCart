import {create} from 'zustand';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  phoneNumber: string | null;
  setTokens: (access: string, refresh: string) => void;
  setPhone: (phone: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>(set => ({
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  phoneNumber: null,
  setTokens: (access, refresh) =>
    set({accessToken: access, refreshToken: refresh, isAuthenticated: true}),
  setPhone: (phone) => set({phoneNumber: phone}),
  logout: () =>
    set({
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      phoneNumber: null,
    }),
}));
