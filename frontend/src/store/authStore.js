import { create } from 'zustand';
import axios from 'axios';

// Configure axios base URL
axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.withCredentials = true;

// Add response interceptor for automatic session handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Session expired, clear auth state
      useAuthStore.getState().setUser(null);
      useAuthStore.getState().setLoading(false);
      useAuthStore.getState().setError('Session expired. Please log in again.');
    }
    return Promise.reject(error);
  }
);


const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  // Actions
  setUser: (user) => {
    set({ user, isAuthenticated: !!user });
    // Persist user data to localStorage
    if (user) {
      localStorage.setItem('leetqode_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('leetqode_user');
    }
  },
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),

  // Initialize auth state from localStorage
  initializeAuth: async () => {
    const storedUser = localStorage.getItem('leetqode_user');
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser);
        set({ user, isAuthenticated: true, isLoading: true });
        // Verify session is still valid with backend
        await get().checkAuth();
      } catch (error) {
        localStorage.removeItem('leetqode_user');
        set({ user: null, isAuthenticated: false, isLoading: false });
      }
    } else {
      // No stored user, check if there's a valid session
      await get().checkAuth();
    }
  },

  // Check authentication status
  checkAuth: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/auth/status/', {
        timeout: 5000, // 5 second timeout
      });
      
      if (response.data.authenticated) {
        console.log('Auth check: User is authenticated', response.data.user);
        set({ 
          user: response.data.user, 
          isAuthenticated: true,
          isLoading: false
        });
      } else {
        console.log('Auth check: User is not authenticated');
        set({ 
          user: null, 
          isAuthenticated: false,
          isLoading: false
        });
      }
    } catch (error) {
      console.error('Auth check error:', error);
      set({ 
        user: null, 
        isAuthenticated: false,
        isLoading: false,
        error: error.code === 'ECONNREFUSED' ? 'Backend server not available' : (error.response?.data?.message || 'Authentication check failed')
      });
    }
  },

  // Login with Google credential
  login: async (credential) => {
    set({ isLoading: true, error: null });
    
    try {
      const response = await axios.post('/api/auth/google/', {
        credential: credential
      }, {
        timeout: 10000, // 10 second timeout
      });

      if (response.data.success) {
        console.log('Login successful:', response.data.user);
        set({
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false
        });
        // Authentication successful - no need to redirect, 
        // the App component will handle routing based on isAuthenticated state
      } else {
        set({
          error: response.data.error || 'Authentication failed',
          isLoading: false
        });
      }
    } catch (error) {
      console.error('Login error:', error);
      set({
        error: error.code === 'ECONNREFUSED' ? 'Backend server not available' : (error.response?.data?.error || 'Authentication failed'),
        isLoading: false
      });
    }
  },

  // Logout
  logout: async () => {
    set({ isLoading: true });
    try {
      // Use our API logout endpoint
      await axios.post('/api/auth/logout/');
    } catch (error) {
      console.error('Logout error:', error);
      // Continue with frontend logout even if backend fails
    } finally {
      set({ 
        user: null, 
        isAuthenticated: false,
        isLoading: false 
      });
      // Clear localStorage
      localStorage.removeItem('leetqode_user');
      // Redirect to login page
      window.location.href = '/login';
    }
  },
}));

export default useAuthStore;
