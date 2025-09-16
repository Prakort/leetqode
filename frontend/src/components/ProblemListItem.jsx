import React from 'react';
import { ExternalLink, CheckCircle, XCircle, Clock, Plus } from 'lucide-react';
import useProblemStore from '../store/problemStore';

const ProblemListItem = ({ userProblem, problem, showActions = true }) => {
  const { markSolved, markStruggling, addUserProblem } = useProblemStore();
  const problemData = problem || userProblem?.problem || userProblem;

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-600 bg-green-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'Hard': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'bg-green-500';
    if (confidence >= 60) return 'bg-yellow-500';
    if (confidence >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

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

  const companyTags = ['Amazon', 'Google', 'Microsoft', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'];
  const problemCompanyTags = problemData.tags?.filter(tag => companyTags.includes(tag)) || [];
  const otherTags = problemData.tags?.filter(tag => !companyTags.includes(tag)) || [];

  const handleAddToPractice = async () => {
    try {
      await addUserProblem(problemData.id);
    } catch (error) {
      console.error('Failed to add problem:', error);
      alert(`Failed to add problem: ${error.response?.data?.message || error.message}`);
    }
  };

  const handleSolved = async () => {
    try {
      await markSolved(userProblem.id);
    } catch (error) {
      console.error('Failed to mark as solved:', error);
    }
  };

  const handleStruggling = async () => {
    try {
      await markStruggling(userProblem.id);
    } catch (error) {
      console.error('Failed to mark as struggling:', error);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return 'Overdue';
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Tomorrow';
    return `In ${diffDays} days`;
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        {/* Problem Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3 mb-2">
            <span className="text-sm font-medium text-gray-500 w-8">
              #{problemData.id}
            </span>
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {problemData.title}
            </h3>
            <a
              href={problemData.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 flex-shrink-0"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
          
          <div className="flex items-center space-x-2 mb-2 flex-wrap">
            {/* Difficulty */}
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(problemData.difficulty)}`}>
              {problemData.difficulty}
            </span>
            
            {/* Company Tags */}
            {problemCompanyTags.map((tag, index) => (
              <span key={index} className={`px-2 py-1 text-xs font-medium rounded-full border ${getCompanyTagColor(tag)}`}>
                {tag}
              </span>
            ))}
            
            {/* Other Tags */}
            {otherTags.slice(0, 3).map((tag, index) => (
              <span key={index} className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                {tag}
              </span>
            ))}
            {otherTags.length > 3 && (
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                +{otherTags.length - 3} more
              </span>
            )}
          </div>

          {/* User Progress (if userProblem exists) */}
          {userProblem && (
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <span>Confidence:</span>
                <div className="flex items-center space-x-1">
                  <div className="w-16 bg-gray-200 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full transition-all duration-300 ${getConfidenceColor(userProblem.confidence)}`}
                      style={{ width: `${userProblem.confidence}%` }}
                    ></div>
                  </div>
                  <span className="font-medium">{userProblem.confidence}%</span>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>Due: {formatDate(userProblem.next_due)}</span>
              </div>
              <div>
                <span>Attempts: </span>
                <span className="font-medium">{userProblem.attempts_count}</span>
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        {showActions && (
          <div className="flex items-center space-x-2 ml-4">
            {userProblem ? (
              <>
                <button
                  onClick={handleSolved}
                  className="flex items-center space-x-1 px-3 py-1.5 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 transition-colors"
                >
                  <CheckCircle className="w-4 h-4" />
                  <span>Solved</span>
                </button>
                <button
                  onClick={handleStruggling}
                  className="flex items-center space-x-1 px-3 py-1.5 bg-yellow-600 text-white text-sm font-medium rounded-md hover:bg-yellow-700 transition-colors"
                >
                  <XCircle className="w-4 h-4" />
                  <span>Struggling</span>
                </button>
              </>
            ) : (
              <button
                onClick={handleAddToPractice}
                className="flex items-center space-x-1 px-3 py-1.5 bg-primary-600 text-white text-sm font-medium rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Plus className="w-4 h-4" />
                <span>Add to Practice</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProblemListItem;
