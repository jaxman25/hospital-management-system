const express = require("express");
const router = express.Router();
const db = require("../db.js");
const bcrypt = require("bcryptjs");

// User registration (for new doctors)
router.post("/register", (req, res) => {
  console.log("POST /api/auth/register:", req.body);
  
  const { username, password, name, email, role = "doctor" } = req.body;
  
  // Validate input
  if (!username || !password || !name) {
    return res.status(400).json({ 
      error: "Username, password, and name are required" 
    });
  }
  
  if (password.length < 6) {
    return res.status(400).json({ 
      error: "Password must be at least 6 characters" 
    });
  }
  
  // Check if username already exists
  db.get("SELECT id FROM users WHERE username = ?", [username], (err, row) => {
    if (err) {
      console.error("Database error:", err.message);
      return res.status(500).json({ error: "Database error" });
    }
    
    if (row) {
      return res.status(400).json({ error: "Username already exists" });
    }
    
    // Hash password
    bcrypt.hash(password, 10, (hashErr, hashedPassword) => {
      if (hashErr) {
        console.error("Password hash error:", hashErr);
        return res.status(500).json({ error: "Registration failed" });
      }
      
      // Insert new user
      const insertSQL = `INSERT INTO users (username, password, role, name, email) 
                         VALUES (?, ?, ?, ?, ?)`;
      
      db.run(
        insertSQL,
        [username, hashedPassword, role, name, email || null],
        function(err) {
          if (err) {
            console.error("Insert error:", err.message);
            return res.status(500).json({ error: "Failed to create user" });
          }
          
          // Don't send password back
          res.json({
            success: true,
            message: "User registered successfully",
            user: {
              id: this.lastID,
              username,
              name,
              role,
              email
            }
          });
        }
      );
    });
  });
});

// User login
router.post("/login", (req, res) => {
  console.log("POST /api/auth/login:", req.body.username);
  
  const { username, password } = req.body;
  
  if (!username || !password) {
    return res.status(400).json({ 
      error: "Username and password are required" 
    });
  }
  
  // Find user
  db.get("SELECT * FROM users WHERE username = ?", [username], (err, user) => {
    if (err) {
      console.error("Database error:", err.message);
      return res.status(500).json({ error: "Database error" });
    }
    
    if (!user) {
      return res.status(401).json({ error: "Invalid username or password" });
    }
    
    // Check password with bcrypt
    bcrypt.compare(password, user.password, (compareErr, isValidPassword) => {
      if (compareErr) {
        console.error("Password compare error:", compareErr);
        return res.status(500).json({ error: "Authentication error" });
      }
      
      if (!isValidPassword) {
        return res.status(401).json({ error: "Invalid username or password" });
      }
      
      // Create session
      req.session.userId = user.id;
      req.session.username = user.username;
      req.session.role = user.role;
      req.session.name = user.name;
      
      // Don't send password back
      const { password: _, ...userWithoutPassword } = user;
      
      console.log(` Login successful: ${user.username} (${user.role})`);
      
      res.json({
        success: true,
        message: "Login successful",
        user: userWithoutPassword
      });
    });
  });
});

// Get current user info
router.get("/me", (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }
  
  db.get(
    "SELECT id, username, role, name, email, created_at FROM users WHERE id = ?",
    [req.session.userId],
    (err, user) => {
      if (err) {
        console.error("Database error:", err.message);
        return res.status(500).json({ error: "Database error" });
      }
      
      if (!user) {
        return res.status(404).json({ error: "User not found" });
      }
      
      res.json({ user });
    }
  );
});

// User logout
router.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error("Logout error:", err);
      return res.status(500).json({ error: "Logout failed" });
    }
    
    res.json({ success: true, message: "Logged out successfully" });
  });
});

module.exports = router;
