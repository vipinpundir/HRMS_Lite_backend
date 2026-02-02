from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer


# ================= EMPLOYEES =================

@api_view(['GET', 'POST'])
def employees(request):
    """
    GET  /api/employees/
    POST /api/employees/
    """
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, id):
    """
    GET    /api/employees/{id}/
    PUT    /api/employees/{id}/
    DELETE /api/employees/{id}/
    """
    try:
        employee = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return Response(
            {"error": "Employee not found"},
            status=404
        )

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EmployeeSerializer(
            employee, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        employee.delete()
        return Response(
            {"message": "Employee deleted successfully"},
            status=204
        )


# ================= ATTENDANCE =================

@api_view(['GET', 'POST'])
def attendance(request):
    """
    GET  /api/attendance/
    POST /api/attendance/
    """
    if request.method == 'GET':
        queryset = Attendance.objects.all()

        date = request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=parse_date(date))

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def attendance_by_employee(request, employee_id):
    """
    GET /api/attendance/employee/{employee_id}/
    """
    queryset = Attendance.objects.filter(employee__id=employee_id)

    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if start_date:
        queryset = queryset.filter(date__gte=parse_date(start_date))
    if end_date:
        queryset = queryset.filter(date__lte=parse_date(end_date))

    serializer = AttendanceSerializer(queryset, many=True)
    return Response(serializer.data)
