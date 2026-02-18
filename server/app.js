const express = require("express");
const path = require("path");
const session = require("express-session");

const app = express();

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

// Session configuration
app.use(
  session({
    secret: process.env.SESSION_SECRET || "hospital-secret-key",
    resave: false,
    saveUninitialized: false,
    cookie: {
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
      httpOnly: true,
      secure: false // Set to true in production with HTTPS
    }
  })
);

// Authentication middleware
function requireAuth(req, res, next) {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Authentication required" });
  }
  next();
}

// Import routes
const authRoutes = require("./routes/auth");
const patientRoutes = require("./routes/patients");
const doctorRoutes = require("./routes/doctors");
const appointmentRoutes = require("./routes/appointments");
const statsRoutes = require("./routes/stats");

// Public routes
app.use("/api/auth", authRoutes);

// Protected API routes
app.use("/api/patients", requireAuth, patientRoutes);
app.use("/api/doctors", requireAuth, doctorRoutes);
app.use("/api/appointments", requireAuth, appointmentRoutes);
app.use("/api/stats", requireAuth, statsRoutes);

// Public pages
app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/login.html"));
});

// Protected pages
app.get("/dashboard", requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, "../public/dashboard.html"));
});

app.get("/app", requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Health check (public)
app.get("/health", (req, res) => {
  res.send("OK");
});

// Root redirect
app.get("/", (req, res) => {
  if (req.session.userId) {
    res.redirect("/dashboard");
  } else {
    res.redirect("/login");
  }
});

// Handle 404
app.use((req, res) => {
  res.status(404).sendFile(path.join(__dirname, "../public/404.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(` Server running on http://localhost:${PORT}`);
  console.log(` Dashboard: http://localhost:${PORT}/dashboard`);
  console.log(` Main App: http://localhost:${PORT}/app`);
  console.log(` Login: http://localhost:${PORT}/login`);
});
