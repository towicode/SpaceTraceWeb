#!/usr/bin/env bash
# Hagan Franks <hagan.franks@gmail.com>
# Version 0.0.1
#
# To install this script edit your crontask's like so (webby user):
# $ crontab -e
# SHELL=/bin/bash
# */2 * * * * /var/django/<project>/bin/bulksms-cron-script

# If no .env found, exit!
EXIT_ON_NO_ENV=1
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

script_path=$(abs_path $0)
script_dir=$(dirname ${script_path})

## setup exit trap
SRC_SCRIPT=${script_dir}/lib/setup-exit-trap.sh
SRC_NUM=1
if test -f ${SRC_SCRIPT}; then
  . "${SRC_SCRIPT}" > /dev/null || {
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
  . "${SRC_SCRIPT}" > /dev/null || {
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
  . "${SRC_SCRIPT}" > /dev/null || {
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
  . "${SRC_SCRIPT}" > /dev/null || {
    echo "${SRC_SCRIPT} had an error! exiting.."
    exit 1
  }
else
  echo "ERROR-${SRC_NUM}: missing ${SRC_SCRIPT}!"
  exit 1
fi

# runcrons --force
source ${DJANGO_ENV_PATH}/bin/activate && ${DJANGO_ENV_PATH}/bin/python ${DJANGO_PROJECT_ROOT}/manage.py sms_blast