#  Hospital Management System

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/jaxman25/Project-2-HOSPITAL-MANAGMENT-SYSTEM)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask)](https://flask.palletsprojects.com/)

A comprehensive hospital management system with patient records, doctor scheduling, pharmacy inventory, and real-time dashboard analytics.

##  Screenshots

*(Add screenshots here after deployment)*

##  Features

###  Patient Management
- Add, edit, and delete patient records
- Medical history tracking
- Appointment scheduling
- Prescription management

###  Doctor Portal
- Doctor profiles and specialties
- Appointment calendar
- Patient assignment
- Availability management

###  Pharmacy Module
- Drug inventory management
- Prescription tracking
- Stock alerts and reordering
- Drug interaction warnings

###  Dashboard
- Real-time statistics
- Patient admission charts
- Revenue analytics
- Staff performance metrics

##  Architecture

\\\
HospitalManagementSystem/
 backend/           # Flask/FastAPI REST API
    api/          # API endpoints
    models/       # Database models
    routes/       # Application routes
    crud/         # Database operations
 frontend/         # Web interface
    static/       # CSS, JS, images
    templates/    # HTML templates
 scripts/          # Automation scripts
 database.py       # Database configuration
 requirements.txt  # Python dependencies
\\\

##  Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   \\\ash
   git clone https://github.com/jaxman25/Project-2-HOSPITAL-MANAGMENT-SYSTEM.git
   cd HospitalManagementSystem
   \\\

2. **Install dependencies:**
   \\\ash
   pip install -r requirements.txt
   \\\

3. **Set up database:**
   \\\ash
   python database.py
   \\\

4. **Run the application:**
   \\\ash
   python app.py
   # or
   python main.py
   \\\

5. **Access the application:**
   - Open browser: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard

### Using PowerShell Scripts (Windows)

\\\powershell
# Start everything with one command
.\start.ps1

# Create sample data
.\create-sample-data.ps1

# Test the system
.\simple_test.ps1
\\\

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/patients | Get all patients |
| POST | /api/patients | Create new patient |
| GET | /api/patients/{id} | Get patient by ID |
| PUT | /api/patients/{id} | Update patient |
| DELETE | /api/patients/{id} | Delete patient |
| GET | /api/doctors | Get all doctors |
| GET | /api/drugs | Get all drugs |
| POST | /api/prescriptions | Create prescription |

##  Database Schema

Key Tables:
- **Patients** - Patient personal & medical information
- **Doctors** - Doctor profiles and specialties  
- **Appointments** - Scheduling information
- **Drugs** - Pharmacy inventory
- **Prescriptions** - Medication orders
- **Users** - System authentication

##  Contributing

1. Fork the repository
2. Create a feature branch (\git checkout -b feature/AmazingFeature\)
3. Commit changes (\git commit -m 'Add AmazingFeature'\)
4. Push to branch (\git push origin feature/AmazingFeature\)
5. Open a Pull Request

##  License

Distributed under MIT License. See \LICENSE\ for more information.

##  Author

**jaxman25**
- GitHub: [@jaxman25](https://github.com/jaxman25)
- Project: [Hospital Management System](https://github.com/jaxman25/Project-2-HOSPITAL-MANAGMENT-SYSTEM)

##  Acknowledgments

- Icons by [FontAwesome](https://fontawesome.com)
- CSS Framework: [Bootstrap](https://getbootstrap.com)
- Database: [SQLAlchemy](https://www.sqlalchemy.org)
- Web Framework: [Flask](https://flask.palletsprojects.com/)
