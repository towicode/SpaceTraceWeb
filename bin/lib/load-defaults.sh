#!/usr/bin/env sh
# Hagan Franks 2016-09-13 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu

# General
PROJECT_NAME=webquit
DJANGO_SRC_NAME=bcfsrc
DEPLOY_TYPE=dev

PROJECT_PATH=${HOME}/projects/${PROJECT_NAME}-${DEPLOY_TYPE}
DJANGO_PROJECT_ROOT=${PROJECT_PATH}/${DJANGO_SRC_NAME}
DJANGO_SETTINGS_MODULE=settings.local
PYENV_VERSION='3.6.4'


# System specific changes
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "$machine" = 'Linux' ]; then
  if [ -f '/etc/os-release' ]; then
    DISTRO=$(cat /etc/os-release | grep -P '^NAME="(\w*)"' | grep -Po "(?<=\")[^\"]+(?=\")")
  fi

  # General Linux settings
  SUDO_BIN='/usr/bin/sudo'

  if [ "$DISTRO" = 'Ubuntu' ]; then
    # Apache (Debian/Ubuntu/Mint)
    SERVER_APACHE_SITES_AVAILABLE_DIR=/etc/apache2/sites-available
  fi
fi

