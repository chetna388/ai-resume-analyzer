import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import resumeService from '../services/resumeService';
import LoadingSpinner from '../components/LoadingSpinner';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await resumeService.getHistory();
        setHistory(data.analyses || []);
      } catch (err) {
        setError('Failed to load analysis history');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in-up">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-display font-bold text-white">Analysis History</h1>
          <p className="text-slate-400 mt-1">Review your past resume analyses ({history.length})</p>
        </div>
        <Link to="/upload" className="btn-primary py-2 px-4">
          + New Analysis
        </Link>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-8">
          {error}
        </div>
      )}

      {history.length === 0 && !loading && !error ? (
        <div className="glass-card p-12 text-center flex flex-col items-center justify-center">
          <div className="text-6xl mb-4">📭</div>
          <h2 className="text-2xl font-bold text-white mb-2">No History Yet</h2>
          <p className="text-slate-400 mb-6 max-w-md">You haven't analyzed any resumes yet. Upload your first resume to get started!</p>
          <Link to="/upload" className="btn-primary px-8 py-3">Analyze Your First Resume</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {history.map((item, idx) => {
            const date = new Date(item.created_at).toLocaleDateString();
            const scoreColor = item.ats_score >= 80 ? 'text-green-400 bg-green-400/10 border-green-400/20' : 
                               item.ats_score >= 60 ? 'text-teal-400 bg-teal-400/10 border-teal-400/20' : 
                               item.ats_score >= 40 ? 'text-amber-400 bg-amber-400/10 border-amber-400/20' : 
                               'text-red-400 bg-red-400/10 border-red-400/20';
            
            return (
              <div key={item.id || idx} className="glass-card p-6 flex flex-col hover:border-indigo-500/50 transition-colors animate-fade-in-up" style={{ animationDelay: `${idx * 0.05}s` }}>
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">📄</span>
                    <h3 className="font-semibold text-white truncate max-w-[150px]" title={item.filename}>
                      {item.filename || 'Resume'}
                    </h3>
                  </div>
                  <span className="text-xs text-slate-500">{date}</span>
                </div>
                
                <div className="mb-4">
                  <span className="inline-block px-3 py-1 rounded-full text-xs font-medium bg-slate-800 border border-slate-700 text-indigo-300 mb-2">
                    {item.category}
                  </span>
                </div>

                <div className="mt-auto flex justify-between items-center pt-4 border-t border-slate-700/50">
                  <div className={`px-3 py-1 rounded-lg border font-bold ${scoreColor}`}>
                    Score: {item.ats_score}
                  </div>
                  <div className="text-slate-300 font-medium text-sm">
                    Grade: <span className="text-white">{item.grade}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;
