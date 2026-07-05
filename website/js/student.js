// Student Module

const Student = {
  /**
   * Ensure user is authenticated and is a student
   */
  checkAuth() {
    if (!Auth.isAuthenticated() || localStorage.getItem(CONFIG.USER_ROLE_KEY) !== CONFIG.ROLES.STUDENT) {
      window.location.href = 'student-login.html';
      return false;
    }
    return true;
  },

  /**
   * Load dashboard data
   */
  async loadDashboard() {
    if (!this.checkAuth()) return;

    try {
      // Show loading states on dashboard elements if needed
      // Here we assume standard endpoints for a dashboard
      const [profile, stats, notifications, events] = await Promise.all([
        Api.get('/student/profile'),
        Api.get('/student/stats'),
        Api.get('/student/notifications'),
        Api.get('/student/events')
      ]);

      this._renderProfileOverview(profile);
      this._renderStats(stats);
      this._renderNotifications(notifications);
      this._renderEvents(events);

    } catch (error) {
      Utils.showToast('Failed to load dashboard data. ' + error.message, 'error');
    }
  },

  /**
   * Load Profile Page data
   */
  async loadProfile() {
    if (!this.checkAuth()) return;
    try {
      const profile = await Api.get('/student/profile');
      // Render profile fields (assumes IDs exist on the profile page)
      const fields = ['name', 'rollNumber', 'email', 'phone', 'department', 'year', 'dob', 'bloodGroup', 'address'];
      fields.forEach(field => {
        const el = document.getElementById(`profile-${field}`);
        if (el) el.textContent = profile[field] || '-';
      });
    } catch (error) {
      Utils.showToast('Failed to load profile. ' + error.message, 'error');
    }
  },

  /**
   * Load Attendance Page data
   */
  async loadAttendance() {
    if (!this.checkAuth()) return;
    try {
      const attendance = await Api.get('/student/attendance');
      const tableBody = document.getElementById('attendanceTableBody');
      if (tableBody) {
        tableBody.innerHTML = '';
        attendance.subjects.forEach(sub => {
          tableBody.innerHTML += `
            <tr>
              <td>${sub.code}</td>
              <td>${sub.name}</td>
              <td>${sub.totalClasses}</td>
              <td>${sub.attended}</td>
              <td>
                <span class="badge ${sub.percentage >= 75 ? 'badge-success' : 'badge-danger'}">
                  ${sub.percentage}%
                </span>
              </td>
            </tr>
          `;
        });
      }
    } catch (error) {
      Utils.showToast('Failed to load attendance. ' + error.message, 'error');
    }
  },

  /**
   * Setup logout button listener
   */
  setupLogout() {
    const logoutBtns = document.querySelectorAll('.sidebar-logout');
    logoutBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        Auth.logout();
      });
    });
  },

  // ── Render Helpers (Dashboard) ────────────────────────────────

  _renderProfileOverview(profile) {
    const nameEls = document.querySelectorAll('.sidebar-user-name, .topbar-user-name, .welcome-greeting');
    nameEls.forEach(el => {
      if (el.classList.contains('welcome-greeting')) {
        el.textContent = `Good Day, ${profile.firstName}! 👋`;
      } else {
        el.textContent = `${profile.firstName} ${profile.lastName}`;
      }
    });

    const roleEl = document.querySelector('.sidebar-user-role');
    if (roleEl) roleEl.textContent = `${profile.department} – ${profile.year} Year`;

    const avatarEls = document.querySelectorAll('.avatar, .sidebar-user-avatar');
    avatarEls.forEach(el => {
      el.textContent = profile.firstName.charAt(0) + profile.lastName.charAt(0);
    });
  },

  _renderStats(stats) {
    // Example IDs that would need to be in the HTML
    // We are selecting by the card structure or adding IDs to HTML
    const attendanceVal = document.getElementById('stat-attendance-val');
    if (attendanceVal) attendanceVal.textContent = `${stats.attendancePercentage}%`;

    const marksVal = document.getElementById('stat-marks-val');
    if (marksVal) marksVal.textContent = `${stats.avgMarks}/100`;

    const cgpaVal = document.getElementById('stat-cgpa-val');
    if (cgpaVal) cgpaVal.textContent = stats.cgpa;

    const feeVal = document.getElementById('stat-fee-val');
    if (feeVal) feeVal.textContent = stats.feeStatus;
  },

  _renderNotifications(notifs) {
    const container = document.getElementById('notificationsList');
    if (!container) return;
    container.innerHTML = '';
    notifs.forEach(n => {
      container.innerHTML += `
        <div class="notification-item">
          <div class="notification-dot ${n.type || ''}"></div>
          <div class="notification-content">
            <div class="notification-title">${n.title}</div>
            <div class="notification-desc">${n.description}</div>
          </div>
          <div class="notification-time">${Utils.formatDate(n.date)}</div>
        </div>
      `;
    });
  },

  _renderEvents(events) {
    const container = document.getElementById('eventsList');
    if (!container) return;
    container.innerHTML = '';
    events.forEach(e => {
      container.innerHTML += `
        <div style="padding:1rem;background:#EFF6FF;border-radius:12px;border:1px solid #BFDBFE">
          <div style="font-size:1.5rem;margin-bottom:.5rem">${e.icon || '📅'}</div>
          <div style="font-family:'Outfit',sans-serif;font-weight:700;font-size:.9rem;color:#1F2937;margin-bottom:.25rem">${e.title}</div>
          <div style="font-size:.75rem;color:#6B7280">${Utils.formatDate(e.date)} · ${e.location}</div>
          <a href="#" class="btn btn-primary btn-sm" style="margin-top:.75rem">Register</a>
        </div>
      `;
    });
  }
};
