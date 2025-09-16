import { create } from 'zustand';
import axios from 'axios';

const useProblemStore = create((set, get) => ({
  problems: [],
  userProblems: [],
  dashboardProblems: [],
  stats: null,
  isLoading: false,
  error: null,
  filters: {
    difficulty: '',
    tags: [],
    confidence: '',
    dueToday: false,
  },

  // Actions
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),

  setFilters: (filters) => set({ filters: { ...get().filters, ...filters } }),

  // Fetch all problems
  fetchProblems: async () => {
    set({ isLoading: true, error: null });
    try {
      const { filters } = get();
      const params = new URLSearchParams();
      
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.tags.length > 0) {
        filters.tags.forEach(tag => params.append('tags', tag));
      }
      
      const response = await axios.get(`/api/problems/?${params}`, {
        withCredentials: true,
      });
      
      set({ problems: response.data.results || response.data, isLoading: false });
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to fetch problems',
        isLoading: false 
      });
    }
  },

  // Fetch user's problems
  fetchUserProblems: async () => {
    set({ isLoading: true, error: null });
    try {
      const { filters } = get();
      const params = new URLSearchParams();
      
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.tags.length > 0) {
        filters.tags.forEach(tag => params.append('tags', tag));
      }
      if (filters.confidence) params.append('confidence', filters.confidence);
      if (filters.dueToday) params.append('due_today', 'true');
      
      const response = await axios.get(`/api/user/problems/?${params}`, {
        withCredentials: true,
      });
      
      set({ userProblems: response.data.results || response.data, isLoading: false });
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to fetch user problems',
        isLoading: false 
      });
    }
  },

  // Fetch dashboard problems (due today)
  fetchDashboard: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/dashboard/', {
        withCredentials: true,
      });
      
      set({ 
        dashboardProblems: response.data.due_today || [],
        isLoading: false 
      });
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to fetch dashboard',
        isLoading: false 
      });
    }
  },

  // Fetch user stats
  fetchStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/stats/', {
        withCredentials: true,
      });
      
      set({ stats: response.data, isLoading: false });
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to fetch stats',
        isLoading: false 
      });
    }
  },

  // Add problem to user's list
  addUserProblem: async (problemId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/api/user/problems/', {
        problem_id: problemId,
      }, {
        withCredentials: true,
      });
      
      // Refresh user problems
      await get().fetchUserProblems();
      set({ isLoading: false });
      return response.data;
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to add problem',
        isLoading: false 
      });
      throw error;
    }
  },

  // Update user problem (confidence/attempt)
  updateUserProblem: async (userProblemId, confidenceChange, solved = false) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch(`/api/user/problems/${userProblemId}/update/`, {
        confidence_change: confidenceChange,
        solved: solved,
      }, {
        withCredentials: true,
      });
      
      // Update local state
      const { userProblems, dashboardProblems } = get();
      const updatedUserProblems = userProblems.map(up => 
        up.id === userProblemId ? response.data : up
      );
      const updatedDashboardProblems = dashboardProblems.map(up => 
        up.id === userProblemId ? response.data : up
      );
      
      set({ 
        userProblems: updatedUserProblems,
        dashboardProblems: updatedDashboardProblems,
        isLoading: false 
      });
      
      return response.data;
    } catch (error) {
      set({ 
        error: error.response?.data?.message || 'Failed to update problem',
        isLoading: false 
      });
      throw error;
    }
  },

  // Quick actions for dashboard
  markSolved: async (userProblemId) => {
    return get().updateUserProblem(userProblemId, 20, true);
  },

  markStruggling: async (userProblemId) => {
    return get().updateUserProblem(userProblemId, -10, false);
  },
}));

export default useProblemStore;
