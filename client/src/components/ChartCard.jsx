import React from 'react';

const ChartCard = ({ title, children, description, icon = '📊' }) => {
  return (
    <div className="glass-card p-6 h-full flex flex-col">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <span>{icon}</span> {title}
        </h3>
        {description && <p className="text-sm text-slate-400 mt-1">{description}</p>}
      </div>
      <div className="flex-1 w-full min-h-[300px] flex items-center justify-center">
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
