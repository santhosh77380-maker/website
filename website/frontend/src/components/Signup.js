// ... existing code ...

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('http://localhost:5000/api/student/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (response.ok) {
      // Login page ku pogaama dashboard ku poga token save panni redirect pannanum
      localStorage.setItem('token', data.token);
      localStorage.setItem('userType', 'student');
      window.location.href = '/student-dashboard'; // Change this line
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Fetch error:", error);
    alert("Connection failed. Backend run aagutha nu check pannunga!");
  }
};

// ... rest of code ...