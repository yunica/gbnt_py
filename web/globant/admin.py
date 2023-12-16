from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Jobs)
class JobsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HiredEmployees)
class HiredEmployeesAdmin(admin.ModelAdmin):
    raw_id_fields = ["department", "job"]
    list_display = ("id", "name", "department", "job")
    search_fields = ("name",)
