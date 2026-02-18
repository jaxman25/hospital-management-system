const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("server/hospital.db");

console.log("Adding doctor_id column to appointments table...");

// Check if column exists first
db.get("SELECT * FROM pragma_table_info('appointments') WHERE name='doctor_id'", (err, row) => {
  if (err) {
    console.error("Error checking column:", err.message);
    db.close();
    return;
  }
  
  if (row) {
    console.log("Column 'doctor_id' already exists!");
  } else {
    // Add the missing column
    db.run("ALTER TABLE appointments ADD COLUMN doctor_id INTEGER", (alterErr) => {
      if (alterErr) {
        console.error("Error adding column:", alterErr.message);
      } else {
        console.log(" Column 'doctor_id' added successfully!");
        
        // Update any existing rows with a default value
        db.run("UPDATE appointments SET doctor_id = 1 WHERE doctor_id IS NULL", (updateErr) => {
          if (updateErr) {
            console.error("Warning: Could not set default values:", updateErr.message);
          } else {
            console.log(" Set default doctor_id for existing rows");
          }
          db.close();
        });
      }
    });
  }
});
