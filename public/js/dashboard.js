// Hospital Dashboard JavaScript
document.addEventListener("DOMContentLoaded", function() {
  // Check authentication
  checkDashboardAuth();
  
  // Load statistics
  loadStats();
});

// Check authentication for dashboard
async function checkDashboardAuth() {
  try {
    const response = await fetch('/api/auth/me');
    if (!response.ok) {
      window.location.href = '/login';
      return false;
    }
    
    const data = await response.json();
    // Update user info
    if (data.user && data.user.name) {
      document.getElementById('userName').textContent = data.user.name;
    }
    return true;
  } catch (error) {
    console.error('Auth check failed:', error);
    window.location.href = '/login';
    return false;
  }
}

// Load statistics from API
async function loadStats() {
  const content = document.getElementById('stats-content');
  content.innerHTML = `
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading statistics...</p>
    </div>
  `;
  
  try {
    const response = await fetch('/api/stats');
    const stats = await response.json();
    
    displayStats(stats);
  } catch (error) {
    console.error('Error loading stats:', error);
    content.innerHTML = `
      <div class="loading">
        <i class="fas fa-exclamation-triangle" style="color: #e74c3c;"></i>
        <p>Error loading statistics. Please try again.</p>
      </div>
    `;
  }
}

// Display statistics
function displayStats(stats) {
  const content = document.getElementById('stats-content');
  
  // Calculate additional stats
  const avgAppointmentsPerDoctor = stats.totalDoctors > 0 
    ? (stats.totalAppointments / stats.totalDoctors).toFixed(1) 
    : 0;
  
  const today = new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  
  content.innerHTML = `
    <!-- Summary Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-user-injured"></i>
        </div>
        <div class="stat-number">${stats.totalPatients}</div>
        <div class="stat-label">Total Patients</div>
        <div class="stat-trend">
          <span class="badge badge-success">Registered</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-user-md"></i>
        </div>
        <div class="stat-number">${stats.totalDoctors}</div>
        <div class="stat-label">Medical Staff</div>
        <div class="stat-trend">
          <span class="badge badge-info">Available</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-calendar-check"></i>
        </div>
        <div class="stat-number">${stats.totalAppointments}</div>
        <div class="stat-label">Total Appointments</div>
        <div class="stat-trend">
          <span class="badge badge-success">Scheduled</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-calendar-day"></i>
        </div>
        <div class="stat-number">${stats.todaysAppointments}</div>
        <div class="stat-label">Today's Appointments</div>
        <div class="stat-trend">
          <span class="badge badge-warning">${today}</span>
        </div>
      </div>
    </div>
    
    <!-- Data Charts -->
    <div class="data-grid">
      <!-- Gender Distribution -->
      <div class="chart-container">
        <h3 class="chart-title">
          <i class="fas fa-venus-mars"></i> Patient Gender Distribution
        </h3>
        <div id="genderChart">
          ${renderGenderChart(stats.genderDistribution)}
        </div>
      </div>
      
      <!-- Top Doctors -->
      <div class="chart-container">
        <h3 class="chart-title">
          <i class="fas fa-star"></i> Top Doctors by Appointments
        </h3>
        <div id="doctorsChart">
          ${renderDoctorsChart(stats.topDoctors)}
        </div>
      </div>
    </div>
    
    <!-- Detailed Tables -->
    <div class="chart-container">
      <h3 class="chart-title">
        <i class="fas fa-chart-bar"></i> Detailed Statistics
      </h3>
      
      <div class="data-grid">
        <!-- Gender Table -->
        <div>
          <h4>Patient Demographics</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Gender</th>
                <th>Count</th>
                <th>Percentage</th>
              </tr>
            </thead>
            <tbody>
              ${renderGenderTable(stats.genderDistribution, stats.totalPatients)}
            </tbody>
          </table>
        </div>
        
        <!-- Weekly Appointments -->
        <div>
          <h4>Appointments This Week</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Appointments</th>
              </tr>
            </thead>
            <tbody>
              ${renderWeeklyTable(stats.weeklyAppointments)}
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Summary Stats -->
      <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
        <h4>Summary</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
          <div>
            <strong>Upcoming Appointments (7 days):</strong>
            <div style="font-size: 1.5rem; color: #3498db; margin-top: 5px;">
              ${stats.upcomingAppointments}
            </div>
          </div>
          <div>
            <strong>Average per Doctor:</strong>
            <div style="font-size: 1.5rem; color: #27ae60; margin-top: 5px;">
              ${avgAppointmentsPerDoctor} appointments
            </div>
          </div>
          <div>
            <strong>Patient-to-Doctor Ratio:</strong>
            <div style="font-size: 1.5rem; color: #e74c3c; margin-top: 5px;">
              ${stats.totalDoctors > 0 ? (stats.totalPatients / stats.totalDoctors).toFixed(1) : 0}:1
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Render gender distribution chart
function renderGenderChart(genderData) {
  if (!genderData || genderData.length === 0) {
    return '<p class="no-results">No gender data available</p>';
  }
  
  let html = '<div style="display: flex; align-items: flex-end; gap: 20px; height: 200px; margin-top: 20px;">';
  
  const maxCount = Math.max(...genderData.map(g => g.count));
  
  genderData.forEach(gender => {
    const height = (gender.count / maxCount) * 150;
    const color = gender.gender === 'Male' ? '#3498db' : 
                  gender.gender === 'Female' ? '#e74c3c' : '#9b59b6';
    
    html += `
      <div style="text-align: center;">
        <div style="
          width: 60px;
          height: ${height}px;
          background: ${color};
          border-radius: 5px;
          margin: 0 auto;
        "></div>
        <div style="margin-top: 10px; font-weight: bold;">${gender.gender}</div>
        <div style="color: #7f8c8d;">${gender.count}</div>
      </div>
    `;
  });
  
  html += '</div>';
  return html;
}

// Render top doctors chart
function renderDoctorsChart(doctorsData) {
  if (!doctorsData || doctorsData.length === 0) {
    return '<p class="no-results">No appointment data available</p>';
  }
  
  let html = '<div style="margin-top: 20px;">';
  
  const maxCount = Math.max(...doctorsData.map(d => d.appointment_count));
  
  doctorsData.forEach(doctor => {
    const width = (doctor.appointment_count / maxCount) * 100;
    
    html += `
      <div style="margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
          <span style="font-weight: bold;">${doctor.name}</span>
          <span>${doctor.appointment_count} appointments</span>
        </div>
        <div style="
          width: 100%;
          height: 10px;
          background: #ecf0f1;
          border-radius: 5px;
          overflow: hidden;
        ">
          <div style="
            width: ${width}%;
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 5px;
          "></div>
        </div>
        <div style="color: #7f8c8d; font-size: 0.9rem; margin-top: 5px;">
          ${doctor.specialty || 'General'}
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  return html;
}

// Render gender table
function renderGenderTable(genderData, totalPatients) {
  if (!genderData || genderData.length === 0) {
    return '<tr><td colspan="3" class="no-results">No data available</td></tr>';
  }
  
  let html = '';
  genderData.forEach(gender => {
    const percentage = totalPatients > 0 
      ? ((gender.count / totalPatients) * 100).toFixed(1) 
      : 0;
    
    html += `
      <tr>
        <td>${gender.gender}</td>
        <td>${gender.count}</td>
        <td>${percentage}%</td>
      </tr>
    `;
  });
  
  return html;
}

// Render weekly appointments table
function renderWeeklyTable(weeklyData) {
  if (!weeklyData || weeklyData.length === 0) {
    return '<tr><td colspan="2" class="no-results">No appointments this week</td></tr>';
  }
  
  let html = '';
  weeklyData.forEach(day => {
    const date = new Date(day.date);
    const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
    
    html += `
      <tr>
        <td>${dayName}, ${day.date}</td>
        <td>${day.count}</td>
      </tr>
    `;
  });
  
  return html;
}

// Logout function
async function logout() {
  if (!confirm('Are you sure you want to logout?')) return;
  
  try {
    const response = await fetch('/api/auth/logout', {
      method: 'POST'
    });
    
    if (response.ok) {
      window.location.href = '/login';
    } else {
      alert('Logout failed. Please try again.');
    }
  } catch (error) {
    console.error('Logout error:', error);
    alert('Network error. Please try again.');
  }
}
