// Admin Module

const Admin = {
  /**
   * Ensure user is authenticated and is an admin
   */
  checkAuth() {
    if (!Auth.isAuthenticated() || localStorage.getItem(CONFIG.USER_ROLE_KEY) !== CONFIG.ROLES.ADMIN) {
      window.location.href = 'admin-login.html';
      return false;
    }
    return true;
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

  /**
   * Load Dashboard Stats
   */
  async loadDashboard() {
    if (!this.checkAuth()) return;
    try {
      const stats = await Api.get('/admin/stats');
      // For demonstration, assumed to populate specific IDs if added to HTML
      // Since we didn't add IDs to all admin dashboard stats to keep UI intact,
      // this represents how it would bind.
      console.log('Admin Dashboard Stats:', stats);
    } catch (error) {
      Utils.showToast('Failed to load admin stats: ' + error.message, 'error');
    }
  },

  /**
   * Load Students List (for admin-students.html)
   */
  async loadStudents() {
    if (!this.checkAuth()) return;
    
    // Show spinner in table
    const tableBody = document.getElementById('studentsBody');
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center"><i class="fa-solid fa-spinner fa-spin"></i> Loading...</td></tr>';
    }

    try {
      const students = await Api.get('/admin/students');
      if (tableBody) {
        tableBody.innerHTML = '';
        students.forEach(st => {
          const statusBadge = st.status === 'Active' 
            ? '<span class="badge badge-success">Active</span>'
            : (st.status === 'Pending' ? '<span class="badge badge-warning">Pending</span>' : '<span class="badge badge-danger">Inactive</span>');
            
          tableBody.innerHTML += `
            <tr>
              <td>
                <div style="display:flex;align-items:center;gap:.75rem">
                  <div class="avatar avatar-sm" style="background:#E5E7EB;color:#374151">${st.firstName.charAt(0)}${st.lastName.charAt(0)}</div>
                  <div>
                    <div class="col-name">${st.firstName} ${st.lastName}</div>
                    <div style="font-size:.72rem;color:#9CA3AF">${st.email}</div>
                  </div>
                </div>
              </td>
              <td><span style="font-family:'Outfit',sans-serif;font-weight:600">${st.rollNumber}</span></td>
              <td>${st.department}</td>
              <td>${st.year} Year</td>
              <td>${statusBadge}</td>
              <td>
                <button class="btn btn-ghost btn-sm" title="Edit" onclick="Admin.editStudent('${st.id}')"><i class="fa-solid fa-pen"></i></button>
                <button class="btn btn-ghost btn-sm" title="Delete" style="color:#EF4444" onclick="Admin.deleteStudent('${st.id}')"><i class="fa-solid fa-trash"></i></button>
              </td>
            </tr>
          `;
        });
      }
    } catch (error) {
      if (tableBody) tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:red">Failed to load students</td></tr>`;
      Utils.showToast('Failed to load students: ' + error.message, 'error');
    }
  },

  /**
   * Placeholder for edit student
   */
  editStudent(id) {
    Utils.showToast(`Edit student dialog for ID ${id} opened.`, 'info');
    // Implement modal logic here
  },

  /**
   * Delete student
   */
  async deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;
    try {
      await Api.delete(`/admin/students/${id}`);
      Utils.showToast('Student deleted successfully', 'success');
      this.loadStudents();
    } catch (error) {
      Utils.showToast('Failed to delete student: ' + error.message, 'error');
    }
  }
};
