import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  async register(userData: {
    email: string;
    password: string;
    full_name: string;
    phone?: string;
    preferred_language?: string;
  }) {
    const response = await this.client.post('/api/users/register', userData);
    return response.data;
  }

  async login(email: string, password: string) {
    const response = await this.client.post('/api/users/login', {
      email,
      password,
    });
    this.setToken(response.data.access_token);
    return response.data;
  }

  logout() {
    this.clearToken();
  }

  async getCurrentUser() {
    const response = await this.client.get('/api/users/me');
    return response.data;
  }

  async createLearnerProfile(profileData: any) {
    const response = await this.client.post('/api/users/profile', profileData);
    return response.data;
  }

  async getLearnerProfile() {
    const response = await this.client.get('/api/users/profile');
    return response.data;
  }

  async getCourses(params?: {
    sector?: string;
    nsqf_level?: string;
    skip?: number;
    limit?: number;
  }) {
    const response = await this.client.get('/api/courses/', { params });
    return response.data;
  }

  async getCourse(courseId: number) {
    const response = await this.client.get(`/api/courses/${courseId}`);
    return response.data;
  }

  async getRecommendations(params?: {
    top_k?: number;
    include_explanations?: boolean;
  }) {
    const response = await this.client.post('/api/ml/recommendations', null, {
      params,
    });
    return response.data;
  }

  async getLearningPath(careerGoal: string, targetNsqfLevel?: string) {
    const response = await this.client.get('/api/ml/learning-path', {
      params: {
        career_goal: careerGoal,
        target_nsqf_level: targetNsqfLevel,
      },
    });
    return response.data;
  }

  async getSkillGapAnalysis(targetRole: string) {
    const response = await this.client.get('/api/ml/skill-gap-analysis', {
      params: { target_role: targetRole },
    });
    return response.data;
  }

  async updateProgress(progressData: {
    learner_id: number;
    course_id: number;
    completion_percentage: number;
    skills_acquired?: string[];
    assessment_score?: number;
  }) {
    const response = await this.client.post('/api/courses/progress', progressData);
    return response.data;
  }

  async getMyProgress() {
    const response = await this.client.get('/api/courses/progress/my-courses');
    return response.data;
  }

  async getJobMarketInsights(params?: {
    skills?: string[];
    sector?: string;
  }) {
    const response = await this.client.get('/api/ml/job-market-insights', {
      params,
    });
    return response.data;
  }

  async getSectors() {
    const response = await this.client.get('/api/courses/sectors');
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
