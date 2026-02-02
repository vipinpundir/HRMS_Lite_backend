de# HRMS Backend API

Django REST API backend for HRMS Lite application.

## Features
- Employee Management (CRUD operations)
- Attendance Tracking
- RESTful API endpoints
- PostgreSQL database
- CORS enabled

## API Endpoints

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee

### Attendance
- `GET /api/attendance/` - List all attendance records
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/employee/{employee_id}/` - Get attendance by employee

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd hrms-backend