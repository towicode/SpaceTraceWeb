#!/bin/bash
# exec 1> >(logger -s -t $(basename $0)) 2>&1

## Load celeryd / celerybeat with rabbitmq-server debugging.
# 1) Your virtualenv needs to be generated via the /bin/mkvirtualenv script
# 2) Make sure your .env is up to date (look at .env_example) CELERY section
# 3) Install rabbitmq-server if you haven't already done so:
# $ sudo apt-get install rabbitmq-server'
# $ sudo rabbitmqctladd_user ${RABBITMQ_USER} ${RABBITMQ_PASS}
# $ sudo rabbitmqctl add_vhost ${PROJECT_NAME}-${DEPLOY_TYPE}-celery
# $ sudo rabbitmqctl set_permissions -p ${PROJECT_NAME}-${DEPLOY_TYPE}-celery ${RABBITMQ_USER} ".*" ".*" ".*"
#
# Note: below variables are sourced from the .env and should match what you create.
# RABBITMQ_USER = <your rabbitmq username>
# RABBITMQ_PASS = <your rabbitmq password>
# PROJECT_NAME-DEPLOY_TYPE-celery = <your vhost>

abs_path() {
  perl -MCwd -le '
    for (@ARGV) {
      if ($p = Cwd::abs_path $_) {
        print $p;
      } else {
        warn "abs_path: $_: $!\n";
        $ret = 1;
      }
    }
    exit $ret' "$@"
}

function show_help(){
    echo "Usage: version.sh [OPTION]"
    echo "All values are sourced 1st from git status otherwise falls back to RELEASE file.\n"
    echo "-h this help message."
    echo "-f : Force running celerybeat and workers (ignores missing rabbitmq)"
}

script_path=$(abs_path $0)
script_dir=$(dirname ${script_path})

## setup exit trap
SRC_SCRIPT=${script_dir}/lib/setup-exit-trap.sh
SRC_NUM=1
if test -f ${SRC_SCRIPT}; then
  . "${SRC_SCRIPT}" || {
    echo "${SRC_SCRIPT} had an error! exiting.."
    exit 1
  }
else
  echo "ERROR-${SRC_NUM}: missing ${SRC_SCRIPT}!"
  exit 1
fi

## setup required binaries
SRC_SCRIPT=${script_dir}/lib/setup-binary-vars.sh
SRC_NUM=2
if test -f ${SRC_SCRIPT}; then
  . "${SRC_SCRIPT}" || {
    echo "${SRC_SCRIPT} had an error! exiting.."
    exit 1
  }
else
  echo "ERROR-${SRC_NUM}: missing ${SRC_SCRIPT}!"
  exit 1
fi

## load project .env file
SRC_SCRIPT=${script_dir}/lib/load-env-vars.sh
SRC_NUM=3
if test -f ${SRC_SCRIPT}; then
  . "${SRC_SCRIPT}" || {
    echo "${SRC_SCRIPT} had an error! exiting.."
    exit 1
  }
else
  echo "ERROR-${SRC_NUM}: missing ${SRC_SCRIPT}!"
  exit 1
fi

## add ask-function
SRC_SCRIPT=${script_dir}/lib/functions.sh
SRC_NUM=4
if test -f ${SRC_SCRIPT}; then
  . "${SRC_SCRIPT}" || {
    echo "${SRC_SCRIPT} had an error! exiting.."
    exit 1
  }
else
  echo "ERROR-${SRC_NUM}: missing ${SRC_SCRIPT}!"
  exit 1
fi


if [[ -z ${CELERY_BIN+x} ]]; then
  echo "ERROR-1: The environmental variable 'CELERY_BIN' is not set in .env!"
  exit 1
fi

if [[ -z ${DJANGO_SRC_NAME+x} ]]; then
  echo "ERROR-2: The environmental variable 'DJANGO_SRC_NAME' is not set in .env!"
  exit 1
fi

if [[ -z ${DJANGO_PROJECT_ROOT+x} ]]; then
  echo "ERROR-3: The environmental variable 'DJANGO_PROJECT_ROOT' is not set in .env!"
  exit 1
fi

if [[ -z ${RABBITMQ_PASS+x} ]]; then
  echo "ERROR-4: The environmental variable 'RABBITMQ_PASS' is not set in .env!"
  echo "You must enter a password that matches what you configured with rabbitmq-server"
  exit 1
fi

FORCE_RUN=1

while getopts ":hf" opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        f)
            # (X.Y.Z-build-#COMMIT#-#HASH#)
            FORCE_RUN=0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument" >&2
            exit 1
            ;;
    esac
done

${DJANGO_PROJECT_ROOT}/manage.py check_rabbitmq
if [ $? -ne 0 ] && [ $FORCE_RUN -ne 0 ]; then
  echo "ERROR-5: Rabbitmq appears to be down or not yet configured!"
  echo "Start the rabbitmq server and configure your app user account for it!"
  exit 1
fi

${CELERY_BIN} --app=${DJANGO_SRC_NAME}.celery_app:app worker --schedule=${DJANGO_PROJECT_ROOT}/celerybeat-schedule --loglevel=INFO --beat