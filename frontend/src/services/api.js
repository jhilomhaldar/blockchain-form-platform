import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getFormBySlug = async (slug) => {
  const response = await api.get(`/forms/${slug}/`);
  return response.data;
};

export const submitForm = async (payload) => {
  const response = await api.post("/submissions/", payload);
  return response.data;
};

export const verifySubmission = async (submissionRef) => {
  const response = await api.get(`/submissions/${submissionRef}/verify/`);
  return response.data;
};

export const getSubmissionDashboard = async () => {
  const response = await api.get("/submissions/dashboard/");
  return response.data;
};

export const getSubmissionCertificate = async (submissionRef) => {
  const response = await api.get(`/certificates/${submissionRef}/`);
  return response.data;
};

export default api;
