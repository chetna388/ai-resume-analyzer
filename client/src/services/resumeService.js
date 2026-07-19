import api from './api';

const resumeService = {
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('resume', file);
    const response = await api.post('/upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  predictCategory: async (resumeText) => {
    const response = await api.post('/predict-category', { resume_text: resumeText });
    return response.data;
  },

  analyzeResume: async (resumeText, jobDescription, targetRole) => {
    const response = await api.post('/analyze-resume', {
      resume_text: resumeText,
      job_description: jobDescription,
      target_role: targetRole,
    });
    return response.data;
  },

  compareJobDescription: async (resumeText, jdText) => {
    const response = await api.post('/compare-job-description', {
      resume_text: resumeText,
      jd_text: jdText,
    });
    return response.data;
  },

  getHistory: async () => {
    const response = await api.get('/history');
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/profile');
    return response.data;
  }
};

export default resumeService;
