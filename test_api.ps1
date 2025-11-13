# Test Script for SurgeonTrainer API
Write-Host "=== Testing SurgeonTrainer API ===" -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Cyan
$healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method Get
Write-Host "Status: $($healthResponse.status)" -ForegroundColor Yellow
Write-Host "Message: $($healthResponse.message)" -ForegroundColor Yellow

# Test 2: Create a Patient
Write-Host "`n2. Creating Test Patient..." -ForegroundColor Cyan
$patientData = @{
    mrn = "TEST$(Get-Random -Minimum 10000 -Maximum 99999)"
    first_name = "John"
    last_name = "Doe"
    date_of_birth = "1980-01-15"
    sex = "M"
    email = "john.doe@example.com"
    phone = "555-0123"
    address = "123 Main St"
    city = "Boston"
    state = "MA"
    zip_code = "02101"
} | ConvertTo-Json

$createResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients" -Method Post -Body $patientData -ContentType "application/json"
Write-Host "Created Patient ID: $($createResponse.id)" -ForegroundColor Yellow
Write-Host "MRN: $($createResponse.mrn)" -ForegroundColor Yellow
Write-Host "Name: $($createResponse.first_name) $($createResponse.last_name)" -ForegroundColor Yellow

$patientId = $createResponse.id

# Test 3: Get Patient
Write-Host "`n3. Retrieving Patient..." -ForegroundColor Cyan
$getResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients/$patientId" -Method Get
Write-Host "Retrieved: $($getResponse.first_name) $($getResponse.last_name)" -ForegroundColor Yellow

# Test 4: List Patients
Write-Host "`n4. Listing All Patients..." -ForegroundColor Cyan
$listResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients?page=1&page_size=10" -Method Get
Write-Host "Total Patients: $($listResponse.total)" -ForegroundColor Yellow
Write-Host "Patients on Page 1: $($listResponse.patients.Count)" -ForegroundColor Yellow

# Test 5: Update Patient
Write-Host "`n5. Updating Patient..." -ForegroundColor Cyan
$updateData = @{
    email = "john.doe.updated@example.com"
    phone = "555-9999"
} | ConvertTo-Json

$updateResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients/$patientId" -Method Patch -Body $updateData -ContentType "application/json"
Write-Host "Updated Email: $($updateResponse.email)" -ForegroundColor Yellow
Write-Host "Updated Phone: $($updateResponse.phone)" -ForegroundColor Yellow

# Test 6: Get Patient Stats
Write-Host "`n6. Getting Patient Statistics..." -ForegroundColor Cyan
$statsResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/patients/stats/overview" -Method Get
Write-Host "Total Active: $($statsResponse.total_active)" -ForegroundColor Yellow
Write-Host "Total Inactive: $($statsResponse.total_inactive)" -ForegroundColor Yellow
Write-Host "Total Discharged: $($statsResponse.total_discharged)" -ForegroundColor Yellow

Write-Host "`n=== All Tests Passed! ===" -ForegroundColor Green
Write-Host "`nAPI Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Alternative Docs: http://localhost:8000/redoc" -ForegroundColor Cyan
