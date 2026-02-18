const express = require("express");
const router = express.Router();
const db = require("../db.js");

// GET all doctors
router.get("/", (req, res) => {
  console.log("GET /api/doctors");
  db.all("SELECT * FROM doctors", [], (err, rows) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch doctors" });
    }
    res.json(rows);
  });
});

// GET single doctor by ID
router.get("/:id", (req, res) => {
  const { id } = req.params;
  console.log(`GET /api/doctors/${id}`);
  
  db.get("SELECT * FROM doctors WHERE id = ?", [id], (err, row) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch doctor" });
    }
    if (!row) {
      return res.status(404).json({ error: "Doctor not found" });
    }
    res.json(row);
  });
});

// POST - Create new doctor
router.post("/", (req, res) => {
  console.log("POST /api/doctors:", req.body);
  
  const { name, specialty, image_url } = req.body;
  
  if (!name) {
    return res.status(400).json({ error: "Doctor name is required" });
  }
  
  const sql = `INSERT INTO doctors (name, specialty, image_url) VALUES (?, ?, ?)`;
  
  db.run(sql, [name, specialty || null, image_url || null], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to add doctor: " + err.message });
    }
    res.json({ 
      id: this.lastID, 
      message: "Doctor added successfully",
      name: name
    });
  });
});

// PUT - Update existing doctor
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { name, specialty, image_url } = req.body;
  
  console.log(`PUT /api/doctors/${id}:`, req.body);
  
  if (!name) {
    return res.status(400).json({ error: "Doctor name is required" });
  }
  
  const sql = `UPDATE doctors 
               SET name = ?, specialty = ?, image_url = ?
               WHERE id = ?`;
  
  db.run(sql, [name, specialty || null, image_url || null, id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to update doctor: " + err.message });
    }
    
    if (this.changes === 0) {
      return res.status(404).json({ error: "Doctor not found" });
    }
    
    res.json({ 
      success: true,
      message: "Doctor updated successfully",
      id: id
    });
  });
});

// DELETE doctor
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  db.run("DELETE FROM doctors WHERE id = ?", [id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to delete doctor" });
    }
    res.json({ message: "Doctor deleted successfully" });
  });
});

module.exports = router;
