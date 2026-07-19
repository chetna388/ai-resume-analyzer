import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import useAnalysis from '../hooks/useAnalysis';

const ROLES = [
  'Software Engineer', 'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
  'Data Scientist', 'AI/ML Engineer', 'Cloud Engineer', 'DevOps Engineer',
  'Android Developer', 'iOS Developer', 'Java Developer', 'Python Developer',
  'Product Manager', 'Data Analyst'
];

const UploadResumePage = () => {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  
  const { 
    resumeText, uploadResume, jobDescription, setJobDescription, 
    targetRole, setTargetRole, analyzeResume, loading, error 
  } = useAnalysis();
  
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (selectedFile) => {
    if (selectedFile.type !== 'application/pdf') {
      alert('Please upload a PDF file.');
      return;
    }
    setFile(selectedFile);
    try {
      await uploadResume(selectedFile);
      setStep(2);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyze = async () => {
    if (!targetRole) {
      alert('Please select a target role');
      return;
    }
    try {
      const result = await analyzeResume();
      navigate('/analysis', { state: { result } });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in-up">
      <div className="mb-10">
        <h1 className="text-3xl font-display font-bold text-white text-center">New Resume Analysis</h1>
        <p className="text-slate-400 text-center mt-2">Follow the steps below to get AI-powered insights</p>
      </div>

      {/* Stepper */}
      <div className="flex items-center justify-center mb-12">
        <div className={`flex flex-col items-center ${step >= 1 ? 'text-indigo-400' : 'text-slate-500'}`}>
          <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold mb-2 transition-colors ${step >= 1 ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)]' : 'bg-slate-800 border border-slate-600'}`}>
            1
          </div>
          <span className="text-sm font-medium">Upload PDF</span>
        </div>
        <div className={`w-24 h-1 mx-2 rounded-full transition-colors ${step >= 2 ? 'bg-indigo-500' : 'bg-slate-700'}`}></div>
        <div className={`flex flex-col items-center ${step >= 2 ? 'text-indigo-400' : 'text-slate-500'}`}>
          <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold mb-2 transition-colors ${step >= 2 ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)]' : 'bg-slate-800 border border-slate-600'}`}>
            2
          </div>
          <span className="text-sm font-medium">Target Role</span>
        </div>
        <div className={`w-24 h-1 mx-2 rounded-full transition-colors ${step >= 3 ? 'bg-indigo-500' : 'bg-slate-700'}`}></div>
        <div className={`flex flex-col items-center ${step >= 3 ? 'text-indigo-400' : 'text-slate-500'}`}>
          <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold mb-2 transition-colors ${step >= 3 ? 'bg-indigo-600 text-white shadow-[0_0_15px_rgba(99,102,241,0.5)]' : 'bg-slate-800 border border-slate-600'}`}>
            3
          </div>
          <span className="text-sm font-medium">Analyze</span>
        </div>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-8 flex items-center gap-3">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* Step 1: Upload */}
      {step === 1 && (
        <div className="glass-card p-8 animate-fade-in-up">
          <h2 className="text-xl font-bold text-white mb-6">Step 1: Upload your resume</h2>
          
          <div 
            className={`upload-zone ${isDragging ? 'drag-over' : ''} ${loading ? 'opacity-50 pointer-events-none' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              className="hidden" 
              accept=".pdf"
              onChange={handleFileSelect} 
            />
            
            {loading ? (
              <div className="flex flex-col items-center py-8">
                <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mb-4"></div>
                <p className="text-lg font-medium text-indigo-400">Extracting text from PDF...</p>
              </div>
            ) : (
              <div className="flex flex-col items-center py-6">
                <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center text-3xl mb-4">
                  📄
                </div>
                <p className="text-lg font-medium text-white mb-2">Drag & drop your PDF here</p>
                <p className="text-slate-400 text-sm mb-6">or click to browse files</p>
                <button className="btn-primary py-2 px-6">Select File</button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Step 2: Details */}
      {(step === 2 || step === 3) && (
        <div className="glass-card p-8 animate-fade-in-up">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-white">Step 2: Target Role & Job Description</h2>
            <button onClick={() => setStep(1)} className="text-sm text-slate-400 hover:text-white transition-colors">
              Change File ({file?.name})
            </button>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Target Role <span className="text-red-400">*</span>
              </label>
              <select 
                className="input-field appearance-none bg-slate-800"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
              >
                <option value="">Select a role...</option>
                {ROLES.map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <label className="block text-sm font-medium text-slate-300">
                  Job Description (Optional, but highly recommended)
                </label>
                <span className="text-xs text-slate-500">{jobDescription.length} chars</span>
              </div>
              <textarea 
                className="input-field min-h-[150px] resize-y"
                placeholder="Paste the job description here to get a customized ATS match score and specific missing skills..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              ></textarea>
            </div>

            {/* Preview extracted text snippet */}
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Extracted Text Preview</label>
              <div className="bg-slate-900/50 rounded-lg p-4 text-xs text-slate-500 font-mono h-24 overflow-y-auto border border-slate-700/50">
                {resumeText}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-700/50 flex justify-end">
              <button 
                className="btn-primary w-full md:w-auto text-lg px-8 py-3 flex items-center justify-center shadow-[0_0_20px_rgba(99,102,241,0.4)]"
                onClick={handleAnalyze}
                disabled={loading || !targetRole}
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
                    Running AI Analysis...
                  </>
                ) : (
                  <>
                    <span className="mr-2">⚡</span> Analyze Resume
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadResumePage;
