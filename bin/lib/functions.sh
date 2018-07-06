#!/usr/bin/env bash
# Hagan Franks 2016-09-13 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu

ask() {
    # http://djm.me/ask
    while true; do

        if [ "${2:-}" = "Y" ]; then
            ynprompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            ynprompt="y/N"
            default=N
        else
            ynprompt="y/n"
            default=
        fi

        echo -n "$1 [$ynprompt] "
        # Ask the question - use /dev/tty in case stdin is redirected from somewhere else
        read REPLY </dev/tty
        # </dev/tty

        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi

        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac
    done
}

function check_env_config_loaded() {
  # Script checks to make sure our .env loaded
  if [[ -z ${ENV_DEFINED+x} ]]; then
    echo "ERROR: .env does not not appear to be loaded!"
    echo "Make sure ENV_DEFINED=true is in your .env file!"
    return 1
  fi
}

## Pascal Pilz bash join function
function join_by { local IFS="$1"; shift; echo "$*"; }

function sort_str {
    ## Sort an array
    ## For example: 
    # VARRAY=( '2.7.14' '3.6.3' '3.6.2' '2.4.1' '2.7.13' '1')
    # sort_str ${VARRAY[@]}
    # That echo's back a sorted string!
    unset SORTED_ARRAY
    INPUT_ARRAY=( "$@" )
    # echo "Input Array"
    # printf "[%s]\n" "${INPUT_ARRAY[@]}"
    IFS=$'\n' SORTED_ARRAY=($(sort <<<"${INPUT_ARRAY[*]}"))
    unset IFS
    echo "$(join_by ' ' ${SORTED_ARRAY[@]} | sed -e 's/^[ \t]*//')"
    return 0
}

function function_exists {
    declare -f -F $1 > /dev/null
    return $?
}

function contains_element () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


return 0