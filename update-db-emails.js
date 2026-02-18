// Update database schema to include email fields
console.log("Updating database schema for email notifications...");

const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("server/hospital.db");

// Add email column to patients table if it doesn't exist
db.run(`
  ALTER TABLE patients 
  ADD COLUMN email TEXT
`, (err) => {
  if (err && !err.message.includes("duplicate column name")) {
    console.error("Error adding email to patients:", err.message);
  } else {
    console.log(" Patients table updated with email column");
  }
});

// Add email column to doctors table if it doesn't exist
db.run(`
  ALTER TABLE doctors 
  ADD COLUMN email TEXT
`, (err) => {
  if (err && !err.message.includes("duplicate column name")) {
    console.error("Error adding email to doctors:", err.message);
  } else {
    console.log(" Doctors table updated with email column");
  }
});

// Add some test emails to existing records
db.run(`
  UPDATE patients 
  SET email = 'patient' || id || '@example.com' 
  WHERE email IS NULL
`, (err) => {
  if (err) {
    console.error("Error updating patient emails:", err.message);
  } else {
    console.log(" Added test emails to patients");
  }
});

db.run(`
  UPDATE doctors 
  SET email = 'doctor' || id || '@hospital.com' 
  WHERE email IS NULL
`, (err) => {
  if (err) {
    console.error("Error updating doctor emails:", err.message);
  } else {
    console.log(" Added test emails to doctors");
  }
});

db.close(() => {
  console.log(" Database update complete!");
  console.log("Patients and doctors now have email columns.");
  console.log("Test emails have been added to existing records.");
});
