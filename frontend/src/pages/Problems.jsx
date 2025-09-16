import React, { useEffect, useState } from 'react';
import { Search, Filter } from 'lucide-react';
import useProblemStore from '../store/problemStore';
import ProblemListItem from '../components/ProblemListItem';
import LoadingSpinner from '../components/LoadingSpinner';

const Problems = () => {
  const {
    problems,
    userProblems,
    isLoading,
    error,
    searchTerm,
    filters,
    fetchProblems,
    fetchUserProblems,
    setFilters,
    setSearchTerm,
    clearFilters,
    getFilteredProblems,
  } = useProblemStore();

  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    // Only fetch if problems haven't been loaded yet
    if (problems.length === 0) {
      fetchProblems();
    }
    fetchUserProblems();
  }, [fetchProblems, fetchUserProblems, problems.length]);

  // Create a map of user problems for quick lookup
  const userProblemMap = new Map();
  userProblems.forEach(up => {
    userProblemMap.set(up.problem.id, up);
  });

  // Get filtered problems from store
  const filteredProblems = getFilteredProblems();

  const allTags = [...new Set(problems.flatMap(p => p.tags))].sort();
  const companyTags = ['Amazon', 'Google', 'Microsoft', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'];
  const availableTags = allTags.filter(tag => !companyTags.includes(tag));
  const availableCompanyTags = allTags.filter(tag => companyTags.includes(tag));

  const getCompanyTagColor = (company) => {
    const colors = {
      'Amazon': 'bg-orange-100 text-orange-800 border-orange-200',
      'Google': 'bg-blue-100 text-blue-800 border-blue-200',
      'Microsoft': 'bg-green-100 text-green-800 border-green-200',
      'Meta': 'bg-purple-100 text-purple-800 border-purple-200',
      'Apple': 'bg-gray-100 text-gray-800 border-gray-200',
      'Netflix': 'bg-red-100 text-red-800 border-red-200',
      'Uber': 'bg-black text-white border-black',
      'Airbnb': 'bg-pink-100 text-pink-800 border-pink-200',
    };
    return colors[company] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const handleFilterChange = (key, value) => {
    if (key === 'tags') {
      const newTags = filters.tags.includes(value)
        ? filters.tags.filter(tag => tag !== value)
        : [...filters.tags, value];
      setFilters({ tags: newTags });
    } else {
      setFilters({ [key]: value });
    }
  };


  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">All Problems</h1>
        <p className="mt-2 text-gray-600">
          Browse and practice all 100 LeetCode problems with confidence tracking and spaced repetition.
        </p>
      </div>

      {/* Search and Filters */}
      <div className="card mb-8">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search problems by title or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            <Filter className="w-4 h-4" />
            <span>Filters</span>
          </button>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {/* Difficulty Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Difficulty
                </label>
                <select
                  value={filters.difficulty}
                  onChange={(e) => handleFilterChange('difficulty', e.target.value)}
                  className="input"
                >
                  <option value="">All Difficulties</option>
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              {/* Company Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Company
                </label>
                <div className="max-h-32 overflow-y-auto space-y-1">
                  {availableCompanyTags.map(tag => (
                    <label key={tag} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={filters.tags.includes(tag)}
                        onChange={() => handleFilterChange('tags', tag)}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className={`text-sm px-2 py-1 rounded-full border ${getCompanyTagColor(tag)}`}>
                        {tag}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Tags Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tags
                </label>
                <div className="max-h-32 overflow-y-auto space-y-1">
                  {availableTags.map(tag => (
                    <label key={tag} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={filters.tags.includes(tag)}
                        onChange={() => handleFilterChange('tags', tag)}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-700">{tag}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-end">
                <button
                  onClick={clearFilters}
                  className="btn btn-secondary w-full"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Error State */}
      {error && (
        <div className="card mb-8">
          <div className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={() => {
                fetchProblems();
                fetchUserProblems();
              }}
              className="btn btn-primary"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !problems.length && (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      )}

      {/* Problems Grid */}
      {!isLoading && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-gray-600">
              Showing {filteredProblems.length} of {problems.length} problems
            </p>
            {filters.difficulty || filters.tags.length > 0 || searchTerm ? (
              <button
                onClick={clearFilters}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Clear all filters
              </button>
            ) : null}
          </div>

          {filteredProblems.length === 0 ? (
            <div className="card text-center py-12">
              <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No problems found
              </h3>
              <p className="text-gray-600 mb-4">
                Try adjusting your search terms or filters.
              </p>
              <button
                onClick={clearFilters}
                className="btn btn-primary"
              >
                Clear Filters
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredProblems.map((problem) => {
                const userProblem = userProblemMap.get(problem.id);
                return (
                  <ProblemListItem
                    key={problem.id}
                    userProblem={userProblem}
                    problem={problem}
                    showActions={true}
                  />
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Problems;
