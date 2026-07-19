import React from 'react';

const Footer = () => {
  return (
    <footer className="mt-auto py-8 border-t border-indigo-500/20 bg-slate-900/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center">
        <div className="text-slate-400 text-sm mb-4 md:mb-0">
          &copy; {new Date().getFullYear()} AI Resume Analyzer. All rights reserved.
        </div>
        <div className="flex items-center space-x-4 text-sm text-slate-500">
          <span>Built with</span>
          <span className="px-2 py-1 bg-slate-800 rounded-md text-indigo-400">React</span>
          <span className="px-2 py-1 bg-slate-800 rounded-md text-teal-400">Tailwind</span>
          <span className="px-2 py-1 bg-slate-800 rounded-md text-purple-400">Python</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
