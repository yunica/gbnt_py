from django.conf import settings
from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(
    "employees_by_departments_jobs_quarter",
    views.EmployeByDepartJobQuarter,
    basename="employees_by_departments_jobs_quarter",
)
