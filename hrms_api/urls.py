from django.urls import path
from .views import (
    employees,
    employee_detail,
    attendance,
    attendance_by_employee
)

urlpatterns = [
    # Employees
    path('employees/', employees),
    path('employees/<int:id>/', employee_detail),

    # Attendance
    path('attendance/', attendance),
    path('attendance/employee/<int:employee_id>/', attendance_by_employee),
]
