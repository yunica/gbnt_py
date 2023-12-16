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
class EmployeByDepartJobQuarter(ViewSet):
    def list(self, request):
        year = int(request.GET.get("year", 2021))
        # get quartes
        hired_employees_ = models.HiredEmployees.objects.filter(
            datetime__year=year
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
