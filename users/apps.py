from django.apps import AppConfig
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # def ready(self):
    #     if os.environ.get('RUN_MAIN', None) != 'true':
    #         return  # Avoids running the command twice
    #     from django.core.management import call_command
    #     call_command('create_admins')
