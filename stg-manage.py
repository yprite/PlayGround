import getpass
import os
import sys

USER = 'www-data'

if __name__ == "__main__":
    if getpass.getuser() == USER:
        print ("Error: In Staging Mode")
        sys.exit(1)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'playground.settings_staging'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
