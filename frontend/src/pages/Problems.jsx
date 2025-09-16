import React, { useEffect, useState } from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import useProblemStore from '../store/problemStore';
import ProblemCard from '../components/ProblemCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Problems = () => {
  const {
    problems,
    userProblems,
    isLoading,
    error,
    filters,
    fetchProblems,
    fetchUserProblems,
    setFilters,
  } = useProblemStore();

  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    fetchProblems();
    fetchUserProblems();
  }, [fetchProblems, fetchUserProblems]);

  // Create a map of user problems for quick lookup
  const userProblemMap = new Map();
  userProblems.forEach(up => {
    userProblemMap.set(up.problem.id, up);
  });

  // Filter problems based on search term and filters
  const filteredProblems = problems.filter(problem => {
    const matchesSearch = problem.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         problem.id.toString().includes(searchTerm);
    
    const matchesDifficulty = !filters.difficulty || problem.difficulty === filters.difficulty;
    
    const matchesTags = filters.tags.length === 0 || 
                       filters.tags.some(tag => problem.tags.includes(tag));
    
    return matchesSearch && matchesDifficulty && matchesTags;
  });

  const availableTags = [...new Set(problems.flatMap(p => p.tags))].sort();

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

  const clearFilters = () => {
    setFilters({ difficulty: '', tags: [], confidence: '', dueToday: false });
    setSearchTerm('');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Problems</h1>
        <p className="mt-2 text-gray-600">
          Practice LeetCode problems with confidence tracking and spaced repetition.
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
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProblems.map((problem) => {
                const userProblem = userProblemMap.get(problem.id);
                return (
                  <ProblemCard
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
