#  Hospital Management System

A modern, FastAPI-based Hospital Management System with web interface and RESTful API.

##  Quick Start

### Prerequisites
- Python 3.8+
- Git (optional)

### Installation
1. Clone the repository:
   \\\ash
   git clone https://github.com/jaxman25/Project-2-HOSPITAL-MANAGMENT-SYSTEM.git
   cd Project-2-HOSPITAL-MANAGMENT-SYSTEM
   \\\

2. Set up virtual environment:
   \\\ash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # Or: source venv/bin/activate  # Linux/Mac
   \\\

3. Install dependencies:
   \\\ash
   pip install -r requirements.txt
   \\\

### Running the System
1. Start the server:
   \\\ash
   python -m uvicorn minimal_main:app --reload --host 0.0.0.0 --port 8000
   \\\

2. Open in browser:
   - **Dashboard**: http://localhost:8000/dashboard
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/api/health

##  Features

###  Currently Implemented
- **Doctors Management**: CRUD operations for doctors
- **Patients Management**: CRUD operations for patients  
- **RESTful API**: Fully documented API with Swagger UI
- **Web Dashboard**: User-friendly web interface
- **Health Monitoring**: System health check endpoint
- **CORS Support**: Cross-origin resource sharing enabled

###  API Endpoints
- \GET /api/health\ - System health status
- \GET /api/doctors\ - List all doctors
- \POST /api/doctors\ - Create new doctor
- \GET /api/patients\ - List all patients
- \POST /api/patients\ - Create new patient
- \GET /docs\ - Interactive API documentation
- \GET /dashboard\ - Web dashboard

##  Technology Stack

- **Backend**: FastAPI (Python)
- **API Documentation**: Swagger UI / ReDoc
- **Frontend**: HTML/CSS with Jinja2 templates
- **Development Server**: Uvicorn
- **Virtual Environment**: Python venv

##  Project Structure

\\\
project/
 minimal_main.py          # Main FastAPI application
 requirements.txt         # Python dependencies
 venv/                   # Virtual environment
 backend/                # Database models and configuration
 routes/                 # API route definitions
 templates/              # HTML templates
 schemas/                # Pydantic schemas
 static/                 # Static files (CSS, JS, images)
\\\

##  Usage Examples

### Using the API with curl:
\\\ash
# Get all doctors
curl http://localhost:8000/api/doctors

# Create a new doctor
curl -X POST http://localhost:8000/api/doctors \\
  -H "Content-Type: application/json" \\
  -d '{\"name\": \"Dr. Sarah Wilson\", \"specialization\": \"Cardiology\"}'

# Get all patients
curl http://localhost:8000/api/patients
\\\

### Using the Web Interface:
1. Open http://localhost:8000/dashboard
2. Navigate using the menu
3. View doctors, patients, and system status

##  Troubleshooting

### Common Issues:

1. **Port 8000 already in use**:
   \\\ash
   # Find and kill the process
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   \\\

2. **Module not found errors**:
   \\\ash
   # Make sure virtual environment is activated
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   \\\

3. **Server not starting**:
   \\\ash
   # Check Python version
   python --version
   
   # Try minimal version
   python -m uvicorn minimal_main:app --reload --port 8000
   \\\

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

##  Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Documentation with [Swagger UI](https://swagger.io/tools/swagger-ui/)
- Icons from [Font Awesome](https://fontawesome.com/)

---

** Happy Coding!** If you have any questions or issues, please open an issue on GitHub.
