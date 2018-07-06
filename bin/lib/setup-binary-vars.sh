#!/usr/bin/env sh
# Hagan Franks 2018-06-13 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu

#temporarily disable exit on error -> so we can print error messages...
if echo "$-" | egrep -q 'e'; then
  ENABLE_ERROR_HANDLER=true
  set +e
else
  ENABLE_ERROR_HANDLER=false
fi

check_missing_bin() {
  if [ ! -f "$1" ]; then
    echo "ERROR: Missing $2"
    echo $3
    return 1
  fi
}

warning_missing_bin() {
  if [ ! -f "$1" ]; then
    echo "WARNING: Missing $2"
    echo $3
    return 1
  fi
}

## os detection
if [ "$OSTYPE" = "linux-gnu" ]; then
  OSCLASS='linux'
  # Linux version of whereis has a -b option
  WHEREIS='whereis -b $BINARY | cut -d" " -f2'

  # Setup readlink for linux
  BINARY='readlink'
  READLINK=$(eval $WHEREIS)
  check_missing_bin "${READLINK}" "${BINARY}" "Possible fix: apt-get install coreutils" || return 1

  BINARY='sed'
  SED=$(eval $WHEREIS)
  check_missing_bin "${SED}" "${BINARY}" "Possible fix: apt-get install sed" || return 1

elif echo -n "$OSTYPE" | egrep -q '^darwin.*'; then
  OSCLASS='osx'
  WHEREIS='which -a $BINARY | grep bin | head -n1'

  BINARY='gsed'
  SED=$(eval $WHEREIS)
  check_missing_bin "${SED}" "${BINARY}" "Missing ${SED}, Possible fix: brew install gnu-sed"

  # Setup readlink / greadlink for osx
  BINARY='greadlink'
  READLINK=$(eval $WHEREIS)
  check_missing_bin "${READLINK}" "${BINARY}" "Possible fix: brew install coreutils" || return 1
elif [ "$OSTYPE" = "cygwin" ]; then
  OSCLASS='cygwin'
  echo "Unsupported os (cygwin)"
elif [ "$OSTYPE" = "msys" ]; then
  OSCLASS='msys'
  echo "Unsupported os (msys)"
elif [ "$OSTYPE" = "win32" ]; then
  OSCLASS='windows'
  echo "Unsupported os (win32)"
  return 1
elif [ "$OSTYPE" = "freebsd"* ]; then
  OSCLASS='freebsd'
  WHEREIS='whereis $BINARY'

  # Setup readlink for FreeBSD
  READLINK=$(eval $WHEREIS)
  check_missing_bin "${READLINK}" "${BINARY}" "Possible fix: pkg install coreutils" || return 1
else
  echo "Unknown OS: $OSTYPE"
  return 1
fi

BINARY='realpath'
REALPATH=$(eval $WHEREIS)
check_missing_bin "${REALPATH}" "${BINARY}" "Possible fix: apt-get install realpath / brew install realpath" || return 1

BINARY='basename'
BASENAME=$(eval $WHEREIS)
check_missing_bin "${BASENAME}" "${BINARY}" "" || return 1

BINARY='dirname'
DIRNAME=$(eval $WHEREIS)
check_missing_bin "${DIRNAME}" "${BINARY}" "" || return 1

BINARY='python'
PYTHON=$(eval $WHEREIS)
check_missing_bin "${PYTHON}" "${BINARY}" "" || return 1

BINARY='rabbitmqctl'
RABBITMQCTL=$(eval $WHEREIS)
warning_missing_bin "${RABBITMQCTL}" "${BINARY}" "Fix: sudo apt-get install rabbitmq-server / brew install rabbitmq"

BINARY='createdb'
CREATEDB=$(eval $WHEREIS)
check_missing_bin "${CREATEDB}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='dropdb'
DROPDB=$(eval $WHEREIS)
check_missing_bin "${DROPDB}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='pg_restore'
PGRESTORE=$(eval $WHEREIS)
check_missing_bin "${PGRESTORE}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='pg_dump'
PGDUMP=$(eval $WHEREIS)
check_missing_bin "${PGDUMP}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='psql'
PSQL=$(eval $WHEREIS)
check_missing_bin "${PSQL}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='zcat'
ZCAT=$(eval $WHEREIS)
check_missing_bin "${ZCAT}" "${BINARY}" "" || return 1

BINARY='gunzip'
GUNZIP=$(eval $WHEREIS)
check_missing_bin "${GUNZIP}" "${BINARY}" "Possible fix: apt-get/brew/pkg install gunzip" || return 1

BINARY='vacuumdb'
VACUUMDB=$(eval $WHEREIS)
check_missing_bin "${VACUUMDB}" "${BINARY}" "Possible fix: apt-get/brew/pkg install postgresql-server" || return 1

BINARY='pip'
PIP_BIN=$(eval $WHEREIS)
check_missing_bin "${PIP_BIN}" "${BINARY}" "Possible fix: brew install python / apt-get install python-pip" || return 1

if [[ -z ${_SKIP_VIRTUALENVWRAPPER_CHECK+x} ]]; then
  BINARY='virtualenvwrapper.sh'
  VIRTUALENVWRAPPER_SCRIPT=$(eval $WHEREIS)
  if [ ! -f "${VIRTUALENVWRAPPER_SCRIPT}" ]; then
    # check if this exists with pyenv
    VIRTUALENVWRAPPER_SCRIPT=$(pyenv which $BINARY)
    if [ ! -f "${VIRTUALENVWRAPPER_SCRIPT}" ]; then
      echo "ERROR: Missing ${BINARY}"
      echo "Possible fix: pip install virtualenvwrapper"
      return 1
    fi
  fi
fi

# Re-enable error handling
if $ENABLE_ERROR_HANDLER; then
  set -e
fi

return 0


check_missing_bin() {
  if [ ! -f "$1" ]; then
    echo "ERROR: Missing $2"
    echo $3
    return 1
  fi
}