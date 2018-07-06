#!/bin/bash

# bail out if error
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/django-bash-library

_SET_DJ_PRJ_ROOT=0
# Exit trap (CLEANUP HERE)
function finish {
  if [[ $_SET_DJ_PRJ_ROOT == 1 ]]; then
    unset DJANGO_PROJECT_ROOT
  fi
}
trap finish EXIT


if [[ "${DJANGO_PROJECT_ROOT:?non-empty}" == "non-empty" ]]; then
    export DJANGO_PROJECT_ROOT
    _SET_DJ_PRJ_ROOT=1
    echo "DJANGO_PROJECT_ROOT : $DJANGO_PROJECT_ROOT"
else
    echo "DJANGO_PROJECT_ROOT : $DJANGO_PROJECT_ROOT"
fi

# Set our DJANGO_DATABASE_NAME environment var
$($DIR/get-django-settings.py --database-name)
# Set our DJANGO_DATABASE_USER environment var
$($DIR/get-django-settings.py --database-user)
# Set our DJANGO_DATABASE_PASSWORD environment var
$($DIR/get-django-settings.py --database-password)
# Set our DJANGO_DATABASE_PORT environment var
$($DIR/get-django-settings.py --database-port)

if [[ "${DJANGO_DATABASE_NAME:?non-empty}" == "non-empty" ]]; then
    echo "Error, couldn't get DJANGO_DATABASE_NAME variable from django settings!"
    exit 1
fi

SOURCE_DATABASE_NAME='djangoashline'

# Using gpg encrypted files here!
BACKUP_FOLDER=$(realpath $DIR/../backups)
RESTORE_FILE=$(find $BACKUP_FOLDER -type f -name "*db.sql.gz.gpg" -print | sort -hr | head -1)
if [[ "${RESTORE_FILE}xxx" == "xxx" ]] || [[ ! -f "$RESTORE_FILE" ]]; then
    echo "ERROR: No file to restore from! Check your backups folder for $BACKUP_FOLDER/*-db.sql.gz.gpg file"
    exit 1
fi

echo "About to Load ashline database using '$DJANGO_DATABASE_NAME' database name."
echo "Source: $RESTORE_FILE"
if ask "Are you sure you want to restore this database?"; then
  set +e
  dropdb --username=postgres --host=localhost $DJANGO_DATABASE_NAME
  set -e
  createdb --username=postgres --host=localhost -O $DJANGO_DATABASE_USER -E UTF8 $DJANGO_DATABASE_NAME
  gpg --decrypt $RESTORE_FILE | zcat | sed -e "s/^CREATE DATABASE ${SOURCE_DATABASE_NAME}/CREATE DATABASE $DJANGO_DATABASE_NAME/g" | sed -e "s/connect ${SOURCE_DATABASE_NAME}/connect $DJANGO_DATABASE_NAME/g" | psql
  for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" $DJANGO_DATABASE_NAME` ; do psql -c "alter table \"$tbl\" owner to $DJANGO_DATABASE_USER" $DJANGO_DATABASE_NAME ; done
  for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" $DJANGO_DATABASE_NAME` ; do  psql -c "alter table \"$tbl\" owner to $DJANGO_DATABASE_USER" $DJANGO_DATABASE_NAME ; done
  for tbl in `psql -qAt -c "select table_name from information_schema.views where table_schema = 'public';" $DJANGO_DATABASE_NAME` ; do  psql -c "alter table \"$tbl\" owner to $DJANGO_DATABASE_USER" $DJANGO_DATABASE_NAME ; done
fi