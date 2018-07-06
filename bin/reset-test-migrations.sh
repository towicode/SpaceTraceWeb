#!/bin/bash
# bin/reset-local-migrations.sh
# Send complaints to Hagan Franks <franks@email.arizona.edu>

# bail out if error
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/django-bash-library

_CWD=`pwd`
# migration_order=(telephony outreach ehipcore coaching bulksms webquit evaluation ashline_core)

echo "About to delete all *TEST* migration files in the following folders:"
TEST_MIGRATIONS="${DJANGO_PROJECT_ROOT}/apps/**/migrations_clean"
MIGRATIONS="${DJANGO_PROJECT_ROOT}/apps/**/migrations"
LOCAL_SETTINGS_FILE="${DJANGO_PROJECT_ROOT}/settings/local.py"
set +e
# Print out our files to remove
cntr=`find ${TEST_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' -print 2> /dev/null | grep -v test_init | wc -l`
echo "CNTR: ${cntr}"
if [ $cntr -eq 0 ]; then
    echo "No preexisting TEST_MIGRATIONS!"
else
    echo "Found the following preexisting test migrations for project ${PROJECT_NAME}"
    find ${TEST_MIGRATIONS} -type f -name '*.py' -not -name '__init__.py' 2> /dev/null | grep -v test_init | sed -E -e 's/^.*\/apps\/([_[:alnum:]]+)\/[_[:alnum:]]+\/([[:digit:]]{4}).*/\1 \2/'
fi
# build up list to act on (for removing)
OLD_TEST_MIGRATIONS=$(find ${TEST_MIGRATIONS} \( -type f -o -type l \) \( -name '*.py' -o -name '*.pyc' \) -not -name '__init__.py' -print 2> /dev/null | grep -v test_init)
set -e
if ask "Are you sure you want to delete all LOCAL migration files?" N; then
    # find ${TEST_MIGRATIONS} -type f \( -name '*.py' -o -name '*.pyc' \) -not -name '__init__.py' -print0 | xargs -0 rm
    for SRC in $OLD_TEST_MIGRATIONS; do
        rm $SRC
    done
    for SRC in $(find ${MIGRATIONS} -type f -name '*.py' -not -name '__init__.py'); do
        DEST=$(echo ${SRC} | sed -e 's/migrations/migrations_clean/g')
        if [[ ! -d "$(dirname $DEST)" ]]; then
            mkdir $(dirname $DEST)
            touch $(dirname $DEST)/__init__.py
        fi
    done
else
    echo "Aborted!"
    exit 0
fi

# Need to temporarily enable the "MIGRATION_MODULES" as TEST_MIGRATION_MODULES
if ask "Do you want to generate test migrations (/apps/**/migrations_clean)" N; then
    if [[ -f "${LOCAL_SETTINGS_FILE}" ]]; then
        echo "Found local settings file: ${LOCAL_SETTINGS_FILE}!"
        if grep -xqFe "# MIGRATION_MODULES = TEST_MIGRATION_MODULES #AUTOSCRIPT#" ${LOCAL_SETTINGS_FILE}; then
            sed -i '/^#\s*MIGRATION_MODULES = TEST_MIGRATION_MODULES #AUTOSCRIPT#/s/^#\s*//g' ${LOCAL_SETTINGS_FILE}
            cd ${DJANGO_PROJECT_ROOT}
            python manage.py makemigrations
            cd $_CWD
            sed -i '/^\s*MIGRATION_MODULES = TEST_MIGRATION_MODULES #AUTOSCRIPT#/s/^/# /g' ${LOCAL_SETTINGS_FILE}
        else
            echo -e "\n\nMIGRATION_MODULES = TEST_MIGRATION_MODULES #AUTOSCRIPT#" >> ${LOCAL_SETTINGS_FILE}
            cd ${DJANGO_PROJECT_ROOT}
            python manage.py makemigrations
            cd $_CWD
            sed -i '/^\s*MIGRATION_MODULES = TEST_MIGRATION_MODULES #AUTOSCRIPT#/s/^/# /g' ${LOCAL_SETTINGS_FILE}
        fi
    fi
fi
