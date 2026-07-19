import React, { useState } from 'react';

const ImprovementCard = ({ title, suggestions = [], priority = 'Medium', icon = '💡' }) => {
  const [expanded, setExpanded] = useState(false);
  
  let priorityColor = 'text-amber-400 border-amber-500/30 bg-amber-500/10';
  if (priority.toLowerCase() === 'high') {
    priorityColor = 'text-red-400 border-red-500/30 bg-red-500/10';
  } else if (priority.toLowerCase() === 'low') {
    priorityColor = 'text-green-400 border-green-500/30 bg-green-500/10';
  }

  const displayCount = expanded ? suggestions.length : Math.min(3, suggestions.length);

  return (
    <div className="glass-card p-5 mb-4 hover:border-indigo-500/30 transition-colors">
      <div className="flex justify-between items-start mb-3">
        <h4 className="text-md font-semibold text-white flex items-center gap-2">
          <span>{icon}</span> {title}
        </h4>
        <span className={`text-xs px-2 py-1 rounded-md border font-medium ${priorityColor}`}>
          {priority} Priority
        </span>
      </div>
      
      <ul className="space-y-2 mt-3">
        {suggestions.slice(0, displayCount).map((item, idx) => (
          <li key={idx} className="flex items-start text-sm text-slate-300 animate-fade-in-up" style={{ animationDelay: `${idx * 0.1}s` }}>
            <span className="text-indigo-400 mr-2 mt-0.5">•</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
      
      {suggestions.length > 3 && (
        <button 
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-indigo-400 hover:text-indigo-300 mt-4 font-medium transition-colors"
        >
          {expanded ? 'Show Less ↑' : `Show ${suggestions.length - 3} More ↓`}
        </button>
      )}
    </div>
  );
};

export default ImprovementCard;
