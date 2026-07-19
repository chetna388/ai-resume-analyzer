import React from 'react';

const LoadingSpinner = ({ fullPage = false, message = 'Loading...', size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24'
  };

  const spinner = (
    <div className="flex flex-col items-center justify-center">
      <div className="relative">
        <div className={`${sizeClasses[size]} rounded-full border-4 border-slate-700/50`}></div>
        <div className={`absolute top-0 left-0 ${sizeClasses[size]} rounded-full border-4 border-indigo-500 border-t-transparent animate-spin`}></div>
        <div className={`absolute top-0 left-0 ${sizeClasses[size]} rounded-full border-4 border-teal-400 border-b-transparent animate-[spin_1.5s_linear_infinite_reverse] opacity-50`}></div>
      </div>
      {message && (
        <p className="mt-4 text-sm font-medium bg-gradient-to-r from-indigo-400 to-teal-400 bg-clip-text text-transparent animate-pulse">
          {message}
        </p>
      )}
    </div>
  );

  if (fullPage) {
    return (
      <div className="fixed inset-0 bg-[#0f172a]/80 backdrop-blur-sm z-50 flex items-center justify-center">
        {spinner}
      </div>
    );
  }

  return <div className="p-8 flex justify-center w-full">{spinner}</div>;
};

export default LoadingSpinner;
