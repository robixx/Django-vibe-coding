# This is an auto-generated Django model module.
from django.db import models


class Employeedetails(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    slno = models.IntegerField(db_column='SLNo', blank=True, null=True)
    employeeid = models.CharField(db_column='EmployeeID', max_length=50, blank=True, null=True)
    nameemployee = models.CharField(db_column='NameEmployee', max_length=150, blank=True, null=True)
    designation = models.CharField(db_column='Designation', max_length=100, blank=True, null=True)
    presentaddress = models.CharField(db_column='PresentAddress', max_length=250, blank=True, null=True)
    permanentaddress = models.CharField(db_column='PermanentAddress', max_length=250, blank=True, null=True)
    mobilenumber = models.CharField(db_column='MobileNumber', max_length=100, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=100, blank=True, null=True)
    medicalinformation = models.CharField(db_column='MedicalInformation', max_length=250, blank=True, null=True)
    localguardianname = models.CharField(db_column='LocalGuardianName', max_length=150, blank=True, null=True)
    localguardiannumber = models.CharField(db_column='LocalGuardianNumber', max_length=215, blank=True, null=True)
    localguardianaddress = models.CharField(db_column='LocalGuardianAddress', max_length=250, blank=True, null=True)
    relationshipwithguardian = models.CharField(db_column='RelationshipwithGuardian', max_length=100, blank=True, null=True)
    localguardianemail = models.CharField(db_column='LocalGuardianEmail', max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EmployeeDetails'


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)
    isactive = models.IntegerField(db_column='IsActive', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Role(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    role_name = models.CharField(db_column='RoleName', max_length=100, blank=True, null=True)
    role_description = models.TextField(db_column='RoleDescription', blank=True, null=True)
    is_active = models.IntegerField(db_column='IsActive', default=1)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='UpdatedAt', auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Role'


class Page(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    page_name = models.CharField(db_column='PageName', max_length=100, blank=True, null=True)
    page_url = models.CharField(db_column='PageURL', max_length=200, blank=True, null=True)
    page_icon = models.CharField(db_column='PageIcon', max_length=50, blank=True, null=True)
    is_active = models.IntegerField(db_column='IsActive', default=1)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Page'


class RolePermission(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='RoleId', related_name='permissions')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, db_column='PageId', related_name='role_permissions')
    can_view = models.IntegerField(db_column='CanView', default=0)
    can_add = models.IntegerField(db_column='CanAdd', default=0)
    can_edit = models.IntegerField(db_column='CanEdit', default=0)
    can_delete = models.IntegerField(db_column='CanDelete', default=0)
    is_active = models.IntegerField(db_column='IsActive', default=1)
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RolePermission'
        unique_together = ('role', 'page')
