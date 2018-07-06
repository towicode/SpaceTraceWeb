#!/bin/sh
# This script is used to launch celery beat from the systemd/system V services.
${CELERY_BIN} beat -A $CELERY_APP --pidfile=${CELERYBEAT_PID_FILE} ${CELERYBEAT_OPTS}