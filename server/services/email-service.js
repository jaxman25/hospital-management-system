// Email Service for Hospital Management System
const cron = require("node-cron");
const db = require("../db.js");
const { sendEmail } = require("../config/email.js");
const { 
  appointmentReminder, 
  doctorAppointmentNotification,
  welcomePatient 
} = require("../templates/email-templates.js");

class EmailService {
  constructor() {
    this.isRunning = false;
  }
  
  // Start the email scheduler
  start() {
    if (this.isRunning) {
      console.log(" Email scheduler is already running");
      return;
    }
    
    console.log(" Starting email scheduler...");
    
    // Schedule daily email check at 8 AM
    // cron syntax: "0 8 * * *" = At 08:00 every day
    // For testing: "*/5 * * * *" = Every 5 minutes
    cron.schedule("0 8 * * *", () => {
      console.log(" Running scheduled email check...");
      this.sendDailyReminders();
    });
    
    // For testing: Run every 5 minutes
    cron.schedule("*/5 * * * *", () => {
      console.log(" Test mode: Checking for reminders...");
      this.sendDailyReminders();
    });
    
    this.isRunning = true;
    console.log(" Email scheduler started");
    console.log("   - Daily reminders at 8:00 AM");
    console.log("   - Test mode: Every 5 minutes");
  }
  
  // Send appointment reminders for tomorrow
  async sendDailyReminders() {
    try {
      // Get tomorrow's date (YYYY-MM-DD)
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomorrowStr = tomorrow.toISOString().split('T')[0];
      
      console.log(` Looking for appointments on: ${tomorrowStr}`);
      
      // Get appointments for tomorrow with patient and doctor info
      const sql = `
        SELECT a.*, p.name as patient_name, p.email as patient_email,
               d.name as doctor_name, d.specialty, d.email as doctor_email
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.date = ?
      `;
      
      db.all(sql, [tomorrowStr], async (err, appointments) => {
        if (err) {
          console.error(" Database error fetching appointments:", err.message);
          return;
        }
        
        console.log(` Found ${appointments.length} appointments for tomorrow`);
        
        // Send reminder for each appointment
        for (const appointment of appointments) {
          await this.sendAppointmentReminder(appointment);
        }
      });
      
    } catch (error) {
      console.error(" Error in sendDailyReminders:", error.message);
    }
  }
  
  // Send reminder for a specific appointment
  async sendAppointmentReminder(appointment) {
    try {
      // Prepare data
      const patient = {
        name: appointment.patient_name,
        email: appointment.patient_email,
        id: appointment.patient_id
      };
      
      const doctor = {
        name: appointment.doctor_name,
        specialty: appointment.specialty,
        email: appointment.doctor_email
      };
      
      // Check if patient has email
      if (!patient.email) {
        console.log(`     Patient ${patient.name} has no email, skipping reminder`);
        return;
      }
      
      // Create email content
      const htmlContent = appointmentReminder(appointment, patient, doctor);
      const subject = `Reminder: Appointment Tomorrow with Dr. ${doctor.name}`;
      
      console.log(`    Sending reminder to ${patient.name} <${patient.email}>`);
      
      // Send email
      const result = await sendEmail(patient.email, subject, htmlContent);
      
      if (result.success) {
        console.log(`    Reminder sent to ${patient.name}`);
        
        // Also notify doctor if they have email
        if (doctor.email) {
          await this.sendDoctorNotification(appointment, patient, doctor);
        }
      }
      
    } catch (error) {
      console.error(` Error sending reminder for appointment ${appointment.id}:`, error.message);
    }
  }
  
  // Send notification to doctor
  async sendDoctorNotification(appointment, patient, doctor) {
    try {
      const htmlContent = doctorAppointmentNotification(appointment, patient, doctor);
      const subject = `New Appointment: ${patient.name} on ${appointment.date}`;
      
      console.log(`    Notifying Dr. ${doctor.name} <${doctor.email}>`);
      
      await sendEmail(doctor.email, subject, htmlContent);
      console.log(`    Doctor notified`);
      
    } catch (error) {
      console.error(` Error notifying doctor:`, error.message);
    }
  }
  
  // Send welcome email to new patient
  async sendWelcomeEmail(patient) {
    try {
      if (!patient.email) {
        console.log(`     Patient ${patient.name} has no email, skipping welcome email`);
        return { success: false, error: "No email address" };
      }
      
      const htmlContent = welcomePatient(patient);
      const subject = `Welcome to City General Hospital, ${patient.name}!`;
      
      console.log(` Sending welcome email to ${patient.name} <${patient.email}>`);
      
      const result = await sendEmail(patient.email, subject, htmlContent);
      
      if (result.success) {
        console.log(` Welcome email sent to ${patient.name}`);
      }
      
      return result;
      
    } catch (error) {
      console.error(` Error sending welcome email:`, error.message);
      return { success: false, error: error.message };
    }
  }
  
  // Manually trigger reminders (for testing)
  async sendTestReminders() {
    console.log(" Sending test reminders...");
    
    // Get today's appointments for testing
    const today = new Date().toISOString().split('T')[0];
    
    const sql = `
      SELECT a.*, p.name as patient_name, p.email as patient_email,
             d.name as doctor_name, d.specialty, d.email as doctor_email
      FROM appointments a
      JOIN patients p ON a.patient_id = p.id
      JOIN doctors d ON a.doctor_id = d.id
      WHERE a.date = ?
      LIMIT 2
    `;
    
    db.all(sql, [today], async (err, appointments) => {
      if (err) {
        console.error("Database error:", err.message);
        return;
      }
      
      console.log(`Found ${appointments.length} appointments for testing`);
      
      for (const appointment of appointments) {
        await this.sendAppointmentReminder(appointment);
      }
      
      console.log(" Test reminders completed");
    });
  }
}

// Create singleton instance
const emailService = new EmailService();

module.exports = emailService;
