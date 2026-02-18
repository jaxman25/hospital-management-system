const express = require("express");
const router = express.Router();
const db = require("../db.js");

// GET all appointments OR filter by date
router.get("/", (req, res) => {
  const filterDate = req.query.date;
  console.log("GET /api/appointments", filterDate ? `date: "${filterDate}"` : "");
  
  let sql = "SELECT * FROM appointments";
  let params = [];
  
  if (filterDate) {
    sql += " WHERE date = ?";
    params.push(filterDate);
  }
  
  sql += " ORDER BY date DESC, time DESC";
  
  db.all(sql, params, (err, rows) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch appointments" });
    }
    res.json(rows);
  });
});

// GET single appointment by ID
router.get("/:id", (req, res) => {
  const { id } = req.params;
  console.log(`GET /api/appointments/${id}`);
  
  db.get("SELECT * FROM appointments WHERE id = ?", [id], (err, row) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch appointment" });
    }
    if (!row) {
      return res.status(404).json({ error: "Appointment not found" });
    }
    res.json(row);
  });
});

// POST - Create new appointment
router.post("/", (req, res) => {
  console.log("POST /api/appointments:", req.body);
  
  const { patient_id, doctor_id, date, time, reason } = req.body;
  
  if (!patient_id || !doctor_id || !date || !time) {
    const missing = [];
    if (!patient_id) missing.push("patient_id");
    if (!doctor_id) missing.push("doctor_id");
    if (!date) missing.push("date");
    if (!time) missing.push("time");
    
    return res.status(400).json({ 
      error: "Missing required fields", 
      missing: missing 
    });
  }
  
  const sql = `INSERT INTO appointments (patient_id, doctor_id, date, time, reason) 
               VALUES (?, ?, ?, ?, ?)`;
  
  db.run(sql, [patient_id, doctor_id, date, time, reason || null], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to create appointment: " + err.message });
    }
    res.json({ 
      id: this.lastID, 
      message: "Appointment scheduled successfully"
    });
  });
});

// PUT - Update existing appointment
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { patient_id, doctor_id, date, time, reason } = req.body;
  
  console.log(`PUT /api/appointments/${id}:`, req.body);
  
  if (!patient_id || !doctor_id || !date || !time) {
    const missing = [];
    if (!patient_id) missing.push("patient_id");
    if (!doctor_id) missing.push("doctor_id");
    if (!date) missing.push("date");
    if (!time) missing.push("time");
    
    return res.status(400).json({ 
      error: "Missing required fields", 
      missing: missing 
    });
  }
  
  const sql = `UPDATE appointments 
               SET patient_id = ?, doctor_id = ?, date = ?, time = ?, reason = ?
               WHERE id = ?`;
  
  db.run(sql, [patient_id, doctor_id, date, time, reason || null, id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to update appointment: " + err.message });
    }
    
    if (this.changes === 0) {
      return res.status(404).json({ error: "Appointment not found" });
    }
    
    res.json({ 
      success: true,
      message: "Appointment updated successfully",
      id: id
    });
  });
});

// DELETE appointment
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  db.run("DELETE FROM appointments WHERE id = ?", [id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to delete appointment" });
    }
    res.json({ message: "Appointment deleted successfully" });
  });
});

module.exports = router;
