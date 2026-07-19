import React from 'react';

const SkillCard = ({ title, skills = [], type = 'found', icon = '🎯' }) => {
  let chipClass = 'skill-chip';
  let badgeClass = 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
  
  if (type === 'missing') {
    chipClass += ' missing';
    badgeClass = 'bg-red-500/20 text-red-400 border-red-500/30';
  } else if (type === 'matched') {
    chipClass += ' matched';
    badgeClass = 'bg-teal-500/20 text-teal-400 border-teal-500/30';
  }

  return (
    <div className="glass-card p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <span>{icon}</span> {title}
        </h3>
        <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${badgeClass}`}>
          {skills.length}
        </span>
      </div>
      
      <div className="flex flex-wrap gap-2 mt-auto">
        {skills.length > 0 ? (
          skills.map((skill, idx) => (
            <span key={idx} className={chipClass}>
              {skill}
            </span>
          ))
        ) : (
          <p className="text-slate-400 text-sm italic w-full text-center py-4">None detected</p>
        )}
      </div>
    </div>
  );
};

export default SkillCard;
