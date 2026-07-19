import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import resumeService from '../services/resumeService';
import LoadingSpinner from '../components/LoadingSpinner';

const ProfilePage = () => {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await resumeService.getProfile();
        setProfileData(data);
      } catch (err) {
        setError('Failed to load profile data');
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) return <LoadingSpinner fullPage />;

  const stats = profileData?.stats || {};
  const joinDate = user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Recently';

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in-up">
      <h1 className="text-3xl font-display font-bold text-white mb-8">Your Profile</h1>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-8">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* User Info Card */}
        <div className="md:col-span-1">
          <div className="glass-card p-8 text-center flex flex-col items-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-4xl text-white font-bold mb-4 shadow-[0_0_30px_rgba(99,102,241,0.4)]">
              {user?.username ? user.username.charAt(0).toUpperCase() : 'U'}
            </div>
            <h2 className="text-xl font-bold text-white mb-1">{user?.username}</h2>
            <p className="text-sm text-slate-400 mb-4">{user?.email}</p>
            <div className="w-full pt-4 border-t border-slate-700/50">
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Member Since</p>
              <p className="text-sm text-slate-300 mt-1">{joinDate}</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="md:col-span-2 space-y-6">
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <span>📊</span> Analytics Overview
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
                <p className="text-sm text-slate-400 font-medium">Total Resumes Analyzed</p>
                <p className="text-2xl font-bold text-white mt-1">{stats.total_analyses || 0}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
                <p className="text-sm text-slate-400 font-medium">Average ATS Score</p>
                <p className="text-2xl font-bold text-teal-400 mt-1">{stats.avg_ats_score || '--'}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
                <p className="text-sm text-slate-400 font-medium">Highest Score</p>
                <p className="text-2xl font-bold text-indigo-400 mt-1">{stats.best_score || '--'}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
                <p className="text-sm text-slate-400 font-medium">Most Common Category</p>
                <p className="text-lg font-bold text-purple-400 mt-1 truncate">{stats.most_common_category || 'N/A'}</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-6 bg-gradient-to-r from-indigo-900/20 to-transparent border-l-4 border-l-indigo-500">
            <h3 className="text-white font-bold mb-2">Account Settings</h3>
            <p className="text-sm text-slate-400 mb-4">Manage your personal information and preferences.</p>
            <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg border border-slate-600 transition-colors text-sm font-medium disabled:opacity-50" disabled>
              Edit Profile (Coming Soon)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
