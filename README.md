# 🏥 Hospital Management System

A comprehensive web-based Hospital Management System built with Node.js, Express, and SQLite for managing hospital operations including patient records, doctor schedules, appointments, and more.

## 📋 Features

- **User Authentication**: Secure login and registration for different user roles (admin, doctors, staff)
- **Patient Management**: Add, view, update, and manage patient information
- **Doctor Management**: Manage doctor profiles, specializations, and schedules
- **Appointment Scheduling**: Book and manage patient appointments
- **Dashboard**: Interactive dashboard with key statistics and metrics
- **Email Notifications**: Automated email notifications for appointments and updates
- **Database**: SQLite database for efficient data storage

## 🚀 Technology Stack

- **Backend**: Node.js, Express.js
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **Authentication**: Express Session, bcryptjs
- **Email Service**: Nodemailer
- **Other Tools**: Node-cron for scheduled tasks, Express Validator for input validation

## 📁 Project Structure
├── backend/ # Backend server code
├── frontend/ # Frontend client code
│ ├── css/ # Stylesheets
│ ├── js/ # JavaScript files
│ └── *.html # HTML pages
├── server/ # Express server files
├── public/ # Static assets
├── config/ # Configuration files
├── routes/ # API routes
├── services/ # Business logic services
├── templates/ # Email templates
├── utils/ # Utility functions
├── database/ # Database related files
├── .env # Environment variables
├── hospital.db # SQLite database
├── package.json # Dependencies
└── README.md # This file

text

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaxman25/hospital-management-system.git
   cd hospital-management-system
Install dependencies

bash
npm install
Configure environment variables
Create a .env file in the root directory:

env
PORT=3000
SESSION_SECRET=your_secret_key_here
# Add email configuration if using nodemailer
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
Initialize the database

bash
node check.js
node add-column.js
node check-columns.js
node setup-auth.js
Start the application

bash
# Development mode
npm run dev

# Production mode
npm start
Access the application
Open your browser and navigate to http://localhost:3000

📊 Database Management
The project includes several utility scripts for database management:

add-column.js - Add new columns to existing tables

check-columns.js - Verify database schema

check.js - General database checks

setup-auth.js - Set up authentication tables

update-db-emails.js - Update email-related fields

🔧 Available Scripts
npm start - Start the production server

npm run dev - Start development server with auto-restart

node test.js - Run tests

🚦 Usage
Register/Login: Create an account or login with existing credentials

Dashboard: View key metrics and statistics

Manage Patients: Add and manage patient information

Schedule Appointments: Book appointments with doctors

View Reports: Access various reports and analytics

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the ISC License.

📧 Contact
My name - John Bundi

My email - bundij69@gmail.com

Project Link: https://github.com/jaxman25/hospital-management-system

🙏 Acknowledgments
Thanks to all contributors

Built with Node.js and Express

SQLite for lightweight database management