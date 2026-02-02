from rest_framework import serializers
from django.core.validators import EmailValidator
from datetime import date
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name',
            'email', 'department', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_employee_id(self, value):
        if self.instance and self.instance.employee_id == value:
            return value
        if Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError(
                "Employee with this ID already exists."
            )
        return value

    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            return value
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Employee with this email already exists."
            )
        EmailValidator()(value)
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.full_name', read_only=True
    )
    employee_code = serializers.CharField(
        source='employee.employee_id', read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name',
            'employee_code', 'date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'employee_name', 'employee_code'
        ]

    def validate(self, data):
        if data['date'] > date.today():
            raise serializers.ValidationError(
                {"date": "Attendance date cannot be in the future"}
            )

        if Attendance.objects.filter(
            employee=data['employee'],
            date=data['date']
        ).exists():
            raise serializers.ValidationError(
                "Attendance already marked for this employee on this date"
            )
        return data

    def validate_status(self, value):
        if value not in ['present', 'absent']:
            raise serializers.ValidationError(
                "Status must be 'present' or 'absent'"
            )
        return value
