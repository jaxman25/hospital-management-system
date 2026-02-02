Write-Host " Testing Pharmacy Management Module" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

 = "http://localhost:8000/api/v1/pharmacy"

# 1. Test drug endpoints
Write-Host "
1. Testing drug endpoints..." -ForegroundColor Yellow

# Create a test drug
 = @{
    brand_name = "Paracetamol 500mg"
    generic_name = "Acetaminophen"
    drug_type = "tablet"
    strength = "500mg"
    unit = "tablet"
    category = "Analgesic"
    manufacturer = "Generic Pharma"
    prescription_required = False
    storage_conditions = '{"temperature": "room", "humidity": "low"}'
    side_effects = '["nausea", "rash", "headache"]'
    contraindications = '["liver disease", "alcoholism"]'
} | ConvertTo-Json

try {
     = Invoke-RestMethod -Uri "/drugs" 
        -Method Post 
        -Body  
        -ContentType "application/json"
    
    Write-Host " Drug created: " -ForegroundColor Green
     = .drug_id
} catch {
    Write-Host " Failed to create drug: " -ForegroundColor Red
}

# 2. Test inventory endpoints
if () {
    Write-Host "
2. Testing inventory endpoints..." -ForegroundColor Yellow
    
     = @{
        drug_id = 
        batch_number = "BATCH001"
        quantity = 1000
        unit_price = 0.05
        selling_price = 0.10
        expiry_date = (Get-Date).AddYears(1).ToString("yyyy-MM-dd")
        location = "Shelf A1"
        reorder_level = 100
        reorder_quantity = 500
    } | ConvertTo-Json
    
    try {
         = Invoke-RestMethod -Uri "/inventory" 
            -Method Post 
            -Body  
            -ContentType "application/json"
        
        Write-Host " Inventory added:  units" -ForegroundColor Green
    } catch {
        Write-Host " Failed to add inventory: " -ForegroundColor Red
    }
}

# 3. Test supplier endpoints
Write-Host "
3. Testing supplier endpoints..." -ForegroundColor Yellow

 = @{
    name = "MediSupplies Inc."
    contact_person = "John Supplier"
    email = "john@medisupplies.com"
    phone = "+1-800-MED-SUP"
    address = '{"street": "123 Pharma St", "city": "MedCity", "state": "MC", "zip": "12345"}'
    tax_id = "TAX-12345"
    payment_terms = "Net 30"
    delivery_time = 7
} | ConvertTo-Json

try {
     = Invoke-RestMethod -Uri "/suppliers" 
        -Method Post 
        -Body  
        -ContentType "application/json"
    
    Write-Host " Supplier created: " -ForegroundColor Green
     = .supplier_id
} catch {
    Write-Host " Failed to create supplier: " -ForegroundColor Red
}

# 4. Test prescription endpoints
Write-Host "
4. Testing prescription endpoints..." -ForegroundColor Yellow

# First get a patient and doctor
try {
    @{count=0; patients=System.Object[]} = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients" -Method Get
    @{count=2; doctors=System.Object[]} = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/doctors" -Method Get
    
    if (@{count=0; patients=System.Object[]}.count -gt 0 -and @{count=2; doctors=System.Object[]}.count -gt 0) {
         = @{count=0; patients=System.Object[]}.patients[0].id
         = @{count=2; doctors=System.Object[]}.doctors[0].id
        
         = @{
            patient_id = 
            doctor_id = 
            items = @(
                @{
                    drug_id = 
                    quantity = 30
                    dosage = "500mg"
                    frequency = "Every 6 hours"
                    duration = "5 days"
                    instructions = "Take with food"
                }
            )
            validity_days = 30
            notes = "Test prescription"
        } | ConvertTo-Json
        
         = Invoke-RestMethod -Uri "/prescriptions" 
            -Method Post 
            -Body  
            -ContentType "application/json"
        
        Write-Host " Prescription created: " -ForegroundColor Green
         = .prescription_id
    }
} catch {
    Write-Host " Failed to create prescription: " -ForegroundColor Red
}

# 5. Test reports
Write-Host "
5. Testing report endpoints..." -ForegroundColor Yellow

try {
    # Inventory value report
     = Invoke-RestMethod -Uri "/reports/inventory-value" -Method Get
    Write-Host " Inventory Value Report:" -ForegroundColor Green
    Write-Host "   Total items: " -ForegroundColor Gray
    Write-Host "   Total value: Green(.cost_value)" -ForegroundColor Gray
    
    # Low stock report
     = Invoke-RestMethod -Uri "/inventory/low-stock" -Method Get
    Write-Host " Low Stock Report:" -ForegroundColor Green
    Write-Host "   Low stock items: " -ForegroundColor Gray
    Write-Host "   Expired items: " -ForegroundColor Gray
    
} catch {
    Write-Host " Failed to get reports: " -ForegroundColor Red
}

# 6. Test drug interaction check
Write-Host "
6. Testing drug interaction check..." -ForegroundColor Yellow

if () {
    try {
         = Invoke-RestMethod -Uri "/drug-interactions/check?drug_ids=&drug_ids=" -Method Get
        Write-Host " Drug interaction check completed" -ForegroundColor Green
        Write-Host "   Interactions found: " -ForegroundColor Gray
    } catch {
        Write-Host " Failed to check interactions: " -ForegroundColor Red
    }
}

# 7. List all endpoints
Write-Host "
7. Testing all pharmacy endpoints..." -ForegroundColor Yellow

 = @(
    "/drugs",
    "/inventory",
    "/inventory/low-stock",
    "/suppliers",
    "/prescriptions",
    "/purchase-orders"
)

foreach ( in ) {
    Write-Host "   Testing ..." -NoNewline
    try {
         = Invoke-RestMethod -Uri  -Method Get -TimeoutSec 2
        Write-Host " " -ForegroundColor Green
    } catch {
        Write-Host " " -ForegroundColor Red
    }
}

Write-Host "
 Pharmacy Module Testing Complete!" -ForegroundColor Green
Write-Host "
 Pharmacy API Documentation: http://localhost:8000/docs#/pharmacy" -ForegroundColor Cyan
