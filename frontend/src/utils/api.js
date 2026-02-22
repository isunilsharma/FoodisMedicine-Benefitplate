import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;

// Auth API
export const authAPI = {
  exchangeSession: (sessionId) => api.post('/auth/session', { session_id: sessionId }),
  getMe: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

// Geography API
export const geographyAPI = {
  lookupZip: (zipCode) => api.post('/geography/lookup', { zip_code: zipCode }),
};

// Eligibility API
export const eligibilityAPI = {
  evaluate: (zipCode, answers) => api.post('/eligibility/evaluate', { zip_code: zipCode, answers }),
};

// Programs API
export const programsAPI = {
  list: (params) => api.get('/programs', { params }),
  getById: (programId) => api.get(`/programs/${programId}`),
  generateExplanation: (programId, matchedConditions, unmetConditions = []) =>
    api.post(`/programs/${programId}/generate-explanation`, { matched_conditions: matchedConditions, unmet_conditions: unmetConditions }),
};

// User API
export const userAPI = {
  saveResult: (data) => api.post('/user/save-result', data),
  getSavedResults: () => api.get('/user/saved-results'),
  generatePDF: (programIds, zipCode, county, state) =>
    api.post('/user/generate-checklist-pdf', { program_ids: programIds, zip_code: zipCode, county, state }, { responseType: 'blob' }),
};

// Admin API
export const adminAPI = {
  listPrograms: () => api.get('/admin/programs'),
  createProgram: (data) => api.post('/admin/programs', data),
  updateProgram: (programId, data) => api.put(`/admin/programs/${programId}`, data),
  deleteProgram: (programId) => api.delete(`/admin/programs/${programId}`),
  programsNeedingReview: () => api.get('/admin/programs/needs-review'),
  getAnalytics: (days = 30) => api.get('/admin/analytics', { params: { days } }),
};
