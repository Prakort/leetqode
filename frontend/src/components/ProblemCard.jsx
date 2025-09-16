import React from 'react';
import { ExternalLink, CheckCircle, XCircle, Clock } from 'lucide-react';
import useProblemStore from '../store/problemStore';

const ProblemCard = ({ userProblem, problem, showActions = true, isDashboard = false }) => {
  const { markSolved, markStruggling, addUserProblem } = useProblemStore();
  const problemData = problem || userProblem?.problem || userProblem;

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy': return 'badge-easy';
      case 'Medium': return 'badge-medium';
      case 'Hard': return 'badge-danger';
      default: return 'badge-secondary';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'bg-success-500';
    if (confidence >= 60) return 'bg-warning-500';
    if (confidence >= 40) return 'bg-orange-500';
    return 'bg-danger-500';
  };

  const handleAddToPractice = async () => {
    try {
      await addUserProblem(problemData.id);
    } catch (error) {
      console.error('Failed to add problem:', error);
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
    <div className="card hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {problemData.id}. {problemData.title}
            </h3>
            <a
              href={problemData.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
          
          <div className="flex items-center space-x-2 mb-3">
            <span className={`badge ${getDifficultyColor(problemData.difficulty)}`}>
              {problemData.difficulty}
            </span>
            {problemData.tags?.map((tag, index) => (
              <span key={index} className="badge bg-gray-100 text-gray-800">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* User Progress (if userProblem exists) */}
      {userProblem && (
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Confidence</span>
            <span className="text-sm text-gray-600">{userProblem.confidence}%</span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${getConfidenceColor(userProblem.confidence)}`}
              style={{ width: `${userProblem.confidence}%` }}
            ></div>
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center space-x-1">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="text-gray-600">Next due:</span>
              <span className="font-medium">{formatDate(userProblem.next_due)}</span>
            </div>
            <div className="text-gray-600">
              <span>Attempts: </span>
              <span className="font-medium">{userProblem.attempts_count}</span>
            </div>
          </div>
        </div>
      )}

      {/* Actions */}
      {showActions && (
        <div className="flex space-x-2">
          {userProblem ? (
            <>
              <button
                onClick={handleSolved}
                className="btn btn-success flex-1 flex items-center justify-center space-x-1"
              >
                <CheckCircle className="w-4 h-4" />
                <span>Solved</span>
              </button>
              <button
                onClick={handleStruggling}
                className="btn btn-warning flex-1 flex items-center justify-center space-x-1"
              >
                <XCircle className="w-4 h-4" />
                <span>Struggling</span>
              </button>
            </>
          ) : (
            <button
              onClick={handleAddToPractice}
              className="btn btn-primary w-full"
            >
              Add to Practice
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ProblemCard;
