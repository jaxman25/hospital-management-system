Write-Host "Creating sample hospital data..." -ForegroundColor Cyan

# Create patients
1..10 | ForEach-Object {
    {
    "first_name":  "John",
    "date_of_birth":  "1990-05-15",
    "gender":  "Male",
    "contact_number":  "+1-555-0123",
    "email":  "john.doe@example.com",
    "blood_group":  "O+",
    "last_name":  "Doe"
} = @{
        first_name = "Patient"
        last_name = "Test"
        date_of_birth = "1980-01-"
        contact_number = "+1-555-010"
        email = "patient@hospital.com"
        gender = if ( % 2 -eq 0) { "Female" } else { "Male" }
        blood_group = @("A+", "B+", "O+", "AB+")[( % 4)]
    } | ConvertTo-Json
    
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/api/patients" 
            -Method Post 
            -Body {
    "first_name":  "John",
    "date_of_birth":  "1990-05-15",
    "gender":  "Male",
    "contact_number":  "+1-555-0123",
    "email":  "john.doe@example.com",
    "blood_group":  "O+",
    "last_name":  "Doe"
} 
            -ContentType "application/json" | Out-Null
        Write-Host "  Created patient " -ForegroundColor Green
    } catch { }
}

# Create appointments
1..5 | ForEach-Object {
     = @{
        patient_id = "existing-patient-id"  # Get from your patients list
        doctor_id = "existing-doctor-id"    # Get from your doctors list
        appointment_date = (Get-Date).AddDays().ToString("yyyy-MM-dd")
        appointment_time = "09:00"
        type = "consultation"
        duration = 30
        notes = "Follow-up appointment "
    } | ConvertTo-Json
    
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/api/appointments" 
            -Method Post 
            -Body  
            -ContentType "application/json" | Out-Null
        Write-Host "  Created appointment " -ForegroundColor Green
    } catch { }
}

Write-Host " Sample data creation complete!" -ForegroundColor Green
