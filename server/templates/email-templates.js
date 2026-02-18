// Email Templates for Hospital Management System

// Appointment Reminder Template
function appointmentReminder(appointment, patient, doctor) {
  const appointmentDate = new Date(appointment.date + 'T' + appointment.time);
  const formattedDate = appointmentDate.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  const formattedTime = appointmentDate.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });

  return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      background: #3498db;
      color: white;
      padding: 20px;
      text-align: center;
      border-radius: 5px 5px 0 0;
    }
    .content {
      background: #f9f9f9;
      padding: 30px;
      border-radius: 0 0 5px 5px;
    }
    .appointment-details {
      background: white;
      border: 1px solid #ddd;
      border-radius: 5px;
      padding: 20px;
      margin: 20px 0;
    }
    .detail-row {
      display: flex;
      margin-bottom: 10px;
    }
    .detail-label {
      font-weight: bold;
      width: 150px;
      color: #2c3e50;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #ddd;
      color: #7f8c8d;
      font-size: 0.9em;
    }
    .button {
      display: inline-block;
      background: #27ae60;
      color: white;
      padding: 12px 25px;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 20px;
    }
    .logo {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="logo"> City General Hospital</div>
    <h1>Appointment Reminder</h1>
  </div>
  
  <div class="content">
    <p>Dear <strong>${patient.name}</strong>,</p>
    
    <p>This is a friendly reminder about your upcoming appointment.</p>
    
    <div class="appointment-details">
      <h3>Appointment Details:</h3>
      <div class="detail-row">
        <div class="detail-label">Date:</div>
        <div>${formattedDate}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Time:</div>
        <div>${formattedTime}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Doctor:</div>
        <div>Dr. ${doctor.name} ${doctor.specialty ? `(${doctor.specialty})` : ''}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Reason:</div>
        <div>${appointment.reason || 'General checkup'}</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">Appointment ID:</div>
        <div>#${appointment.id}</div>
      </div>
    </div>
    
    <h3>Please Remember:</h3>
    <ul>
      <li>Arrive 15 minutes before your scheduled time</li>
      <li>Bring your ID and insurance card</li>
      <li>Bring any relevant medical records or test results</li>
      <li>Notify us if you need to reschedule or cancel</li>
    </ul>
    
    <p>If you need to reschedule or have any questions, please contact our reception at (123) 456-7890.</p>
    
    <div style="text-align: center;">
      <a href="#" class="button">Add to Calendar</a>
    </div>
  </div>
  
  <div class="footer">
    <p>City General Hospital<br>
    123 Medical Center Drive, Health City, HC 12345</p>
    <p>Phone: (123) 456-7890 | Email: contact@cityhospital.example.com</p>
    <p>This is an automated message. Please do not reply to this email.</p>
  </div>
</body>
</html>
  `;
}

// Doctor Notification Template
function doctorAppointmentNotification(appointment, patient, doctor) {
  return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .header { background: #2c3e50; color: white; padding: 20px; }
    .content { padding: 20px; }
    .appointment { background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 15px 0; }
    .footer { background: #ecf0f1; padding: 15px; margin-top: 20px; font-size: 0.9em; }
  </style>
</head>
<body>
  <div class="header">
    <h2>New Appointment Scheduled</h2>
  </div>
  
  <div class="content">
    <p>Dear Dr. <strong>${doctor.name}</strong>,</p>
    
    <p>A new appointment has been scheduled with you:</p>
    
    <div class="appointment">
      <p><strong>Patient:</strong> ${patient.name}</p>
      <p><strong>Date:</strong> ${appointment.date}</p>
      <p><strong>Time:</strong> ${appointment.time}</p>
      <p><strong>Reason:</strong> ${appointment.reason || 'Not specified'}</p>
      <p><strong>Patient ID:</strong> ${patient.id}</p>
    </div>
    
    <p>Please review the appointment details in the Hospital Management System.</p>
  </div>
  
  <div class="footer">
    <p>Hospital Management System Notification</p>
  </div>
</body>
</html>
  `;
}

// Welcome Email for New Patients
function welcomePatient(patient) {
  return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .header { background: #27ae60; color: white; padding: 20px; }
    .content { padding: 20px; }
    .welcome { font-size: 1.2em; margin: 20px 0; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Welcome to Our Hospital!</h1>
  </div>
  
  <div class="content">
    <p>Dear <strong>${patient.name}</strong>,</p>
    
    <div class="welcome">
      Welcome to City General Hospital! We're delighted to have you as our patient.
    </div>
    
    <p>Your patient registration is complete. Your patient ID is: <strong>${patient.id}</strong></p>
    
    <h3>What to do next:</h3>
    <ul>
      <li>Schedule your first appointment with a doctor</li>
      <li>Download our patient portal app (if available)</li>
      <li>Review our hospital policies and patient rights</li>
      <li>Update your medical history in your patient profile</li>
    </ul>
    
    <p>If you have any questions, please don't hesitate to contact us.</p>
    
    <p>Best regards,<br>
    City General Hospital Team</p>
  </div>
</body>
</html>
  `;
}

module.exports = {
  appointmentReminder,
  doctorAppointmentNotification,
  welcomePatient,
};
