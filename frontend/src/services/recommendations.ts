import api from './api';
import { RecommendationRequest, RecommendationResponse, RecommendationListItem } from '../types';

export const recommendationService = {
  async create(request: RecommendationRequest): Promise<RecommendationResponse> {
    const { data } = await api.post<RecommendationResponse>('/api/recommendations/', request);
    return data;
  },

  async list(): Promise<RecommendationListItem[]> {
    const { data } = await api.get<RecommendationListItem[]>('/api/recommendations/');
    return data;
  },

  async getById(id: string): Promise<RecommendationResponse> {
    const { data } = await api.get<RecommendationResponse>(`/api/recommendations/${id}`);
    return data;
  },

  async getRisk(id: string) {
    const { data } = await api.get(`/api/recommendations/${id}/risk`);
    return data;
  },

  async getSustainability(id: string) {
    const { data } = await api.get(`/api/recommendations/${id}/sustainability`);
    return data;
  },

  getReportUrl(id: string): string {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/recommendations/${id}/report`;
  },
};
