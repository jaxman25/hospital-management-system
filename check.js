console.log("Checking database tables...");
const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("server/hospital.db", (err) => {
  if (err) {
    console.error("Connection error:", err.message);
    return;
  }
  
  db.all("SELECT name FROM sqlite_master WHERE type='table'", (err, tables) => {
    if (err) {
      console.error("Error:", err.message);
    } else if (!tables || tables.length === 0) {
      console.log("NO TABLES FOUND - Database is empty");
    } else {
      console.log("TABLES FOUND (" + tables.length + "):");
      tables.forEach(t => console.log("   " + t.name));
    }
    db.close();
  });
});
