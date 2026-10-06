import api from './api';
import { PackagingMaterial } from '../types';

export const packagingService = {
  async list(): Promise<PackagingMaterial[]> {
    const { data } = await api.get<PackagingMaterial[]>('/api/packaging/');
    return data;
  },

  async getById(id: string): Promise<PackagingMaterial> {
    const { data } = await api.get<PackagingMaterial>(`/api/packaging/${id}`);
    return data;
  },
};
