# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Employee(models.Model):
    Gender_Choices = (
        ('0', 'Male'),
        ('1', 'Female'),

    )
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(db_column='FIRST_NAME', max_length=60)  # Field name made lowercase.
    last_name = models.CharField(db_column='LAST_NAME', max_length=60)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', unique=True, max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20)  # Field name made lowercase.
    gender = models.IntegerField(db_column='GENDER', choices=Gender_Choices)  # Field name made lowercase.
    date_of_birth = models.DateTimeField(db_column='DATE_OF_BIRTH', blank=True, null=True)  # Field name made lowercase.
    mobile_number = models.CharField(db_column='MOBILE_NUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    address_1 = models.CharField(db_column='ADDRESS_1', max_length=100)  # Field name made lowercase.
    address_2 = models.CharField(db_column='ADDRESS_2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, db_column='ROLE_ID')  # Field name made lowercase.
    project = models.ForeignKey('Project', on_delete=models.DO_NOTHING, db_column='PROJECT_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Project(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=60)  # Field name made lowercase.
    project_details = models.TextField(db_column='PROJECT_DETAILS', blank=True, null=True)  # Field name made lowercase.
    project_start_date = models.DateTimeField(db_column='PROJECT_START_DATE')  # Field name made lowercase.
    project_expected_end_date = models.DateTimeField(db_column='PROJECT_EXPECTED_END_DATE', blank=True, null=True)  # Field name made lowercase.
    progress_status = models.ForeignKey('ProjectProgressStatus', on_delete=models.DO_NOTHING, db_column='PROGRESS_STATUS_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project'


class ProjectProgressStatus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=45)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project_progress_status'


class Role(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    role_name = models.CharField(db_column='ROLE_NAME', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role'
