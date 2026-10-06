import api from './api';

export const adminService = {
  async getStats() {
    const { data } = await api.get('/api/admin/stats');
    return data;
  },
  async getUsers() {
    const { data } = await api.get('/api/admin/users');
    return data;
  },
  async getAllRecommendations(skip = 0, limit = 20) {
    const { data } = await api.get(`/api/admin/recommendations?skip=${skip}&limit=${limit}`);
    return data;
  },
  async getMaterials() {
    const { data } = await api.get('/api/admin/materials');
    return data;
  },
};
