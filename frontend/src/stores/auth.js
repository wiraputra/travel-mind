import { defineStore } from 'pinia';
import apiClient from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('user-token') || null,
    user: JSON.parse(localStorage.getItem('user-info')) || null, // { userId, username }
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    // getToken: (state) => state.token,
    // getCurrentUser: (state) => state.user,
  },
  actions: {
    setAuth({ token, userData }) {
      this.token = token;
      this.user = userData; // userData bisa berupa { userId, username }
      localStorage.setItem('user-token', token);
      localStorage.setItem('user-info', JSON.stringify(userData));
    },
    clearAuth() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('user-token');
      localStorage.removeItem('user-info');
    },
    async loginAction(credentials) {
      try {
        const response = await apiClient.post('/auth/login', credentials);
        const token = response.data.access_token;
        const userData = { userId: response.data.user_id, username: response.data.username };
        this.setAuth({ token, userData });
        return Promise.resolve(response.data);
      } catch (error) {
        this.clearAuth();
        return Promise.reject(error.response.data);
      }
    },
    logout() {
      this.clearAuth();
      // router.push('/login');
    },
    async registerAction(userData) {
      try {
        const response = await apiClient.post('/auth/register', userData);
        return Promise.resolve(response.data);
      } catch (error) {
        return Promise.reject(error.response?.data || { msg: 'Terjadi kesalahan tak dikenal' });
      }
    }
  },
});
