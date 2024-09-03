from rest_framework import serializers
from .models import *
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'shift', 'location', 'office_location', \
                  'frm']


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(write_only=True)    
    new_password = serializers.CharField(write_only=True)
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id' ,'email', 'first_name', 'last_name', 'is_active', 'is_admin')
        
        
class DisableUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
class BulkUploadSerializer(serializers.Serializer):
    file = serializers.CharField()  


class SubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubActivity
        fields = '__all__'  
    

class ActivitySerializer(serializers.ModelSerializer):
    projects = SubActivitySerializer(many=True, read_only=True)
    class Meta:
        model = Activity
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    projects = ActivitySerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
        

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class OfficeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = '__all__'


class RuleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        

class TimeSheetDetailsSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client_name.name')
    project_name = serializers.CharField(source='project_name.name')
    activity_name = serializers.CharField(source='activity_name.name')

    class Meta:
        model = TimeSheetDetails
        fields = '__all__'
        
    # def get_client_name(self, obj):
    #     return obj.client.name

    # def get_project_name(self, obj):
    #     return obj.project.name

    # def get_activity_name(self, obj):
    #     return obj.activity.name
        
 
class AddTaskSerializer(serializers.Serializer):
    activity_id = serializers.IntegerField()
    assigned_by = serializers.CharField(max_length=255)
    employee_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=255)
    project_id = serializers.IntegerField()
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
        
        
class MissedTaskSerializer(serializers.Serializer):
    activity_id = serializers.IntegerField()
    assigned_by = serializers.CharField(max_length=255)
    employee_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=255)
    project_id = serializers.IntegerField()
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    comments = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Calculate the difference between start_time and end_time
        time_difference = timedelta(hours=end_time.hour, minutes=end_time.minute) - timedelta(hours=start_time.hour, minutes=start_time.minute)

        # Check if the difference is more than one hour
        if time_difference > timedelta(hours=1) or time_difference < timedelta(hours=0):
            raise serializers.ValidationError("The difference between start_time and end_time cannot be more than one hour start_time can not be after end time.")

        return data
        
        
class EmailTimeSheetsSerializer(serializers.Serializer):
    employee = serializers.BooleanField(default=False)
    frm = serializers.BooleanField(default=False)
    management = serializers.BooleanField(default=False)
    
    
class EmployeeRecordSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print(attrs)
        attrs['username'] = attrs.get('email')
        # Call the original validate method to get the token
        data = super().validate(attrs)

        # Fetch the user using the email in attrs
        email = self.user.email
        user = CustomUser.objects.get(email=email)
        frm = FRM.objects.get(id=user.frm.id)

        # Add custom fields to the response
        data['userid'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        data['frm_name'] = frm.name

        return data
    
    
class EditTimeSheetRecordsSerializer(serializers.Serializer):
    comments = serializers.CharField(required=True)
    timesheet_id = serializers.IntegerField(required=True)
    
    
class ProjectsToClientsSerializer(serializers.Serializer):
    client_name = serializers.CharField(required=True)
    

class EODSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True)
    

class PauseResumeTaskSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    timesheet_id = serializers.IntegerField(required=True)
    
    
class ClientNameSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'projects']  # Include client ID and projects

    def get_projects(self, obj):
        projects = obj.projects.filter(is_active=True)
        return [
            {
                'project_id': project.id,
                'project_name': project.name
            }
            for project in projects
        ]
