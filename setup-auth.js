console.log("Setting up authentication system...");

const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("server/hospital.db");

// Create users table
const createTableSQL = `
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'doctor',
    name TEXT NOT NULL,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`;

db.run(createTableSQL, (err) => {
  if (err) {
    console.error("Error creating users table:", err.message);
    db.close();
    return;
  }
  
  console.log(" Users table created");
  
  // Create default admin account
  // Note: We'll use a simple password for now, install bcryptjs separately
  const adminPassword = "admin123"; // In production, use bcrypt
  
  const insertSQL = `
    INSERT OR IGNORE INTO users (username, password, role, name, email) 
    VALUES (?, ?, ?, ?, ?)
  `;
  
  db.run(
    insertSQL,
    ["admin", adminPassword, "admin", "System Administrator", "admin@hospital.com"],
    (err) => {
      if (err) {
        console.error("Error creating admin:", err.message);
      } else {
        console.log(" Default admin account created");
        console.log("  Username: admin");
        console.log("  Password: admin123");
        console.log("  Role: admin");
        console.log("");
        console.log("  WARNING: For production, install bcryptjs:");
        console.log("    npm install bcryptjs");
        console.log("    Then hash passwords properly!");
      }
      db.close();
    }
  );
});
