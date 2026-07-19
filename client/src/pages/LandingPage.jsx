import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-28 overflow-hidden">
        <div className="absolute inset-0 z-0 bg-[var(--gradient-hero)]"></div>
        <div className="absolute inset-0 z-0 opacity-30 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTU0LjYyNyAwTDYwIDUuMzczdi43NTg2TDkuMjc0IDYwSDMuOTAybDUwLjcyNS01MC43MjVWMEg1NC42Mjd6IiBmaWxsPSIjZmZmIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIG9wYWNpdHk9Ii4wNSIvPjwvc3ZnPg==')]"></div>
        
        {/* Floating animated blobs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl mix-blend-screen animate-[pulse-glow_4s_ease-in-out_infinite]"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-500/20 rounded-full blur-3xl mix-blend-screen animate-[pulse-glow_6s_ease-in-out_infinite_reverse]"></div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center animate-fade-in-up">
          <h1 className="text-5xl md:text-7xl font-display font-extrabold tracking-tight mb-8">
            <span className="block text-white mb-2">Elevate Your Career with</span>
            <span className="block gradient-text">AI-Powered Resume Analysis</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-slate-300 mx-auto mb-10">
            Get instant ATS scoring, personalized skill recommendations, and ML-driven insights to land your dream job faster.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
            <Link to="/register" className="btn-primary text-lg px-8 py-4 w-full sm:w-auto text-center shadow-[0_0_20px_rgba(99,102,241,0.4)]">
              Get Started for Free
            </Link>
            <a href="#features" className="px-8 py-4 w-full sm:w-auto text-center rounded-xl bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600/50 text-white font-semibold transition-all duration-300 backdrop-blur-sm">
              Learn More
            </a>
          </div>

          <div className="mt-20 pt-10 border-t border-slate-700/50 grid grid-cols-1 gap-8 sm:grid-cols-3 max-w-4xl mx-auto">
            <div>
              <p className="text-4xl font-display font-bold text-white">10,000+</p>
              <p className="mt-2 text-indigo-400 font-medium">Resumes Analyzed</p>
            </div>
            <div>
              <p className="text-4xl font-display font-bold text-white">95%</p>
              <p className="mt-2 text-teal-400 font-medium">Prediction Accuracy</p>
            </div>
            <div>
              <p className="text-4xl font-display font-bold text-white">50+</p>
              <p className="mt-2 text-purple-400 font-medium">Job Categories</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-[#0f172a] relative z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-3xl font-display font-bold text-white sm:text-4xl">Powerful Features</h2>
            <p className="mt-4 text-lg text-slate-400">Everything you need to optimize your resume and beat the ATS.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: '🧠', title: 'ML Classification', desc: 'Our advanced models predict your exact job category with high precision based on industry standards.' },
              { icon: '📊', title: 'ATS Score Analysis', desc: 'Get a comprehensive 0-100 score analyzing readability, impact, formatting, and keyword optimization.' },
              { icon: '🎯', title: 'Smart Skill Detection', desc: 'Automatically extract and categorize hard and soft skills to identify critical gaps against target roles.' },
              { icon: '❓', title: 'AI Interview Prep', desc: 'Generate customized technical and behavioral interview questions based on your specific resume content.' },
              { icon: '🚀', title: 'Improvement Tips', desc: 'Receive actionable, priority-based recommendations to enhance bullet points and structure.' },
              { icon: '📈', title: 'Detailed Analytics', desc: 'Visualize your strengths and weaknesses through interactive charts and historical tracking.' },
            ].map((feature, idx) => (
              <div key={idx} className="glass-card p-8 hover:-translate-y-2 transition-all duration-300 animate-fade-in-up" style={{ animationDelay: `${0.1 * (idx + 1)}s` }}>
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 bg-slate-900/50 border-y border-slate-800 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-display font-bold text-white sm:text-4xl">How It Works</h2>
          </div>
          
          <div className="relative">
            <div className="absolute top-1/2 left-0 w-full h-1 bg-gradient-to-r from-indigo-500/20 via-teal-500/50 to-purple-500/20 -translate-y-1/2 hidden md:block rounded-full"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {[
                { icon: '📄', title: 'Upload Resume', desc: 'Upload your PDF resume' },
                { icon: '⚡', title: 'AI Analysis', desc: 'We extract and parse data' },
                { icon: '📊', title: 'Get ATS Score', desc: 'Instant detailed feedback' },
                { icon: '🎯', title: 'Improve & Apply', desc: 'Fix issues and get hired' }
              ].map((step, idx) => (
                <div key={idx} className="relative z-10 flex flex-col items-center text-center">
                  <div className="w-20 h-20 rounded-2xl glass-card flex items-center justify-center text-3xl mb-4 bg-slate-800 shadow-[0_0_20px_rgba(99,102,241,0.2)]">
                    {step.icon}
                  </div>
                  <h3 className="text-lg font-bold text-white mb-1">Step {idx + 1}</h3>
                  <h4 className="text-indigo-400 font-medium mb-2">{step.title}</h4>
                  <p className="text-slate-400 text-sm">{step.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="glass-card p-12 text-center bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-indigo-500/30">
            <h2 className="text-3xl font-display font-bold text-white mb-4">Ready to optimize your resume?</h2>
            <p className="text-lg text-slate-300 mb-8 max-w-2xl mx-auto">Join thousands of job seekers who have successfully landed their target roles using our AI insights.</p>
            <Link to="/register" className="btn-primary text-lg px-10 py-4 inline-block shadow-[0_0_30px_rgba(99,102,241,0.5)] hover:shadow-[0_0_50px_rgba(99,102,241,0.7)]">
              Start Analyzing Today
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
