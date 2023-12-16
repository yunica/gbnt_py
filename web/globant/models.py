from django.db import models


class Departments(models.Model):
    id = models.BigIntegerField(primary_key=True)
    department = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "departments"

    def __str__(self):
        return self.department


class Jobs(models.Model):
    id = models.BigIntegerField(primary_key=True)
    jobs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "jobs"

    def __str__(self):
        return self.jobs


class HiredEmployees(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey(Departments, blank=True, null=True, on_delete=models.SET_NULL)
    job = models.ForeignKey(Jobs, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        managed = False
        db_table = "hired_employees"

    def __str__(self):
        return self.name
