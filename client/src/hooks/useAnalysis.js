import { useState } from 'react';
import resumeService from '../services/resumeService';

export const useAnalysis = () => {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const uploadResume = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const data = await resumeService.uploadResume(file);
      setResumeText(data.extracted_text);
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'Error uploading resume');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const analyzeResume = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await resumeService.analyzeResume(resumeText, jobDescription, targetRole);
      setAnalysisResult(data);
      localStorage.setItem('lastAnalysis', JSON.stringify(data));
      return data;
    } catch (err) {
      setError(err.response?.data?.message || 'Error analyzing resume');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setResumeText('');
    setJobDescription('');
    setTargetRole('');
    setAnalysisResult(null);
    setError(null);
  };

  return {
    resumeText,
    setResumeText,
    jobDescription,
    setJobDescription,
    targetRole,
    setTargetRole,
    analysisResult,
    setAnalysisResult,
    loading,
    error,
    uploadResume,
    analyzeResume,
    resetAnalysis,
  };
};

export default useAnalysis;
