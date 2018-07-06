#!/usr/bin/env sh
# Hagan Franks 2016-09-13 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu
#
# TO USE THIS source passing the path to the project directory ie:
# . <path to root of project>/bin/lib/load-env-vars.sh
# For example:
# . ${script_dir}/lib/load-env-vars.sh || { echo "${script_dir}/lib/load-env-vars.sh had an error! exiting..."; exit 1 }
GUESS_PROJECT_ROOT=$(${READLINK} -f ${script_dir}/..)
ENV_FILE=$(find ${GUESS_PROJECT_ROOT} -type f -name ".env" \( -not -path "${GUESS_PROJECT_ROOT}/postgres/*" -a -not -path "${GUESS_PROJECT_ROOT}/envs/*" \) | xargs)
ENV_FILE_CNTR=$(find ${GUESS_PROJECT_ROOT} -type f -name ".env" \( -not -path "${GUESS_PROJECT_ROOT}/postgres/*" -a -not -path "${GUESS_PROJECT_ROOT}/envs/*" \) -print0 | xargs -0 -I{} echo {} | wc -l)

if [ ${ENV_FILE_CNTR} -eq 1 ] && [ -f $ENV_FILE ]; then
    echo "Found env file @ $ENV_FILE"
    . $ENV_FILE
elif [ ${ENV_FILE_CNTR} -gt 1 ] && [ -f $(echo ${ENV_FILE} | awk '{ print $1 }') ]; then
    # && [ -f ${ENV_FILE[0]} ]
    ENV_FILE=$(echo ${ENV_FILE} | awk '{ print $1 }')
    echo "Found env file @ ${ENV_FILE}"
    . $ENV_FILE
else
    echo "ERROR: Couldn't find .env file in project!"
    echo "Copy the example env file: ${GUESS_PROJECT_ROOT}/bcfsrc/.env_example] to ${GUESS_PROJECT_ROOT}/bcfsrc/.env and modify."
    return 1
fi

return 0