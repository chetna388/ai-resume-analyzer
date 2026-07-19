import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { jsPDF } from 'jspdf';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
  PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import ScoreCircle from '../components/ScoreCircle';
import SkillCard from '../components/SkillCard';
import ChartCard from '../components/ChartCard';
import ImprovementCard from '../components/ImprovementCard';
import LoadingSpinner from '../components/LoadingSpinner';

const COLORS = ['#6366f1', '#14b8a6', '#f59e0b', '#8b5cf6', '#ec4899', '#3b82f6', '#10b981', '#f97316'];

const AnalysisResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('skills');
  const [expandedQ, setExpandedQ] = useState(null);

  useEffect(() => {
    if (location.state?.result) {
      setResult(location.state.result);
      localStorage.setItem('lastAnalysis', JSON.stringify(location.state.result));
    } else {
      const saved = localStorage.getItem('lastAnalysis');
      if (saved) {
        setResult(JSON.parse(saved));
      } else {
        navigate('/upload');
      }
    }
  }, [location, navigate]);

  if (!result) return <LoadingSpinner fullPage />;

  const {
    category = 'Unknown',
    confidence = 0,
    ats_score = 0,
    grade = 'N/A',
    strength = 'N/A',
    matching_percentage = 0,
    skills_found = [],
    skills_by_category = {},
    missing_skills = [],
    recommendations = {},
    interview_questions = [],
    score_breakdown = {},
    resume_stats = {}
  } = result;

  // --- Chart Data Preparation ---

  // Radar chart from score_breakdown
  const radarData = [
    { subject: 'Similarity', A: score_breakdown?.similarity?.score || 0, fullMark: 100 },
    { subject: 'Skills', A: score_breakdown?.skill_match?.score || 0, fullMark: 100 },
    { subject: 'Structure', A: score_breakdown?.resume_structure?.score || 0, fullMark: 100 },
    { subject: 'Projects', A: score_breakdown?.project_relevance?.score || 0, fullMark: 100 },
    { subject: 'Keywords', A: score_breakdown?.keyword_presence?.score || 0, fullMark: 100 },
  ];

  // Bar chart for weighted breakdown
  const breakdownData = Object.entries(score_breakdown || {}).map(([key, val]) => ({
    name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    score: val?.weighted_score || 0,
    raw: val?.score || 0,
    weight: val?.weight || 0,
  }));

  // Pie chart from skills_by_category
  const pieData = Object.entries(skills_by_category || {}).length > 0
    ? Object.entries(skills_by_category).map(([name, skills]) => ({
        name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        value: Array.isArray(skills) ? skills.length : 0,
      }))
    : [
        { name: 'Languages', value: skills_found.filter(s => ['Python','Java','JavaScript','C++','C#','TypeScript','Go','SQL','HTML','CSS','R','Ruby','PHP','Kotlin','Swift'].map(x => x.toLowerCase()).includes(s.toLowerCase())).length || 1 },
        { name: 'Frameworks', value: skills_found.filter(s => ['React','Node.js','Django','Flask','Spring Boot','Angular','Vue.js','Express.js','Next.js','FastAPI'].map(x => x.toLowerCase()).includes(s.toLowerCase())).length || 1 },
        { name: 'DevOps/Cloud', value: skills_found.filter(s => ['Docker','AWS','Azure','GCP','Kubernetes','Jenkins','Terraform','CI/CD','Linux'].map(x => x.toLowerCase()).includes(s.toLowerCase())).length || 0 },
        { name: 'ML/AI', value: skills_found.filter(s => ['TensorFlow','PyTorch','Scikit-learn','Pandas','NumPy','Machine Learning','Deep Learning','NLP'].map(x => x.toLowerCase()).includes(s.toLowerCase())).length || 0 },
        { name: 'Tools', value: skills_found.filter(s => ['Git','GitHub','Jira','VS Code','REST API','GraphQL','Postman'].map(x => x.toLowerCase()).includes(s.toLowerCase())).length || 1 },
      ].filter(d => d.value > 0);

  // --- Recommendation Tabs ---
  const recTabs = [
    { key: 'skills', label: '🔧 Missing Skills', data: recommendations?.missing_skills || [] },
    { key: 'courses', label: '📚 Courses', data: recommendations?.courses || [] },
    { key: 'projects', label: '💡 Projects', data: recommendations?.project_suggestions || [] },
    { key: 'certs', label: '🏆 Certifications', data: recommendations?.certifications || [] },
    { key: 'tips', label: '📝 Resume Tips', data: recommendations?.weak_sections || [] },
  ];

  const activeRecData = recTabs.find(t => t.key === activeTab)?.data || [];

  // --- PDF Generation ---
  const generatePDF = () => {
    const doc = new jsPDF();
    doc.setFont("helvetica");

    // Title
    doc.setFontSize(22);
    doc.setTextColor(79, 70, 229);
    doc.text("AI Resume Analysis Report", 20, 20);

    doc.setFontSize(10);
    doc.setTextColor(120, 120, 120);
    doc.text(`Generated on ${new Date().toLocaleString()}`, 20, 28);

    // Divider
    doc.setDrawColor(99, 102, 241);
    doc.line(20, 32, 190, 32);

    // Overview
    doc.setFontSize(16);
    doc.setTextColor(30, 41, 59);
    doc.text("Overview", 20, 42);

    doc.setFontSize(11);
    doc.setTextColor(60, 60, 60);
    doc.text(`Predicted Category: ${category}`, 20, 52);
    doc.text(`Confidence: ${(confidence * 100).toFixed(1)}%`, 20, 59);
    doc.text(`ATS Score: ${ats_score}/100 (Grade: ${grade})`, 20, 66);
    doc.text(`Strength: ${strength}`, 20, 73);
    doc.text(`Matching Percentage: ${matching_percentage}%`, 20, 80);

    // Skills Found
    let yPos = 95;
    doc.setFontSize(14);
    doc.setTextColor(30, 41, 59);
    doc.text("Skills Found", 20, yPos);
    yPos += 8;
    doc.setFontSize(10);
    doc.setTextColor(60, 60, 60);
    if (skills_found.length > 0) {
      const skillText = doc.splitTextToSize(skills_found.join(', '), 170);
      doc.text(skillText, 20, yPos);
      yPos += skillText.length * 5 + 5;
    } else {
      doc.text("No skills detected.", 20, yPos);
      yPos += 8;
    }

    // Missing Skills
    if (missing_skills.length > 0) {
      yPos += 5;
      doc.setFontSize(14);
      doc.setTextColor(30, 41, 59);
      doc.text("Missing Skills", 20, yPos);
      yPos += 8;
      doc.setFontSize(10);
      doc.setTextColor(180, 60, 60);
      const missingText = doc.splitTextToSize(missing_skills.join(', '), 170);
      doc.text(missingText, 20, yPos);
      yPos += missingText.length * 5 + 5;
    }

    // Score Breakdown
    if (Object.keys(score_breakdown).length > 0) {
      if (yPos > 230) { doc.addPage(); yPos = 20; }
      yPos += 5;
      doc.setFontSize(14);
      doc.setTextColor(30, 41, 59);
      doc.text("Score Breakdown", 20, yPos);
      yPos += 8;
      doc.setFontSize(10);
      doc.setTextColor(60, 60, 60);
      Object.entries(score_breakdown).forEach(([key, val]) => {
        if (yPos > 270) { doc.addPage(); yPos = 20; }
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        doc.text(`${label}: ${val?.score || 0}/100 (Weight: ${val?.weight || 0}%, Weighted: ${val?.weighted_score || 0})`, 20, yPos);
        yPos += 6;
      });
    }

    // Interview Questions
    if (interview_questions.length > 0) {
      if (yPos > 220) { doc.addPage(); yPos = 20; }
      yPos += 10;
      doc.setFontSize(14);
      doc.setTextColor(30, 41, 59);
      doc.text("Interview Prep Questions", 20, yPos);
      yPos += 8;
      doc.setFontSize(10);
      doc.setTextColor(60, 60, 60);
      interview_questions.forEach((q, i) => {
        if (yPos > 265) { doc.addPage(); yPos = 20; }
        const qText = doc.splitTextToSize(`Q${i + 1}: ${q.question}`, 170);
        doc.text(qText, 20, yPos);
        yPos += qText.length * 5 + 4;
      });
    }

    doc.save(`Resume_Analysis_${category.replace(/\s+/g, '_')}.pdf`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 animate-fade-in-up">
        <div>
          <h1 className="text-3xl font-display font-bold text-white">Analysis Results</h1>
          <p className="text-slate-400 mt-1">Comprehensive breakdown of your resume against the target role</p>
        </div>
        <div className="flex gap-3">
          <button onClick={generatePDF} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg border border-slate-600 transition-colors flex items-center gap-2">
            <span>📥</span> Download Report
          </button>
          <Link to="/upload" className="btn-primary py-2 px-4">
            ✨ New Analysis
          </Link>
        </div>
      </div>

      {/* ROW 1: Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Category Card */}
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center animate-fade-in-up stagger-1">
          <div className="text-4xl mb-3">🎯</div>
          <h3 className="text-slate-400 text-sm font-medium mb-1">Predicted Role</h3>
          <p className="text-xl font-bold text-white mb-2">{category}</p>
          <div className="w-full bg-slate-800 rounded-full h-2 mt-2">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-1000" style={{ width: `${confidence * 100}%` }}></div>
          </div>
          <p className="text-xs text-slate-500 mt-2">{(confidence * 100).toFixed(1)}% Confidence</p>
        </div>

        {/* ATS Score */}
        <div className="glass-card p-6 flex items-center justify-center animate-fade-in-up stagger-2">
          <ScoreCircle score={ats_score} label="ATS Score" grade={grade} size={140} />
        </div>

        {/* Matching Percentage */}
        <div className="glass-card p-6 flex items-center justify-center animate-fade-in-up stagger-3">
          <ScoreCircle score={Math.round(matching_percentage)} label="Skill Match" size={140} />
        </div>

        {/* Key Metrics */}
        <div className="glass-card p-6 flex flex-col justify-center animate-fade-in-up stagger-4">
          <h3 className="text-slate-400 text-sm font-medium mb-4 flex items-center gap-2">
            <span>📈</span> Key Metrics
          </h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Strength</span>
                <span className={`font-bold ${ats_score >= 70 ? 'text-teal-400' : ats_score >= 50 ? 'text-amber-400' : 'text-red-400'}`}>{strength}</span>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Skills Found</span>
                <span className="text-teal-400 font-bold">{skills_found.length}</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5">
                <div className="bg-teal-500 h-1.5 rounded-full transition-all duration-1000" style={{ width: `${Math.min(100, skills_found.length * 5)}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Missing Skills</span>
                <span className="text-red-400 font-bold">{missing_skills.length}</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5">
                <div className="bg-red-500 h-1.5 rounded-full transition-all duration-700" style={{ width: `${Math.min(100, missing_skills.length * 10)}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Words</span>
                <span className="text-slate-300 font-bold">{resume_stats?.word_count || 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ROW 2: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          <ChartCard title="Score Breakdown" description="Performance across 5 key dimensions">
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#475569', fontSize: 10 }} />
                <Radar name="Score" dataKey="A" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} strokeWidth={2} />
                <Tooltip contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.95)', border: '1px solid rgba(99,102,241,0.3)', borderRadius: '12px', color: '#e2e8f0' }} />
              </RadarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        <div className="animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
          <ChartCard title="Skill Distribution" description="Categories of your detected skills">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={4} dataKey="value" animationBegin={200} animationDuration={1000}>
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.95)', border: 'none', borderRadius: '12px', color: '#e2e8f0' }} />
                <Legend wrapperStyle={{ color: '#cbd5e1', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>
      </div>

      {/* Weighted Score Bar Chart */}
      {breakdownData.length > 0 && (
        <div className="mb-8 animate-fade-in-up" style={{ animationDelay: '0.45s' }}>
          <ChartCard title="Weighted Score Breakdown" description="Contribution of each factor to your total ATS score">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={breakdownData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis type="number" domain={[0, 50]} tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis type="category" dataKey="name" width={120} tick={{ fill: '#cbd5e1', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.95)', border: '1px solid rgba(99,102,241,0.3)', borderRadius: '12px', color: '#e2e8f0' }}
                  formatter={(value, name) => [`${value.toFixed(1)} pts`, name === 'score' ? 'Weighted Score' : name]}
                />
                <Bar dataKey="score" fill="#6366f1" radius={[0, 8, 8, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>
      )}

      {/* ROW 3: Skills */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="animate-fade-in-up" style={{ animationDelay: '0.5s' }}>
          <SkillCard
            title="Skills Detected"
            skills={skills_found}
            type="found"
          />
        </div>
        <div className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
          <SkillCard
            title="Missing Skills"
            skills={missing_skills}
            type="missing"
          />
        </div>
      </div>

      {/* ROW 4: Recommendations */}
      <div className="mb-10 animate-fade-in-up" style={{ animationDelay: '0.7s' }}>
        <h2 className="text-2xl font-display font-bold text-white mb-6 flex items-center gap-2">
          <span>🚀</span> Actionable Recommendations
        </h2>

        {/* Tabs */}
        <div className="flex space-x-1 bg-slate-800/50 rounded-xl p-1 mb-6 overflow-x-auto">
          {recTabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2.5 rounded-lg font-medium text-sm transition-all whitespace-nowrap ${
                activeTab === tab.key
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              {tab.label} ({tab.data.length})
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {activeTab === 'skills' && activeRecData.map((item, idx) => (
            <div key={idx} className="glass-card p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-white font-medium">{item.skill || item}</span>
                <span className={`text-xs px-2 py-1 rounded-full font-bold ${
                  item.importance === 'High' ? 'bg-red-500/20 text-red-400' :
                  item.importance === 'Medium' ? 'bg-amber-500/20 text-amber-400' :
                  'bg-green-500/20 text-green-400'
                }`}>{item.importance || 'Medium'}</span>
              </div>
            </div>
          ))}

          {activeTab === 'courses' && activeRecData.map((item, idx) => (
            <div key={idx} className="glass-card p-4">
              <h4 className="text-white font-medium mb-1">{item.course_name}</h4>
              <p className="text-sm text-slate-400 mb-2">For: <span className="text-indigo-400">{item.skill}</span></p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-500">{item.platform}</span>
                {item.url && (
                  <a href={item.url} target="_blank" rel="noopener noreferrer"
                     className="text-xs text-teal-400 hover:text-teal-300 transition-colors">
                    View Course →
                  </a>
                )}
              </div>
            </div>
          ))}

          {activeTab === 'projects' && activeRecData.map((item, idx) => (
            <div key={idx} className="glass-card p-4">
              <h4 className="text-white font-medium mb-2">💡 {item.title}</h4>
              <p className="text-sm text-slate-400 mb-3">{item.description}</p>
              <p className="text-xs text-indigo-400">Skills: {item.skills_demonstrated}</p>
            </div>
          ))}

          {activeTab === 'certs' && activeRecData.map((item, idx) => (
            <div key={idx} className="glass-card p-4">
              <h4 className="text-white font-medium mb-1">🏆 {item.name}</h4>
              <p className="text-sm text-slate-400">{item.provider}</p>
            </div>
          ))}

          {activeTab === 'tips' && activeRecData.map((item, idx) => (
            <ImprovementCard
              key={idx}
              title={item.section || 'Resume Tip'}
              suggestions={[item.suggestion || item.issue || '']}
              priority={item.issue ? 'High' : 'Medium'}
              icon="📝"
            />
          ))}

          {activeRecData.length === 0 && (
            <div className="col-span-full glass-card p-8 text-center text-slate-400">
              <p className="text-lg mb-2">✅ Looking good!</p>
              <p>No specific recommendations in this category.</p>
            </div>
          )}
        </div>
      </div>

      {/* ROW 5: Interview Questions */}
      {interview_questions && interview_questions.length > 0 && (
        <div className="mb-10 animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
          <h2 className="text-2xl font-display font-bold text-white mb-6 flex items-center gap-2">
            <span>🎙️</span> Interview Prep Questions
          </h2>
          <div className="glass-card overflow-hidden">
            {interview_questions.map((q, idx) => (
              <div
                key={idx}
                className="border-b border-slate-700/50 last:border-0 hover:bg-slate-800/30 transition-colors cursor-pointer"
                onClick={() => setExpandedQ(expandedQ === idx ? null : idx)}
              >
                <div className="p-5">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="px-2.5 py-1 bg-indigo-500/15 text-indigo-400 text-xs font-bold rounded-lg border border-indigo-500/20">
                      Q{idx + 1}
                    </span>
                    {q.skill && (
                      <span className="skill-chip text-xs">{q.skill}</span>
                    )}
                    {q.difficulty && (
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        q.difficulty === 'Hard' ? 'bg-red-500/15 text-red-400' :
                        q.difficulty === 'Medium' ? 'bg-amber-500/15 text-amber-400' :
                        'bg-green-500/15 text-green-400'
                      }`}>{q.difficulty}</span>
                    )}
                  </div>
                  <p className="text-white font-medium text-base">{q.question}</p>
                </div>
                {expandedQ === idx && q.hint && (
                  <div className="px-5 pb-5">
                    <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-700/50 text-sm text-slate-300">
                      <span className="text-teal-400 font-bold mr-2">💡 Hint:</span> {q.hint}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bottom Actions */}
      <div className="flex flex-wrap gap-4 justify-center pb-8 animate-fade-in-up" style={{ animationDelay: '0.9s' }}>
        <button onClick={generatePDF} className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl border border-slate-600 transition-all hover:scale-105 flex items-center gap-2">
          📥 Download Full Report
        </button>
        <Link to="/upload" className="btn-primary py-3 px-6 rounded-xl flex items-center gap-2 hover:scale-105 transition-transform">
          ✨ Analyze Another Resume
        </Link>
        <Link to="/history" className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl border border-slate-600 transition-all hover:scale-105 flex items-center gap-2">
          📋 View History
        </Link>
      </div>
    </div>
  );
};

export default AnalysisResultPage;
