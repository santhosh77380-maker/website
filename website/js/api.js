// API utility for handling HTTP requests to the FastAPI backend

const Api = {
  /**
   * Get the authentication token from localStorage
   * @returns {string|null}
   */
  getToken() {
    return localStorage.getItem(CONFIG.TOKEN_KEY);
  },

  /**
   * Helper function to build headers
   * @param {boolean} requiresAuth 
   * @returns {Object}
   */
  _buildHeaders(requiresAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    if (requiresAuth) {
      const token = this.getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return headers;
  },

  /**
   * Handle the fetch response
   * @param {Response} response 
   * @returns {Promise<any>}
   */
  async _handleResponse(response) {
    let data;
    try {
      data = await response.json();
    } catch (e) {
      data = { message: 'Failed to parse response' };
    }

    if (!response.ok) {
      // If unauthorized, redirect to login
      if (response.status === 401 || response.status === 403) {
        Utils.showToast('Session expired. Please log in again.', 'error');
        localStorage.removeItem(CONFIG.TOKEN_KEY);
        localStorage.removeItem(CONFIG.USER_ROLE_KEY);
        // Quick redirect logic, you may want to refine this based on the page
        if (!window.location.pathname.includes('login')) {
          setTimeout(() => {
            window.location.href = 'student-login.html'; 
          }, 1500);
        }
      }
      throw new Error(data.detail || data.message || 'An error occurred');
    }
    return data;
  },

  /**
   * Generic request function
   * @param {string} endpoint 
   * @param {Object} options 
   * @param {boolean} requiresAuth 
   * @returns {Promise<any>}
   */
  async request(endpoint, options = {}, requiresAuth = true) {
    const url = `${CONFIG.API_BASE_URL}${endpoint}`;
    
    const config = {
      ...options,
      headers: {
        ...this._buildHeaders(requiresAuth),
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      return await this._handleResponse(response);
    } catch (error) {
      console.error(`API Request failed for ${endpoint}:`, error);
      throw error;
    }
  },

  // ── Convenience methods ──────────────────────────────────────

  async get(endpoint, requiresAuth = true) {
    return this.request(endpoint, { method: 'GET' }, requiresAuth);
  },

  async post(endpoint, body, requiresAuth = true) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    }, requiresAuth);
  },

  async put(endpoint, body, requiresAuth = true) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    }, requiresAuth);
  },

  async delete(endpoint, requiresAuth = true) {
    return this.request(endpoint, { method: 'DELETE' }, requiresAuth);
  }
};
