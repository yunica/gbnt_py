from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models.functions import ExtractQuarter
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Case, When, IntegerField, F, Q
from . import models


class IndexView(TemplateView):
    template_name = "index.html"


# api
# crud


# query section 2
class EmployeeByDepartJobQuarter(ViewSet):
    def list(self, request):
        year = int(request.GET.get("year", 2021))

        """
        SELECT 
            d.department,
            j.jobs,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 END) AS Q1,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 END) AS Q2,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 END) AS Q3,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 END) AS Q4
        FROM 
            public.hired_employees he
        JOIN 
            public.departments d ON he.department_id = d.id
        JOIN 
            public.jobs j ON he.job_id = j.id
        WHERE 
            EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY 
            d.department, j.jobs
        ORDER BY 
            d.department, j.jobs;
        """
        # get quartes
        hired_employees_ = (
            models.HiredEmployees.objects.filter(
                datetime__year=year
            ).values("department__department", "job__jobs")
            .annotate(
                # rename fields
                departments=F("department__department"),
                jobs=F("job__jobs"),
                Q1=Count('id', filter=Q(datetime__quarter=1)),
                Q2=Count('id', filter=Q(datetime__quarter=2)),
                Q3=Count('id', filter=Q(datetime__quarter=3)),
                Q4=Count('id', filter=Q(datetime__quarter=4))
            )
            .order_by('departments', 'jobs')
        )
        return Response(list(hired_employees_), status=status.HTTP_200_OK)


class EmployeByHiredByDepartment(ViewSet):
    def list(self, request):
        year = int(request.GET.get("year", 2021))

        total_hired_by_department = (
            models.HiredEmployees.objects.filter(
                datetime__year=year
            )
            .values("department")
            .annotate(hired=Count("id"))
        )
        # calculate
        total_hired_list = [item["hired"] for item in total_hired_by_department]
        average_hired = (
            sum(total_hired_list) / len(total_hired_list) if total_hired_list else 0
        )
        # query filter
        departments_average = (
            models.HiredEmployees.objects.filter(
                datetime__year=year
            )
            .values("department__id", "department__department")
            .annotate(hired=Count("id"))
            .filter(hired__gt=average_hired)
            .order_by("-hired")
        )
        return Response(list(departments_average), status=status.HTTP_200_OK)
