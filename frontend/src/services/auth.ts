import api from './api';
import { AuthToken, LoginCredentials, RegisterData, User } from '../types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthToken> {
    const { data } = await api.post<AuthToken>('/api/auth/login', credentials);
    return data;
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/api/auth/register', data);
    return response.data;
  },

  async getMe(): Promise<User> {
    const { data } = await api.get<User>('/api/auth/me');
    return data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};
