const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("server/hospital.db");

console.log("Checking appointments table structure...");

db.all("PRAGMA table_info(appointments)", (err, columns) => {
  if (err) {
    console.error("Error:", err.message);
  } else if (columns.length === 0) {
    console.log("Table 'appointments' doesn't exist or has no columns");
  } else {
    console.log("CURRENT COLUMNS in 'appointments':");
    console.log("----------------------------");
    columns.forEach(col => {
      console.log(`  ${col.name} (${col.type}) ${col.notnull ? "NOT NULL" : ""} ${col.pk ? "PRIMARY KEY" : ""}`);
    });
    console.log("----------------------------");
  }
  db.close();
});
