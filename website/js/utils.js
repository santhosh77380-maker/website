// Utility functions for UI updates and data formatting

const Utils = {
  /**
   * Displays a toast notification (success, error, warning)
   * @param {string} message 
   * @param {string} type - 'success', 'error', 'info', 'warning'
   */
  showToast(message, type = 'info') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.id = 'toast-container';
      toastContainer.style.position = 'fixed';
      toastContainer.style.bottom = '20px';
      toastContainer.style.right = '20px';
      toastContainer.style.zIndex = '9999';
      toastContainer.style.display = 'flex';
      toastContainer.style.flexDirection = 'column';
      toastContainer.style.gap = '10px';
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    // Inline styling for the toast since we don't have dedicated CSS for it
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '8px';
    toast.style.color = '#fff';
    toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';
    toast.style.transition = 'all 0.3s ease';
    toast.style.fontFamily = "'Outfit', sans-serif";
    toast.style.fontSize = '0.9rem';

    if (type === 'success') toast.style.background = '#10B981';
    else if (type === 'error') toast.style.background = '#EF4444';
    else if (type === 'warning') toast.style.background = '#F59E0B';
    else toast.style.background = '#3B82F6';

    toast.innerHTML = message;
    toastContainer.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    });

    // Remove after 3 seconds
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },

  /**
   * Toggles the loading state of a button
   * @param {HTMLElement} btn 
   * @param {boolean} isLoading 
   * @param {string} originalText 
   */
  setButtonLoading(btn, isLoading, originalText = '') {
    if (!btn) return;
    if (isLoading) {
      btn.disabled = true;
      btn.dataset.originalText = btn.innerHTML;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
    } else {
      btn.disabled = false;
      btn.innerHTML = originalText || btn.dataset.originalText;
    }
  },

  /**
   * Format a date string into readable format (e.g. Aug 15, 2025)
   * @param {string} dateString 
   * @returns {string}
   */
  formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  },
  
  /**
   * Format a time string into readable format
   */
  formatTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  }
};
