from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
    
class FRM(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
    
class OfficeLocation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    
    
class Rule(models.Model):
    rule = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.rule
    
    
class Shift(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=30, null=True, default=True)
    contact_person = models.CharField(max_length=30, null=True, default=True)
    contact_person_email = models.EmailField(unique=True)
    contact_email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, null=True)


    def __str__(self):
        return self.name
    

class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, default=None)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shifts')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='locations')
    office_location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, related_name='officelocations')
    reporting_to = models.CharField(max_length=30, null=True, default=None)
    frm = models.ForeignKey(FRM, on_delete=models.CASCADE, related_name='frms')
    trm = models.CharField(max_length=30, null=True, default=None)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=28, null=True, default=None)
    rules = models.CharField(max_length=30, null=True, default=None)
    client_ids = models.JSONField(models.IntegerField(), blank=True, default=list)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # def set_password(self, raw_password):
    #     self.password = raw_password

    # def check_password(self, raw_password):
    #     if raw_password == self.password:
    #         return True
    #     return False

    @property
    def is_staff(self):
        return self.is_admin


class Role(models.Model):
    role = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.role


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, null=True, default=None)
    contact_person_name = models.CharField(max_length=30, null=True, default=None)
    contact_person_email = models.EmailField(unique=True)
    cost_centre = models.CharField(max_length=30, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, null=True)


    def __str__(self):
        return self.name


class SubActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activities')
    activity_name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, null=True)


    def __str__(self):
        return self.name
    

class TimeSheetDetails(models.Model):
    timesheet_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    activity_name = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='timesheets')
    assigned_by = models.CharField(max_length=255, null=True, default=None)
    comments = models.CharField(max_length=255, null=True, default=None)
    date = models.DateField(null=True, default=None)
    custom_employee_id = models.BigIntegerField(null=True, default=None)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='timesheets')
    # employee_name = models.CharField(max_length=255, null=True, default=None)
    end_time = models.CharField(max_length=255, null=True, default=None)
    eod_status = models.CharField(max_length=255, null=True, default=None)
    # process_name = models.ForeignKey(SubActivity, on_delete=models.CASCADE, related_name='timesheets')
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='timesheets')
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timesheets')
    start_time = models.CharField(max_length=255, null=True, default=None)
    pause_reason = models.CharField(max_length=255, null=True, blank=True, default=None)  # Optional field
    approval_status = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return self.employee_name
    
    # @property
    # def employee_name(self):
    #     return self.employee.first_name
    
    # @property
    # def employee_mail(self):
    #     return self.employee.email
