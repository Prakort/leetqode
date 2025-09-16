import React, { useEffect } from 'react';
import { BarChart3, Calendar, Target, TrendingUp } from 'lucide-react';
import useProblemStore from '../store/problemStore';
import useAuthStore from '../store/authStore';
import ProblemCard from '../components/ProblemCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const { dashboardProblems, stats, isLoading, error, fetchDashboard, fetchStats } = useProblemStore();
  const { user } = useAuthStore();

  useEffect(() => {
    fetchDashboard();
    fetchStats();
  }, [fetchDashboard, fetchStats]);

  if (isLoading && !dashboardProblems.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => {
              fetchDashboard();
              fetchStats();
            }}
            className="btn btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.first_name || 'Coder'}!
        </h1>
        <p className="mt-2 text-gray-600">
          Here's your practice overview for today.
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Calendar className="w-8 h-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Due Today</p>
                <p className="text-2xl font-bold text-gray-900">{stats.due_today}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Target className="w-8 h-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Problems</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_problems}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="w-8 h-8 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Solved</p>
                <p className="text-2xl font-bold text-gray-900">{stats.solved_problems}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="w-8 h-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Confidence</p>
                <p className="text-2xl font-bold text-gray-900">
                  {Math.round(stats.average_confidence)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Difficulty Breakdown */}
      {stats?.difficulty_breakdown && (
        <div className="card mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Difficulty Breakdown</h3>
          <div className="grid grid-cols-3 gap-4">
            {Object.entries(stats.difficulty_breakdown).map(([difficulty, count]) => (
              <div key={difficulty} className="text-center">
                <div className={`badge ${
                  difficulty === 'Easy' ? 'badge-easy' :
                  difficulty === 'Medium' ? 'badge-medium' : 'badge-danger'
                } mb-2`}>
                  {difficulty}
                </div>
                <p className="text-2xl font-bold text-gray-900">{count}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Problems Due Today */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Problems Due Today</h2>
          <span className="text-sm text-gray-600">
            {dashboardProblems.length} problem{dashboardProblems.length !== 1 ? 's' : ''}
          </span>
        </div>

        {dashboardProblems.length === 0 ? (
          <div className="card text-center py-12">
            <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No problems due today!
            </h3>
            <p className="text-gray-600 mb-4">
              Great job! You're all caught up with your practice schedule.
            </p>
            <a
              href="/problems"
              className="btn btn-primary"
            >
              Browse Problems
            </a>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dashboardProblems.map((userProblem) => (
              <ProblemCard
                key={userProblem.id}
                userProblem={userProblem}
                showActions={true}
                isDashboard={true}
              />
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="flex flex-wrap gap-4">
          <a
            href="/problems"
            className="btn btn-primary"
          >
            Browse All Problems
          </a>
          <button
            onClick={() => {
              fetchDashboard();
              fetchStats();
            }}
            className="btn btn-secondary"
            disabled={isLoading}
          >
            {isLoading ? <LoadingSpinner size="sm" /> : 'Refresh'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
