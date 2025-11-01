export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false;
  const token = localStorage.getItem('access_token');
  return !!token;
};

export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
};

export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
};

export const clearToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
};

export const redirectToLogin = (): void => {
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};

export const redirectToDashboard = (): void => {
  if (typeof window !== 'undefined') {
    window.location.href = '/dashboard';
  }
};
