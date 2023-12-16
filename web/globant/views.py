from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models.functions import ExtractQuarter
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Case, When, IntegerField, F
from . import models


class IndexView(TemplateView):
    template_name = "index.html"


# api
# crud

# query section 2
class EmployeeByDepartJobQuarter(ViewSet):
    def list(self, request):
        year = int(request.GET.get("year", 2021))
        # get quartes
        hired_employees_ = models.HiredEmployees.objects.filter(
            datetime__year=year,
            department__isnull=False
        ).annotate(
            quarter=ExtractQuarter('datetime'),
            # rename fields
            departments=F('department__department'),
            jobs=F('job__jobs')
        ).values(
            'departments', 'jobs', 'quarter'
        ).annotate(
            count=Count('id')
        )

        # count by quarter
        quarter_counts = hired_employees_.annotate(
            Q1=Count(Case(When(quarter=1, then=1), output_field=IntegerField())),
            Q2=Count(Case(When(quarter=2, then=1), output_field=IntegerField())),
            Q3=Count(Case(When(quarter=3, then=1), output_field=IntegerField())),
            Q4=Count(Case(When(quarter=4, then=1), output_field=IntegerField()))
        ).values(
            'departments', 'jobs', 'Q1', 'Q2', 'Q3', 'Q4'
        ).order_by(
            'departments', 'jobs',
        )
        return Response(list(quarter_counts), status=status.HTTP_200_OK)


class EmployeByHiredByDepartment(ViewSet):
    def list(self, request):
        year = int(request.GET.get("year", 2021))
        total_hired_by_department = models.HiredEmployees.objects.filter(
            datetime__year=year,
            department__isnull=False
        ).values(
            'department'
        ).annotate(
            hired=Count('id')
        )
        # calculate
        total_hired_list = [item['hired'] for item in total_hired_by_department]
        average_hired = sum(total_hired_list) / len(total_hired_list) if total_hired_list else 0
        # query filter
        departments_average = models.HiredEmployees.objects.filter(
            datetime__year=2021,
            department__isnull=False
        ).values(
            'department__id', 'department__department'
        ).annotate(
            hired=Count('id')
        ).filter(
            hired__gt=average_hired
        ).order_by('-hired')
        return Response(list(departments_average), status=status.HTTP_200_OK)
