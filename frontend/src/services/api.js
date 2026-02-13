import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiService = {
  // Upload CSV file
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Analyze data
  analyzeData: async (sessionId) => {
    const response = await axios.post(`${API_BASE_URL}/analyze/${sessionId}`);
    return response.data;
  },

  // Generate predictions
  predict: async (sessionId, targetColumn, steps = 5) => {
    const response = await axios.post(
      `${API_BASE_URL}/predict/${sessionId}?target_column=${targetColumn}&steps=${steps}`
    );
    return response.data;
  },

  // Get dashboard data
  getDashboard: async (sessionId) => {
    const response = await axios.get(`${API_BASE_URL}/dashboard/${sessionId}`);
    return response.data;
  },

  // Get columns
  getColumns: async (sessionId) => {
    const response = await axios.get(`${API_BASE_URL}/columns/${sessionId}`);
    return response.data;
  },

  // Delete session
  deleteSession: async (sessionId) => {
    const response = await axios.delete(`${API_BASE_URL}/session/${sessionId}`);
    return response.data;
  },
};
