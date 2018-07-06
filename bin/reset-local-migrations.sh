#!/bin/bash
# bin/reset-local-migrations.sh
# Send complaints to Hagan Franks <franks@email.arizona.edu>

# bail out if error
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/django-bash-library

_CWD=`pwd`
# migration_order=(telephony outreach ehipcore coaching bulksms webquit evaluation ashline_core)

echo "About to delete all migration files in the following folders:"
LOCAL_MIGRATIONS="${DJANGO_PROJECT_ROOT}/apps/**/local_migrations"
MIGRATIONS="${DJANGO_PROJECT_ROOT}/apps/**/migrations"
set +e
# Print out our files to remove
cntr=`find ${LOCAL_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' -print 2> /dev/null | wc -l`
if [ $cntr -eq 0 ]; then
    echo "No preexisting local_migrations!"
else
    echo "Found the following preexisting local migrations for project ${PROJECT_NAME}"
    find ${LOCAL_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' -print 2> /dev/null
    cntr=`find ${LOCAL_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' 2> /dev/null | wc -l`
    if [[ $cntr -ne 0 ]]; then
        echo -e "\nDetected migrations that are divergent from main line! You must migrate to a state before these were applied."
        find ${LOCAL_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' 2> /dev/null | sed -E -e 's/^.*\/apps\/([_[:alnum:]]+)\/[_[:alnum:]]+\/([[:digit:]]{4}).*/\1 \2/'
        if ask "Do you want to abort wiping local_migrations directory?" Y; then
            echo "Aborted $0 operation!"
            exit 0
        fi
    fi
fi
# build up list to act on (for removing)
OLD_LOCAL_MIGRATIONS=$(find ${LOCAL_MIGRATIONS} \( -type f -o -type l \) \( -name '*.py' -o -name '*.pyc' \) -not -name '__init__.py' -print 2> /dev/null)
set -e
if ask "Are you sure you want to delete all LOCAL migration files?" N; then
    # find ${LOCAL_MIGRATIONS} -type f \( -name '*.py' -o -name '*.pyc' \) -not -name '__init__.py' -print0 | xargs -0 rm
    for SRC in $OLD_LOCAL_MIGRATIONS; do
        rm $SRC
    done
    for SRC in $(find ${MIGRATIONS} -type f -name '*.py' -not -name '__init__.py'); do
        DEST=$(echo ${SRC} | sed -e 's/migrations/local_migrations/g')
        if [[ ! -d "$(dirname $DEST)" ]]; then
            mkdir $(dirname $DEST)
            touch $(dirname $DEST)/__init__.py
        fi
        ln -s $SRC $(dirname $DEST)/.
    done
else
    echo "Aborted!"
    exit 0
fi
echo -e "\n\n"
echo "It is very VERY important that you make sure your local.py settings file contains"
echo "MIGRATION_MODULES setting override. If you fail to do this, you will likely"
echo "overwrite existing model migrations which are used in produciton."
echo "This WILL cause you to be murdered."
if ask "Do you want to run local migrations to regenerate files?" Y; then
    cd ${DJANGO_PROJECT_ROOT}
    echo "Running local migrations..."
    #python manage.py makemigrations ehipcore telephony outreach ashline_core coaching bulksms webquit evaluation
    python manage.py makemigrations
    cd $_CWD
    echo -e "\n\nTo manually reset your database: 'dropdb <databasename>; createdb -U <databaseuser> -E UTF8 <databasename>; python manage.py migrate"
fi