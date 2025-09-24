// Configuration for API endpoints
const config = {
  API_BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://quantum-banking-api.onrender.com'
    : 'http://localhost:5000'
};

export default config;