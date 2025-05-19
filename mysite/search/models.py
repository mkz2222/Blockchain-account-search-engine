from django.db import models

# Create your models here.

class Testdj(models.Model):
    name = models.CharField(unique=True, max_length=20)
    date_created = models.DateField()
    block = models.IntegerField()
    creator = models.CharField(max_length=20)
    time_created = models.DateTimeField(null=True)
    group1 = models.CharField(max_length=10, default=None, null=True)
    group2 = models.CharField(max_length=10, default=None, null=True)
    group3 = models.CharField(max_length=10, default=None, null=True)
    group4 = models.CharField(max_length=10, default=None, null=True)
    group5 = models.CharField(max_length=10, default=None, null=True)
    group6 = models.CharField(max_length=10, default=None, null=True)
    time_logged = models.DateTimeField(null=True)

    class Meta:
        app_label = 'search'



# class Testdj2(models.Model):
#     name = models.CharField(unique=True, max_length=20)
#     date_created = models.DateField()
#     block = models.IntegerField()
#     creator = models.CharField(max_length=20)
#     time_created = models.DateTimeField(blank=True, null=True)
#     group1 = models.CharField(max_length=10)
#     group2 = models.CharField(max_length=10)
#     group3 = models.CharField(max_length=10)
#     group4 = models.CharField(max_length=10)
#     group5 = models.CharField(max_length=10)

#     class Meta:
#         app_label = 'search'
#         managed = False
#         db_table = 'test11'



