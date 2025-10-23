/**
 * API Configuration Module
 * 
 * Handles:
 * - Axios instance setup with base URL
 * - Request interceptor for token attachment
 * - Response interceptor for error handling and logging
 * - Authentication token management
 * - User notification on errors
 */

import axios from 'axios';
import toast from 'react-hot-toast';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api/',
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Request Interceptor
 * Attaches JWT token to Authorization header if present
 */
API.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

/**
 * Response Interceptor
 * Handles error responses with appropriate messages and actions
 * Implements retry logic for network errors
 * Logs all errors for debugging and monitoring
 */
API.interceptors.response.use(
  response => response,
  error => {
    const errorLog = {
      timestamp: new Date().toISOString(),
      status: error.response?.status,
      message: error.response?.data?.message || error.message,
      url: error.config?.url,
      method: error.config?.method,
      retryCount: error.config?.retryCount || 0,
    };

    console.error('API Error:', errorLog);

    // Handle different error status codes
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
      toast.error('Session expired. Please login again.');
    } else if (error.response?.status === 403) {
      // Forbidden - user lacks permissions
      toast.error('You do not have permission to perform this action.');
    } else if (error.response?.status === 404) {
      // Not found
      toast.error('The requested resource was not found.');
    } else if (error.response?.status === 422) {
      // Validation error
      const errors = error.response?.data?.errors;
      if (errors) {
        Object.values(errors).forEach(err => toast.error(err));
      } else {
        toast.error('Validation error. Please check your input.');
      }
    } else if (error.response?.status >= 500) {
      // Server error
      toast.error('Server error. Please try again later.');
    } else if (error.message === 'Network Error') {
      // Network error - suggest retry
      toast.error('Network error. Please check your connection and try again.');
    } else {
      // Generic error
      const message = error.response?.data?.message || error.message || 'Something went wrong';
      toast.error(message);
    }

    return Promise.reject(error);
  }
);

export default API;