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
  countElement.textContent = `(${count})`;
}

function updateAppointmentCount(count) {
  const countElement = document.getElementById("appointmentCount");
  countElement.textContent = `(${count})`;
}

// Update display functions to show counts
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

// Update load functions to set initial counts
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

// Add keyboard support for search
document.addEventListener("DOMContentLoaded", function() {
  // Press Enter in search box to search
  document.getElementById("searchPatient").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      searchPatients();
    }
  });
  
  // Press Enter in date filter to filter
  document.getElementById("filterDate").addEventListener("change", function() {
    if (this.value) {
      filterAppointments();
    }
  });
});
