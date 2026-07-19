import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import resumeService from '../services/resumeService';
import LoadingSpinner from '../components/LoadingSpinner';

const DashboardPage = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [historyData, profileData] = await Promise.all([
          resumeService.getHistory(),
          resumeService.getProfile()
        ]);
        
        setHistory(historyData.analyses || []);
        setStats(profileData.stats || null);
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <LoadingSpinner fullPage message="Loading dashboard..." />;

  const recentAnalyses = history.slice(0, 5);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in-up">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-white">
            Welcome back, <span className="gradient-text">{user?.username || 'User'}</span>
          </h1>
          <p className="text-slate-400 mt-1">Here's your resume analysis overview.</p>
        </div>
        <Link to="/upload" className="btn-primary shadow-[0_0_20px_rgba(99,102,241,0.3)]">
          + New Analysis
        </Link>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-8">
          {error}
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <div className="glass-card p-6 border-t-4 border-t-indigo-500 stagger-1">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Total Analyses</p>
              <h3 className="text-3xl font-bold text-white mt-2">{stats?.total_analyses || history.length || 0}</h3>
            </div>
            <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400">📄</div>
          </div>
        </div>
        <div className="glass-card p-6 border-t-4 border-t-teal-500 stagger-2">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Avg ATS Score</p>
              <h3 className="text-3xl font-bold text-white mt-2">{stats?.avg_ats_score || '--'}</h3>
            </div>
            <div className="p-3 rounded-xl bg-teal-500/10 text-teal-400">📊</div>
          </div>
        </div>
        <div className="glass-card p-6 border-t-4 border-t-purple-500 stagger-3">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Top Category</p>
              <h3 className="text-xl font-bold text-white mt-2 break-words">{stats?.most_common_category || 'N/A'}</h3>
            </div>
            <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400">🎯</div>
          </div>
        </div>
        <div className="glass-card p-6 border-t-4 border-t-amber-500 stagger-4">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-slate-400">Best Score</p>
              <h3 className="text-3xl font-bold text-white mt-2">{stats?.best_score || '--'}</h3>
            </div>
            <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400">⭐</div>
          </div>
        </div>
      </div>

      {/* Recent Activity & Tips */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-white">Recent Analyses</h2>
            <Link to="/history" className="text-indigo-400 text-sm hover:text-indigo-300 font-medium transition-colors">
              View All
            </Link>
          </div>
          
          <div className="glass-card overflow-hidden">
            {recentAnalyses.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-800/50 border-b border-slate-700">
                      <th className="px-6 py-4 text-sm font-semibold text-slate-300">File / Date</th>
                      <th className="px-6 py-4 text-sm font-semibold text-slate-300">Category</th>
                      <th className="px-6 py-4 text-sm font-semibold text-slate-300">Score</th>
                      <th className="px-6 py-4 text-sm font-semibold text-slate-300">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentAnalyses.map((item, idx) => (
                      <tr key={item.id || idx} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="font-medium text-white flex items-center gap-2">
                            <span className="text-red-400 text-lg">📄</span> {item.filename || `Resume_${item.id}`}
                          </div>
                          <div className="text-xs text-slate-500 mt-1">
                            {new Date(item.created_at).toLocaleDateString()}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800 border border-slate-700 text-indigo-300">
                            {item.category}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`font-bold ${
                            item.ats_score >= 80 ? 'text-green-400' :
                            item.ats_score >= 60 ? 'text-teal-400' :
                            item.ats_score >= 40 ? 'text-amber-400' : 'text-red-400'
                          }`}>
                            {item.ats_score} / 100
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <Link 
                            to={`/history`} // Simplified for now, ideally links to specific result
                            className="text-indigo-400 hover:text-indigo-300 text-sm font-medium"
                          >
                            View Details
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="p-10 text-center flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center text-2xl mb-4">
                  📊
                </div>
                <h3 className="text-lg font-medium text-white mb-2">No analyses yet</h3>
                <p className="text-slate-400 text-sm mb-6 max-w-sm">Upload your first resume to get detailed AI-powered insights and an ATS score.</p>
                <Link to="/upload" className="btn-primary py-2 px-6">
                  Analyze Resume
                </Link>
              </div>
            )}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-bold text-white mb-4">Pro Tips</h2>
          <div className="glass-card p-6 bg-gradient-to-br from-indigo-900/20 to-purple-900/20">
            <ul className="space-y-6">
              <li className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 shrink-0">
                  💡
                </div>
                <div>
                  <h4 className="text-white font-medium mb-1">Tailor your resume</h4>
                  <p className="text-sm text-slate-400">Always customize your resume for the specific job description to beat the ATS.</p>
                </div>
              </li>
              <li className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-teal-500/20 flex items-center justify-center text-teal-400 shrink-0">
                  🎯
                </div>
                <div>
                  <h4 className="text-white font-medium mb-1">Use action verbs</h4>
                  <p className="text-sm text-slate-400">Start bullet points with strong action verbs like "Spearheaded", "Optimized", or "Architected".</p>
                </div>
              </li>
              <li className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-400 shrink-0">
                  📈
                </div>
                <div>
                  <h4 className="text-white font-medium mb-1">Quantify results</h4>
                  <p className="text-sm text-slate-400">Use numbers and metrics (%, $, time) to demonstrate your impact and achievements.</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
