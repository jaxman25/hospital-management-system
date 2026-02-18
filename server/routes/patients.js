const express = require("express");
const router = express.Router();
const db = require("../db.js");

// GET all patients OR search by name
router.get("/", (req, res) => {
  const search = req.query.search;
  console.log("GET /api/patients", search ? `search: "${search}"` : "");
  
  let sql = "SELECT * FROM patients";
  let params = [];
  
  if (search && search.trim()) {
    sql += " WHERE name LIKE ?";
    params.push(`%${search.trim()}%`);
  }
  
  sql += " ORDER BY name";
  
  db.all(sql, params, (err, rows) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch patients" });
    }
    res.json(rows);
  });
});

// GET single patient by ID
router.get("/:id", (req, res) => {
  const { id } = req.params;
  console.log(`GET /api/patients/${id}`);
  
  db.get("SELECT * FROM patients WHERE id = ?", [id], (err, row) => {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to fetch patient" });
    }
    if (!row) {
      return res.status(404).json({ error: "Patient not found" });
    }
    res.json(row);
  });
});

// POST - Create new patient
router.post("/", (req, res) => {
  console.log("POST /api/patients:", req.body);
  
  const { name, age, gender, image_url } = req.body;
  
  if (!name) {
    return res.status(400).json({ error: "Patient name is required" });
  }
  
  const sql = `INSERT INTO patients (name, age, gender, image_url) VALUES (?, ?, ?, ?)`;
  
  db.run(sql, [name, age || null, gender || null, image_url || null], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to add patient: " + err.message });
    }
    res.json({ 
      id: this.lastID, 
      message: "Patient added successfully",
      name: name
    });
  });
});

// PUT - Update existing patient
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { name, age, gender, image_url } = req.body;
  
  console.log(`PUT /api/patients/${id}:`, req.body);
  
  if (!name) {
    return res.status(400).json({ error: "Patient name is required" });
  }
  
  const sql = `UPDATE patients 
               SET name = ?, age = ?, gender = ?, image_url = ?
               WHERE id = ?`;
  
  db.run(sql, [name, age || null, gender || null, image_url || null, id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to update patient: " + err.message });
    }
    
    if (this.changes === 0) {
      return res.status(404).json({ error: "Patient not found" });
    }
    
    res.json({ 
      success: true,
      message: "Patient updated successfully",
      id: id
    });
  });
});

// DELETE patient
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  db.run("DELETE FROM patients WHERE id = ?", [id], function(err) {
    if (err) {
      console.error("Error:", err.message);
      return res.status(500).json({ error: "Failed to delete patient" });
    }
    res.json({ message: "Patient deleted successfully" });
  });
});

module.exports = router;
