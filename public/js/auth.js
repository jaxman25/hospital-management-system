// Authentication JavaScript
document.addEventListener("DOMContentLoaded", function() {
  // Check if already logged in
  checkAuthStatus();
  
  // Setup form event listeners
  setupLoginForm();
  setupRegisterForm();
});

// Tab switching
function showTab(tabName) {
  // Update active tab button
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  document.querySelector(`.tab-btn[onclick="showTab('${tabName}')"]`).classList.add('active');
  
  // Update active tab content
  document.querySelectorAll('.tab-content').forEach(tab => {
    tab.classList.remove('active');
  });
  document.getElementById(`${tabName}-tab`).classList.add('active');
  
  // Clear messages
  clearMessages();
}

// Clear error/success messages
function clearMessages() {
  document.getElementById('error-message').style.display = 'none';
  document.getElementById('success-message').style.display = 'none';
}

// Show error message
function showError(message) {
  const errorEl = document.getElementById('error-message');
  errorEl.textContent = message;
  errorEl.style.display = 'block';
  document.getElementById('success-message').style.display = 'none';
}

// Show success message
function showSuccess(message) {
  const successEl = document.getElementById('success-message');
  successEl.textContent = message;
  successEl.style.display = 'block';
  document.getElementById('error-message').style.display = 'none';
}

// Setup login form
function setupLoginForm() {
  const form = document.getElementById('loginForm');
  if (!form) return;
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
      showError('Please enter username and password');
      return;
    }
    
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        showSuccess('Login successful! Redirecting...');
        setTimeout(() => {
          window.location.href = '/app';
        }, 1500);
      } else {
        showError(data.error || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      showError('Network error. Please try again.');
    }
  });
}

// Setup register form
function setupRegisterForm() {
  const form = document.getElementById('registerForm');
  if (!form) return;
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('regName').value.trim();
    const username = document.getElementById('regUsername').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;
    const role = document.getElementById('regRole').value;
    
    // Validation
    if (!name || !username || !password) {
      showError('Name, username, and password are required');
      return;
    }
    
    if (password.length < 6) {
      showError('Password must be at least 6 characters');
      return;
    }
    
    if (password !== confirmPassword) {
      showError('Passwords do not match');
      return;
    }
    
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, name, email, role })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        showSuccess('Registration successful! You can now login.');
        // Clear form
        form.reset();
        // Switch to login tab
        showTab('login');
      } else {
        showError(data.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      showError('Network error. Please try again.');
    }
  });
}

// Check if user is already logged in
async function checkAuthStatus() {
  try {
    const response = await fetch('/api/auth/me');
    if (response.ok) {
      // Already logged in, redirect to app
      window.location.href = '/app';
    }
  } catch (error) {
    // Not logged in, stay on login page
  }
}

// Logout function (to be used in main app)
async function logout() {
  if (!confirm('Are you sure you want to logout?')) return;
  
  try {
    const response = await fetch('/api/auth/logout', {
      method: 'POST'
    });
    
    if (response.ok) {
      window.location.href = '/login';
    }
  } catch (error) {
    console.error('Logout error:', error);
    alert('Logout failed. Please try again.');
  }
}
