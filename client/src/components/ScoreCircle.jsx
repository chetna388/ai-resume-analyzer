import React, { useEffect, useState } from 'react';

const ScoreCircle = ({ score, size = 120, label, grade }) => {
  const [animatedScore, setAnimatedScore] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const strokeWidth = size * 0.08;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  let colorClass = 'text-green-500';
  let glowColor = 'rgba(34, 197, 94, 0.4)';
  if (score < 40) {
    colorClass = 'text-red-500';
    glowColor = 'rgba(239, 68, 68, 0.4)';
  } else if (score < 60) {
    colorClass = 'text-amber-500';
    glowColor = 'rgba(245, 158, 11, 0.4)';
  } else if (score < 80) {
    colorClass = 'text-teal-500';
    glowColor = 'rgba(20, 184, 166, 0.4)';
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div 
        className="relative flex items-center justify-center rounded-full"
        style={{ width: size, height: size, boxShadow: `0 0 30px ${glowColor}` }}
      >
        <svg className="transform -rotate-90 w-full h-full">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            className="text-slate-700"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={`${colorClass} transition-all duration-1000 ease-out`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-bold font-display text-white">{Math.round(animatedScore)}</span>
          {grade && <span className={`text-sm font-semibold ${colorClass}`}>Grade: {grade}</span>}
        </div>
      </div>
      {label && <span className="mt-4 text-slate-300 font-medium">{label}</span>}
    </div>
  );
};

export default ScoreCircle;
