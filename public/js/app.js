// Hospital Management System - Frontend WITH AUTHENTICATION

// Check authentication on app load
async function checkAppAuth() {
  try {
    const response = await fetch('/api/auth/me');
    if (!response.ok) {
      // Not authenticated, redirect to login
      window.location.href = '/login';
      return false;
    }
    
    const data = await response.json();
    // Update user info in header
    if (data.user && data.user.name) {
      const userNameElement = document.getElementById('userName');
      if (userNameElement) {
        userNameElement.textContent = data.user.name;
      }
    }
    return true;
  } catch (error) {
    console.error('Auth check failed:', error);
    window.location.href = '/login';
    return false;
  }
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

// Update your DOMContentLoaded to check auth
document.addEventListener("DOMContentLoaded", async function() {
  // Check authentication first
  const isAuthenticated = await checkAppAuth();
  if (!isAuthenticated) return;
  
  console.log("Hospital Management System loaded");
  
  // Load initial data
  loadPatients();
  loadDoctors();
  loadAppointments();
  
  // Setup form event listeners
  setupPatientForm();
  setupDoctorForm();
  setupAppointmentForm();
  
  // Add keyboard support for search
  const searchBox = document.getElementById('searchPatient');
  const dateFilter = document.getElementById('filterDate');
  
  if (searchBox) {
    searchBox.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        searchPatients();
      }
    });
  }
  
  if (dateFilter) {
    dateFilter.addEventListener('change', function() {
      if (this.value) {
        filterAppointments();
      }
    });
  }
});

// ========== PATIENT FUNCTIONS ==========
async function loadPatients() {
  try {
    const response = await fetch("/api/patients");
    const patients = await response.json();
    displayPatients(patients);
    populatePatientDropdown(patients);
  } catch (error) {
    console.error("Error loading patients:", error);
    document.getElementById("patients").innerHTML = "<p class='no-results'>Error loading patients</p>";
  }
}

function displayPatients(patients) {
  const container = document.getElementById("patients");
  updatePatientCount(patients.length);
  
  if (patients.length === 0) {
    container.innerHTML = "<p class='no-results'>No patients found</p>";
    return;
  }
  
  container.innerHTML = patients.map(patient => `
    <div class="patient-card" id="patient-${patient.id}">
      ${patient.image_url ? `<img src="${patient.image_url}" alt="${patient.name}" style="width:100px;height:100px;object-fit:cover;">` : ''}
      <h3>${patient.name}</h3>
      <p>Age: ${patient.age || "N/A"}</p>
      <p>Gender: ${patient.gender || "N/A"}</p>
      <div class="patient-actions">
        <button class="edit-btn" onclick="editPatient(${patient.id})">Edit</button>
        <button class="delete-btn" onclick="deletePatient(${patient.id})">Delete</button>
      </div>
    </div>
  `).join("");
}

// Edit patient - opens edit form
async function editPatient(id) {
  try {
    const response = await fetch(`/api/patients/${id}`);
    const patient = await response.json();
    
    if (response.ok) {
      // Create edit form modal
      const editForm = `
        <div class="edit-modal" id="edit-patient-modal">
          <div class="modal-content">
            <h2>Edit Patient: ${patient.name}</h2>
            <form id="editPatientForm">
              <input type="hidden" id="editPatientId" value="${patient.id}">
              <input type="text" id="editPatientName" value="${patient.name || ''}" placeholder="Full Name" required>
              <input type="number" id="editPatientAge" value="${patient.age || ''}" placeholder="Age">
              <input type="text" id="editPatientGender" value="${patient.gender || ''}" placeholder="Gender">
              <input type="text" id="editPatientImage" value="${patient.image_url || ''}" placeholder="Image URL">
              <div class="modal-buttons">
                <button type="submit">Save Changes</button>
                <button type="button" onclick="closeEditModal()">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      `;
      
      // Add modal to page
      document.body.insertAdjacentHTML('beforeend', editForm);
      
      // Setup form submission
      document.getElementById("editPatientForm").addEventListener("submit", async function(e) {
        e.preventDefault();
        await updatePatient();
      });
    }
  } catch (error) {
    console.error("Error fetching patient:", error);
    alert("Error loading patient data");
  }
}

// Update patient in database
async function updatePatient() {
  const patientId = document.getElementById("editPatientId").value;
  const patientData = {
    name: document.getElementById("editPatientName").value,
    age: document.getElementById("editPatientAge").value || null,
    gender: document.getElementById("editPatientGender").value || null,
    image_url: document.getElementById("editPatientImage").value || null
  };
  
  try {
    const response = await fetch(`/api/patients/${patientId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patientData)
    });
    
    if (response.ok) {
      alert("Patient updated successfully!");
      closeEditModal();
      loadPatients(); // Refresh the list
    } else {
      const error = await response.json();
      alert("Error: " + (error.message || "Failed to update patient"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Network error - check console");
  }
}

// ========== DOCTOR FUNCTIONS ==========
async function loadDoctors() {
  try {
    const response = await fetch("/api/doctors");
    const doctors = await response.json();
    populateDoctorDropdown(doctors);
  } catch (error) {
    console.error("Error loading doctors:", error);
  }
}

// Edit doctor function
async function editDoctor(id) {
  try {
    const response = await fetch(`/api/doctors/${id}`);
    const doctor = await response.json();
    
    if (response.ok) {
      const editForm = `
        <div class="edit-modal" id="edit-doctor-modal">
          <div class="modal-content">
            <h2>Edit Doctor: ${doctor.name}</h2>
            <form id="editDoctorForm">
              <input type="hidden" id="editDoctorId" value="${doctor.id}">
              <input type="text" id="editDoctorName" value="${doctor.name || ''}" placeholder="Doctor Name" required>
              <input type="text" id="editDoctorSpecialty" value="${doctor.specialty || ''}" placeholder="Specialty">
              <input type="text" id="editDoctorImage" value="${doctor.image_url || ''}" placeholder="Image URL">
              <div class="modal-buttons">
                <button type="submit">Save Changes</button>
                <button type="button" onclick="closeEditModal()">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      `;
      
      document.body.insertAdjacentHTML('beforeend', editForm);
      
      document.getElementById("editDoctorForm").addEventListener("submit", async function(e) {
        e.preventDefault();
        await updateDoctor();
      });
    }
  } catch (error) {
    console.error("Error fetching doctor:", error);
    alert("Error loading doctor data");
  }
}

async function updateDoctor() {
  const doctorId = document.getElementById("editDoctorId").value;
  const doctorData = {
    name: document.getElementById("editDoctorName").value,
    specialty: document.getElementById("editDoctorSpecialty").value || null,
    image_url: document.getElementById("editDoctorImage").value || null
  };
  
  try {
    const response = await fetch(`/api/doctors/${doctorId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(doctorData)
    });
    
    if (response.ok) {
      alert("Doctor updated successfully!");
      closeEditModal();
      loadDoctors(); // Refresh dropdown
    } else {
      const error = await response.json();
      alert("Error: " + (error.message || "Failed to update doctor"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Network error - check console");
  }
}

// ========== APPOINTMENT FUNCTIONS ==========
async function loadAppointments() {
  try {
    const response = await fetch("/api/appointments");
    const appointments = await response.json();
    displayAppointments(appointments);
  } catch (error) {
    console.error("Error loading appointments:", error);
    document.getElementById("appointments").innerHTML = "<p class='no-results'>Error loading appointments</p>";
  }
}

function displayAppointments(appointments) {
  const container = document.getElementById("appointments");
  updateAppointmentCount(appointments.length);
  
  if (appointments.length === 0) {
    container.innerHTML = "<p class='no-results'>No appointments found</p>";
    return;
  }
  
  container.innerHTML = appointments.map(apt => `
    <div class="appointment-card" id="appointment-${apt.id}">
      <h4>Appointment #${apt.id}</h4>
      <p>Date: ${apt.date} at ${apt.time}</p>
      <p>Patient ID: ${apt.patient_id}</p>
      <p>Doctor ID: ${apt.doctor_id}</p>
      <p>Reason: ${apt.reason || "N/A"}</p>
      <div class="appointment-actions">
        <button class="edit-btn" onclick="editAppointment(${apt.id})">Edit</button>
        <button class="delete-btn" onclick="deleteAppointment(${apt.id})">Cancel</button>
      </div>
    </div>
  `).join("");
}

// Edit appointment
async function editAppointment(id) {
  try {
    const response = await fetch(`/api/appointments/${id}`);
    const appointment = await response.json();
    
    if (response.ok) {
      // We need patients and doctors for dropdowns
      const patientsRes = await fetch("/api/patients");
      const patients = await patientsRes.json();
      const doctorsRes = await fetch("/api/doctors");
      const doctors = await doctorsRes.json();
      
      const patientsOptions = patients.map(p => 
        `<option value="${p.id}" ${p.id == appointment.patient_id ? 'selected' : ''}>${p.name}</option>`
      ).join("");
      
      const doctorsOptions = doctors.map(d => 
        `<option value="${d.id}" ${d.id == appointment.doctor_id ? 'selected' : ''}>Dr. ${d.name}</option>`
      ).join("");
      
      const editForm = `
        <div class="edit-modal" id="edit-appointment-modal">
          <div class="modal-content">
            <h2>Edit Appointment #${appointment.id}</h2>
            <form id="editAppointmentForm">
              <input type="hidden" id="editAppointmentId" value="${appointment.id}">
              <select id="editPatientSelect" required>
                <option value="">Select Patient</option>
                ${patientsOptions}
              </select>
              <select id="editDoctorSelect" required>
                <option value="">Select Doctor</option>
                ${doctorsOptions}
              </select>
              <input type="date" id="editAppointmentDate" value="${appointment.date}" required>
              <input type="time" id="editAppointmentTime" value="${appointment.time}" required>
              <input type="text" id="editAppointmentReason" value="${appointment.reason || ''}" placeholder="Reason">
              <div class="modal-buttons">
                <button type="submit">Save Changes</button>
                <button type="button" onclick="closeEditModal()">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      `;
      
      document.body.insertAdjacentHTML('beforeend', editForm);
      
      document.getElementById("editAppointmentForm").addEventListener("submit", async function(e) {
        e.preventDefault();
        await updateAppointment();
      });
    }
  } catch (error) {
    console.error("Error fetching appointment:", error);
    alert("Error loading appointment data");
  }
}

async function updateAppointment() {
  const appointmentId = document.getElementById("editAppointmentId").value;
  const appointmentData = {
    patient_id: document.getElementById("editPatientSelect").value,
    doctor_id: document.getElementById("editDoctorSelect").value,
    date: document.getElementById("editAppointmentDate").value,
    time: document.getElementById("editAppointmentTime").value,
    reason: document.getElementById("editAppointmentReason").value || null
  };
  
  try {
    const response = await fetch(`/api/appointments/${appointmentId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(appointmentData)
    });
    
    if (response.ok) {
      alert("Appointment updated successfully!");
      closeEditModal();
      loadAppointments(); // Refresh list
    } else {
      const error = await response.json();
      alert("Error: " + (error.message || "Failed to update appointment"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Network error - check console");
  }
}

// ========== DROPDOWN FUNCTIONS ==========
function populatePatientDropdown(patients) {
  const select = document.getElementById("patientSelect");
  if (select) {
    select.innerHTML = '<option value="">Select Patient</option>' + 
      patients.map(p => `<option value="${p.id}">${p.name} (ID: ${p.id})</option>`).join("");
  }
}

function populateDoctorDropdown(doctors) {
  const select = document.getElementById("doctorSelect");
  if (select) {
    select.innerHTML = '<option value="">Select Doctor</option>' + 
      doctors.map(d => `<option value="${d.id}">Dr. ${d.name} - ${d.specialty || "General"}</option>`).join("");
  }
}

// ========== DELETE FUNCTIONS ==========
async function deletePatient(id) {
  if (!confirm("Are you sure you want to delete this patient?")) return;
  
  try {
    const response = await fetch(`/api/patients/${id}`, { method: "DELETE" });
    if (response.ok) {
      alert("Patient deleted successfully!");
      loadPatients();
      loadAppointments();
    }
  } catch (error) {
    console.error("Error deleting patient:", error);
  }
}

async function deleteAppointment(id) {
  if (!confirm("Cancel this appointment?")) return;
  
  try {
    const response = await fetch(`/api/appointments/${id}`, { method: "DELETE" });
    if (response.ok) {
      alert("Appointment cancelled!");
      loadAppointments();
    }
  } catch (error) {
    console.error("Error deleting appointment:", error);
  }
}

// ========== FORM SETUP FUNCTIONS ==========
function setupPatientForm() {
  const form = document.getElementById("patientForm");
  if (form) {
    form.addEventListener("submit", async function(e) {
      e.preventDefault();
      
      const patientData = {
        name: document.getElementById("name").value,
        age: document.getElementById("age").value || null,
        gender: document.getElementById("gender").value || null,
        image_url: document.getElementById("image").value || null
      };
      
      try {
        const response = await fetch("/api/patients", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(patientData)
        });
        
        if (response.ok) {
          alert("Patient added successfully!");
          document.getElementById("patientForm").reset();
          loadPatients();
          loadAppointments();
        } else {
          const error = await response.json();
          alert("Error: " + (error.message || "Failed to add patient"));
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Network error - check console");
      }
    });
  }
}

function setupDoctorForm() {
  const form = document.getElementById("doctorForm");
  if (form) {
    form.addEventListener("submit", async function(e) {
      e.preventDefault();
      
      const doctorData = {
        name: document.getElementById("doctorName").value,
        specialty: document.getElementById("specialty").value || null,
        image_url: document.getElementById("doctorImage").value || null
      };
      
      try {
        const response = await fetch("/api/doctors", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(doctorData)
        });
        
        if (response.ok) {
          alert("Doctor added successfully!");
          document.getElementById("doctorForm").reset();
          loadDoctors();
        } else {
          const error = await response.json();
          alert("Error: " + (error.message || "Failed to add doctor"));
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Network error - check console");
      }
    });
  }
}

function setupAppointmentForm() {
  const form = document.getElementById("appointmentForm");
  if (form) {
    form.addEventListener("submit", async function(e) {
      e.preventDefault();
      
      const appointmentData = {
        patient_id: document.getElementById("patientSelect").value,
        doctor_id: document.getElementById("doctorSelect").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        reason: document.getElementById("reason").value || null
      };
      
      try {
        const response = await fetch("/api/appointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(appointmentData)
        });
        
        if (response.ok) {
          alert("Appointment scheduled successfully!");
          document.getElementById("appointmentForm").reset();
          loadAppointments();
        } else {
          const error = await response.json();
          alert("Error: " + (error.message || "Failed to schedule appointment"));
        }
      } catch (error) {
        console.error("Error:", error);
        alert("Network error - check console");
      }
    });
  }
}

// ========== SEARCH & FILTER FUNCTIONS ==========

// Search patients by name
async function searchPatients() {
  const searchTerm = document.getElementById("searchPatient").value.trim();
  
  if (!searchTerm) {
    alert("Please enter a search term");
    return;
  }
  
  try {
    const response = await fetch(`/api/patients?search=${encodeURIComponent(searchTerm)}`);
    const patients = await response.json();
    displayPatients(patients);
    updatePatientCount(patients.length);
  } catch (error) {
    console.error("Search error:", error);
    document.getElementById("patients").innerHTML = "<p class='no-results'>Error searching patients</p>";
  }
}

// Filter appointments by date
async function filterAppointments() {
  const filterDate = document.getElementById("filterDate").value;
  
  if (!filterDate) {
    alert("Please select a date");
    return;
  }
  
  try {
    const response = await fetch(`/api/appointments?date=${filterDate}`);
    const appointments = await response.json();
    displayAppointments(appointments);
    updateAppointmentCount(appointments.length);
  } catch (error) {
    console.error("Filter error:", error);
    document.getElementById("appointments").innerHTML = "<p class='no-results'>Error filtering appointments</p>";
  }
}

// Clear patient search and show all
function clearPatientSearch() {
  document.getElementById("searchPatient").value = "";
  loadPatients(); // Reload all patients
}

// Clear appointment filter and show all
function clearAppointmentFilter() {
  document.getElementById("filterDate").value = "";
  loadAppointments(); // Reload all appointments
}

// Update count badges
function updatePatientCount(count) {
  const countElement = document.getElementById("patientCount");
  if (countElement) {
    countElement.textContent = `(${count})`;
  }
}

function updateAppointmentCount(count) {
  const countElement = document.getElementById("appointmentCount");
  if (countElement) {
    countElement.textContent = `(${count})`;
  }
}

// ========== MODAL FUNCTION ==========
function closeEditModal() {
  const modals = document.querySelectorAll(".edit-modal");
  modals.forEach(modal => modal.remove());
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

// Doctor Management Functions

// Global variable to store doctors
let doctors = [];

// Load doctors into dropdown
async function loadDoctorsForManagement() {
    try {
        const response = await fetch('/api/doctors');
        doctors = await response.json();
        
        const dropdown = document.getElementById('doctorListDropdown');
        dropdown.innerHTML = '<option value="" disabled selected>Choose a doctor...</option>';
        
        doctors.forEach(doctor => {
            const option = document.createElement('option');
            option.value = doctor.id;
            option.textContent = `${doctor.name} - ${doctor.specialty}`;
            dropdown.appendChild(option);
        });
        
        // Add event listener for dropdown change
        dropdown.addEventListener('change', function() {
            const selectedId = this.value;
            if (selectedId) {
                const doctor = doctors.find(d => d.id == selectedId);
                displaySelectedDoctor(doctor);
            } else {
                hideDoctorInfo();
            }
        });
        
    } catch (error) {
        console.error('Error loading doctors:', error);
    }
}

// Display selected doctor info
function displaySelectedDoctor(doctor) {
    const infoCard = document.getElementById('selectedDoctorInfo');
    const editForm = document.getElementById('doctorEditForm');
    
    // Update doctor info
    document.getElementById('doctorNameDisplay').textContent = doctor.name;
    document.getElementById('doctorSpecialtyDisplay').textContent = doctor.specialty;
    document.getElementById('doctorIdValue').textContent = doctor.id;
    
    // Set image if available
    const imgElement = document.getElementById('doctorImagePreview');
    if (doctor.image) {
        imgElement.src = doctor.image;
        imgElement.style.display = 'block';
    } else {
        imgElement.style.display = 'none';
    }
    
    // Show info card, hide edit form
    infoCard.style.display = 'block';
    editForm.style.display = 'none';
}

// Hide doctor info
function hideDoctorInfo() {
    document.getElementById('selectedDoctorInfo').style.display = 'none';
    document.getElementById('doctorEditForm').style.display = 'none';
}

// View doctor details
function viewDoctorDetails() {
    const dropdown = document.getElementById('doctorListDropdown');
    const doctorId = dropdown.value;
    
    if (!doctorId) {
        alert('Please select a doctor first');
        return;
    }
    
    // In a real app, you might open a modal or navigate to details page
    alert(`Viewing details for doctor ID: ${doctorId}`);
    // You could also implement: window.location.href = `/doctor-details.html?id=${doctorId}`;
}

// Edit selected doctor
function editSelectedDoctor() {
    const dropdown = document.getElementById('doctorListDropdown');
    const doctorId = dropdown.value;
    
    if (!doctorId) {
        alert('Please select a doctor first');
        return;
    }
    
    const doctor = doctors.find(d => d.id == doctorId);
    if (!doctor) return;
    
    // Populate edit form
    document.getElementById('editDoctorId').value = doctor.id;
    document.getElementById('editDoctorName').value = doctor.name;
    document.getElementById('editSpecialty').value = doctor.specialty;
    document.getElementById('editDoctorImage').value = doctor.image || '';
    
    // Show edit form, hide info card
    document.getElementById('selectedDoctorInfo').style.display = 'none';
    document.getElementById('doctorEditForm').style.display = 'block';
}

// Save edited doctor
document.getElementById('editDoctorForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const doctorId = document.getElementById('editDoctorId').value;
    const name = document.getElementById('editDoctorName').value;
    const specialty = document.getElementById('editSpecialty').value;
    const image = document.getElementById('editDoctorImage').value;
    
    try {
        const response = await fetch(`/api/doctors/${doctorId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, specialty, image })
        });
        
        if (response.ok) {
            alert('Doctor updated successfully!');
            
            // Reload doctors
            await loadDoctorsForManagement();
            
            // Reset and hide form
            cancelEdit();
            
            // Select the updated doctor
            document.getElementById('doctorListDropdown').value = doctorId;
            document.getElementById('doctorListDropdown').dispatchEvent(new Event('change'));
        } else {
            alert('Failed to update doctor');
        }
    } catch (error) {
        console.error('Error updating doctor:', error);
        alert('Error updating doctor');
    }
});

// Cancel edit
function cancelEdit() {
    document.getElementById('editDoctorForm').reset();
    document.getElementById('doctorEditForm').style.display = 'none';
    
    const dropdown = document.getElementById('doctorListDropdown');
    if (dropdown.value) {
        document.getElementById('selectedDoctorInfo').style.display = 'block';
    }
}

// Delete selected doctor with confirmation
function deleteSelectedDoctor() {
    const dropdown = document.getElementById('doctorListDropdown');
    const doctorId = dropdown.value;
    
    if (!doctorId) {
        alert('Please select a doctor first');
        return;
    }
    
    const doctor = doctors.find(d => d.id == doctorId);
    if (!doctor) return;
    
    // Create confirmation modal
    const modalHTML = `
        <div class="confirmation-modal">
            <div class="modal-content">
                <h3>Confirm Delete</h3>
                <p>Are you sure you want to delete <strong>${doctor.name}</strong>?</p>
                <p>This action cannot be undone.</p>
                <div class="modal-buttons">
                    <button onclick="confirmDeleteDoctor(${doctorId})" class="confirm-btn">
                        Yes, Delete
                    </button>
                    <button onclick="closeModal()" class="cancel-modal-btn">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Confirm delete
async function confirmDeleteDoctor(doctorId) {
    try {
        const response = await fetch(`/api/doctors/${doctorId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Doctor deleted successfully!');
            
            // Remove modal
            closeModal();
            
            // Reload doctors
            await loadDoctorsForManagement();
            
            // Reset display
            hideDoctorInfo();
            document.getElementById('doctorListDropdown').value = '';
        } else {
            alert('Failed to delete doctor');
        }
    } catch (error) {
        console.error('Error deleting doctor:', error);
        alert('Error deleting doctor');
    }
}

// Close modal
function closeModal() {
    const modal = document.querySelector('.confirmation-modal');
    if (modal) {
        modal.remove();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load doctors for management dropdown
    loadDoctorsForManagement();
    
    // Also load for appointment form (if needed)
    loadDoctorsForDropdown();
});