// Centralized configuration file
const CONFIG = {
  // Base URL for the FastAPI backend
  API_BASE_URL: 'http://localhost:8000/api/v1',
  
  // Storage keys
  TOKEN_KEY: 'excellence_college_jwt',
  USER_ROLE_KEY: 'excellence_college_role',

  // Roles
  ROLES: {
    STUDENT: 'student',
    ADMIN: 'admin'
  }
};
