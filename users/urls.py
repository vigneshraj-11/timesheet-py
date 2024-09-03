from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'subactivities', SubActivityViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'shifts', ShiftViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'officelocations', OfficeLocationViewSet)
router.register(r'rules', RulesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('list/', ListUsersView.as_view(), name='list_users'),
    path('disable_user/', DisableUserView.as_view(), name='disable_user'),
    path('bulk_upload/', BulkUploadView.as_view(), name='bulk_upload'),
     path('add_task/', AddTaskAPIView.as_view(), name='add_task'),
     path('missed_task/', MissedTaskAPIView.as_view(), name='missed_task'),
     path('report_email/', EmailTimeSheetsAPIView.as_view(), name='report_email'),
     path('user/<str:email>/', UserByEmailView.as_view(), name='user_by_email'),    
     path('get_timesheet_records/', EmployeeRecordsView.as_view(), name='get_timesheet_records'), 
     path('logout/blacklist/', BlacklistTokenView.as_view(),name='blacklist'), 
     path('edittimesheetrecords/', EditTimeSheetRecordsView.as_view(),name='edittimesheetrecords'),
     path('projectstoclient/', ProjectsToClinetsView.as_view(),name='projectstoclient'),
     path('eod/', EODView.as_view(),name='eod'),
     path('pausetask/', PauseTaskView.as_view(),name='pausetask'),
     path('resumetask/', ResumeTaskView.as_view(),name='resumetask'),
]
