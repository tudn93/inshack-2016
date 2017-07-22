#!/bin/bash

# this script is an example of how should look a deployment script of a challenge
# (which is on git for example).

#########################
####### SETTINGS ########
#########################

# might be usefull some day
SCRIPT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"

# should be either APP or WEB depending of the challenge.
CHALL_TYPE="APP" # to adapt

# depending on "$CHALL_TYPE" we declare some variables.
if [[ ${CHALL_TYPE} == "APP" ]]; then
        CHALL_FOLDER_EXT="application_files"
	DELETE_SCRIPT_EXT="app"
elif [[ ${CHALL_TYPE} == "WEB" ]]; then
        CHALL_FOLDER_EXT="web_files"
        DELETE_SCRIPT_EXT="web"
fi

# must be less than 50 characters. Must start and end with a letter.
# And must contain only letters, numbers or '-' and '_'.
CHALL_NAME="challname" # to adapt

CHROOTING_SCRIPTS="/root/chrooting_scripts"
# look like this : /root/chrooting_scripts/challname_application_files
TEMP_FOLDER="${CHROOTING_SCRIPTS}/${CHALL_NAME}_${CHALL_FOLDER_EXT}"


#########################
####### COMMANDS ########
#########################

# moving only needed files (no .git sources if not needed!)
rm -rf ${TEMP_FOLDER}
mkdir -p ${TEMP_FOLDER}
cp the_challenge ${TEMP_FOLDER}/${CHALL_NAME}_chall # to adapt
# ex: cp my_python_chall.py ${TEMP_FOLDER}/${CHALL_NAME}_chall.py
cp the_chall_source.c ${TEMP_FOLDER}/${CHALL_NAME}_chall_source.c # to adapt (optional)
cp the_chall_flag.txt ${TEMP_FOLDER}/${CHALL_NAME}_flag # to adapt (optional)

# this line call delete_app.sh OR delete_web.sh to clean the old challenge
${CHROOTING_SCRIPTS}/delete_${DELETE_SCRIPT_EXT}.sh "${CHALL_NAME}"

# finally we can deploy
${CHROOTING_SCRIPTS}/deploy.sh "${CHALL_NAME}"
