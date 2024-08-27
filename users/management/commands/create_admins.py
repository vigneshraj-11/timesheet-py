from django.core.management.base import BaseCommand
from users.models import CustomUser, Location, Shift, OfficeLocation, FRM
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import CustomTokenObtainPairSerializer

class Command(BaseCommand):
    help = "Create two admin users and generate tokens for them."

    def handle(self, *args, **kwargs):
        admins = [
            {"email": "vn@ctdtechs.com", 
             "first_name": "Vignesh", 
             "last_name": "Raj", 
             "shift": 1,
             "location": 1,
             "office_location": 1,
             "frm": 1
             },
            
            {"email": "tm@ctdtechs.com", 
             "first_name": "Tamilselvan", 
             "last_name": "Mani",
             "shift": 1,
             "location": 1,
             "office_location": 1,
             "frm": 1
             },
        ]

        for admin_data in admins:
            try:
                # Ensure related objects exist
                location = Location.objects.get(id=admin_data['location'])
                shift = Shift.objects.get(id=admin_data['shift'])
                office_location = OfficeLocation.objects.get(id=admin_data['office_location'])
                frm = FRM.objects.get(id=admin_data['frm'])
                
                user, created = CustomUser.objects.get_or_create(
                    email=admin_data['email'],
                    defaults={
                        'first_name': admin_data['first_name'],
                        'last_name': admin_data['last_name'],
                        'location': location,
                        'shift': shift,
                        'office_location': office_location,
                        'frm': frm,
                        'is_admin': True,
                    }
                )

                if created:
                    user.set_password(f"{admin_data['first_name'].capitalize()}@123")
                    user.save()

                serializer = CustomTokenObtainPairSerializer(data={'email': admin_data['email'], 'password': f"{admin_data['first_name'].capitalize()}@123"})
                serializer.is_valid(raise_exception=True)
                tokens = serializer.validated_data

                # Print the response
                self.stdout.write(self.style.SUCCESS(
                    f"Admin user created: {user.email}\n"
                    f"Response:\n{{\n"
                    f"    'refresh': '{tokens['refresh']}',\n"
                    f"    'access': '{tokens['access']}',\n"
                    f"    'userid': {user.id},\n"
                    f"    'first_name': '{user.first_name}',\n"
                    f"    'last_name': '{user.last_name}',\n"
                    f"    'email': '{user.email}'\n"
                    f"}}\n"
                ))

            except Location.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Location with ID {admin_data['location']} does not exist."))
            except Shift.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Shift with ID {admin_data['shift']} does not exist."))
            except OfficeLocation.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"OfficeLocation with ID {admin_data['office_location']} does not exist."))
            except FRM.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"FRM with ID {admin_data['frm']} does not exist."))
