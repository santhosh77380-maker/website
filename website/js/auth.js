// Authentication Module

const Auth = {
  /**
   * Initialize authentication on a login page
   * @param {string} role - 'student' or 'admin'
   */
  init(role) {
    // If user is already logged in, redirect them
    if (this.isAuthenticated()) {
      const currentRole = localStorage.getItem(CONFIG.USER_ROLE_KEY);
      this._redirectBasedOnRole(currentRole);
      return;
    }
    this.currentRole = role;
  },

  /**
   * Check if a valid token exists
   * @returns {boolean}
   */
  isAuthenticated() {
    const token = Api.getToken();
    return !!token; // Basic check; ideally we'd verify expiration
  },

  /**
   * Redirect user based on their role
   * @param {string} role 
   */
  _redirectBasedOnRole(role) {
    if (role === CONFIG.ROLES.ADMIN) {
      window.location.href = 'admin-dashboard.html';
    } else {
      window.location.href = 'student-dashboard.html';
    }
  },

  /**
   * Handle the login form submission
   * @param {Event} e 
   * @param {string} emailId - ID of the email input
   * @param {string} pwdId - ID of the password input
   * @param {string} btnId - ID of the submit button
   * @param {string} errContainerId - ID of the generic error container
   */
  async login(e, emailId, pwdId, btnId, errContainerId) {
    e.preventDefault();
    
    const emailInput = document.getElementById(emailId);
    const pwdInput = document.getElementById(pwdId);
    const btn = document.getElementById(btnId);
    const errContainer = document.getElementById(errContainerId);
    
    const email = emailInput.value.trim();
    const password = pwdInput.value.trim();

    // Reset error container
    if (errContainer) errContainer.style.display = 'none';

    // Validation is already handled mostly by the inline scripts in the HTML,
    // but we ensure we have data here.
    if (!email || !password) return;

    Utils.setButtonLoading(btn, true);

    try {
      // POST request to FastAPI backend
      // Adjust the endpoint as necessary, standard OAuth2 uses formData for /token,
      // but assuming a custom JSON login endpoint here based on the plan.
      const payload = { email, password, role: this.currentRole };
      
      const response = await Api.post('/auth/login', payload, false);
      
      // Store token and role
      localStorage.setItem(CONFIG.TOKEN_KEY, response.access_token || response.token);
      localStorage.setItem(CONFIG.USER_ROLE_KEY, this.currentRole);

      Utils.showToast('Login successful! Redirecting...', 'success');

      setTimeout(() => {
        this._redirectBasedOnRole(this.currentRole);
      }, 1000);

    } catch (error) {
      Utils.setButtonLoading(btn, false);
      if (errContainer) {
        errContainer.style.display = 'flex';
        // Assuming errContainer has a span for the message
        const msgSpan = errContainer.querySelector('span');
        if (msgSpan) msgSpan.textContent = error.message || 'Invalid credentials. Please try again.';
      } else {
        Utils.showToast(error.message || 'Login failed', 'error');
      }
    }
  },

  /**
   * Log the user out
   */
  logout() {
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_ROLE_KEY);
    window.location.href = 'home.html';
  }
};
