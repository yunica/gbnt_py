from django.conf import settings
from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(
    "employees_by_departments_jobs_quarter",
    views.EmployeeByDepartJobQuarter,
    basename="employees_by_departments_jobs_quarter",
)
router.register(
    "employees_hired_by_department",
    views.EmployeByHiredByDepartment,
    basename="employees_hired_by_department",
)
