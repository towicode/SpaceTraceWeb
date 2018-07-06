#!/usr/bin/env python
import sys
import os
import argparse
# Ugly hack to get around not having the .env setup yet...

def parse_args(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--database-name', dest='dbname', action='store_true', help='Default Database name')
    parser.add_argument('--database-user', dest='dbuser', action='store_true', help='Default Database user')
    parser.add_argument('--database-password', dest='dbpass', action='store_true', help='Default Database password')
    parser.add_argument('--database-port', dest='dbport', action='store_true', help='Default Database port')
    return parser.parse_args(args)

def main(args):
    """
    Load our django environment and snag settings.
    """
    # Cannot guess this, need 
    project_path = os.environ.get('DJANGO_PROJECT_ROOT', None)
    if(project_path is None):
        raise Exception("Must set the environment var DJANGO_PROJECT_ROOT to the path where your django source exists!")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
    tempcwd = os.getcwd()
    os.chdir(os.path.expanduser(project_path))
    from django.conf import settings
    if(args.dbname):
        print("export DJANGO_DATABASE_NAME={}".format(settings.DATABASES['default']['NAME']))
    if(args.dbuser):
        print("export DJANGO_DATABASE_USER={}".format(settings.DATABASES['default']['USER']))
    if(args.dbpass):
        print("export DJANGO_DATABASE_PASSWORD={}".format(settings.DATABASES['default']['PASSWORD']))
    if(args.dbport):
        print("export DJANGO_DATABASE_PORT={}".format(settings.DATABASES['default']['PORT']))
    os.chdir(tempcwd)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
