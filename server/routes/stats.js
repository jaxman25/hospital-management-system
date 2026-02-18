const express = require("express");
const router = express.Router();
const db = require("../db.js");

// Get all statistics
router.get("/", (req, res) => {
  console.log("GET /api/stats");
  
  // We'll run multiple queries in parallel
  const stats = {};
  
  // Query 1: Total patients
  db.get("SELECT COUNT(*) as total FROM patients", (err, row) => {
    if (err) {
      console.error("Patients count error:", err.message);
      stats.totalPatients = 0;
    } else {
      stats.totalPatients = row.total;
    }
    checkComplete();
  });
  
  // Query 2: Total doctors
  db.get("SELECT COUNT(*) as total FROM doctors", (err, row) => {
    if (err) {
      console.error("Doctors count error:", err.message);
      stats.totalDoctors = 0;
    } else {
      stats.totalDoctors = row.total;
    }
    checkComplete();
  });
  
  // Query 3: Total appointments
  db.get("SELECT COUNT(*) as total FROM appointments", (err, row) => {
    if (err) {
      console.error("Appointments count error:", err.message);
      stats.totalAppointments = 0;
    } else {
      stats.totalAppointments = row.total;
    }
    checkComplete();
  });
  
  // Query 4: Today's appointments
  const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  db.get("SELECT COUNT(*) as total FROM appointments WHERE date = ?", [today], (err, row) => {
    if (err) {
      console.error("Today's appointments error:", err.message);
      stats.todaysAppointments = 0;
    } else {
      stats.todaysAppointments = row.total;
    }
    checkComplete();
  });
  
  // Query 5: Upcoming appointments (next 7 days)
  const nextWeek = new Date();
  nextWeek.setDate(nextWeek.getDate() + 7);
  const nextWeekStr = nextWeek.toISOString().split('T')[0];
  
  db.get(
    `SELECT COUNT(*) as total FROM appointments 
     WHERE date BETWEEN ? AND ?`,
    [today, nextWeekStr],
    (err, row) => {
      if (err) {
        console.error("Upcoming appointments error:", err.message);
        stats.upcomingAppointments = 0;
      } else {
        stats.upcomingAppointments = row.total;
      }
      checkComplete();
    }
  );
  
  // Query 6: Patients by gender
  db.all(
    `SELECT gender, COUNT(*) as count 
     FROM patients 
     WHERE gender IS NOT NULL AND gender != ''
     GROUP BY gender`,
    (err, rows) => {
      if (err) {
        console.error("Gender stats error:", err.message);
        stats.genderDistribution = [];
      } else {
        stats.genderDistribution = rows;
      }
      checkComplete();
    }
  );
  
  // Query 7: Appointments by day (last 7 days)
  const weekAgo = new Date();
  weekAgo.setDate(weekAgo.getDate() - 7);
  const weekAgoStr = weekAgo.toISOString().split('T')[0];
  
  db.all(
    `SELECT date, COUNT(*) as count 
     FROM appointments 
     WHERE date BETWEEN ? AND ?
     GROUP BY date 
     ORDER BY date`,
    [weekAgoStr, today],
    (err, rows) => {
      if (err) {
        console.error("Weekly appointments error:", err.message);
        stats.weeklyAppointments = [];
      } else {
        stats.weeklyAppointments = rows;
      }
      checkComplete();
    }
  );
  
  // Query 8: Most booked doctors
  db.all(
    `SELECT d.name, d.specialty, COUNT(a.id) as appointment_count
     FROM appointments a
     JOIN doctors d ON a.doctor_id = d.id
     GROUP BY a.doctor_id
     ORDER BY appointment_count DESC
     LIMIT 5`,
    (err, rows) => {
      if (err) {
        console.error("Top doctors error:", err.message);
        stats.topDoctors = [];
      } else {
        stats.topDoctors = rows;
      }
      checkComplete();
    }
  );
  
  let completedQueries = 0;
  const totalQueries = 8;
  
  function checkComplete() {
    completedQueries++;
    if (completedQueries === totalQueries) {
      console.log("Statistics calculated:", stats);
      res.json(stats);
    }
  }
});

// Get detailed appointment statistics
router.get("/appointments", (req, res) => {
  console.log("GET /api/stats/appointments");
  
  const stats = {};
  
  // Monthly appointments
  db.all(
    `SELECT strftime('%Y-%m', date) as month, COUNT(*) as count
     FROM appointments
     GROUP BY strftime('%Y-%m', date)
     ORDER BY month DESC
     LIMIT 12`,
    (err, rows) => {
      if (err) {
        console.error("Monthly stats error:", err.message);
        stats.monthly = [];
      } else {
        stats.monthly = rows;
      }
      
      // Send response
      res.json(stats);
    }
  );
});

module.exports = router;
