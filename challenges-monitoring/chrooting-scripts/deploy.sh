#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

USERN=${1:-user}
USERN_CRACKED="${USERN}_cracked"
JAIL=${2:-/srv/jail/}
SCRIPT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Running script with user: ${USERN} and jail : ${JAIL}"
echo

#######################################
### Checking things... ################
#######################################
if [[ ! "${USERN}" =~ ^[a-zA-Z][a-zA-Z0-9_-]{0,48}[a-zA-Z]$ ]]; then
	printf "${RED}Username must be less than 50 characters. Must start and end with a letter. Must contain only letters, numbers or '-' and '_'.\n${NC}" >&2
	exit 1
fi

if id -u ${USERN} > /dev/null 2>&1; then
	printf "${RED}User ${USERN} already exists\n${NC}" >&2
	exit 1
fi

if id -u ${USERN_CRACKED} > /dev/null 2>&1; then
	printf "${RED}User ${USERN_CRACKED} already exists\n${NC}" >&2
	exit 1
fi

CHALL_TYPE="NONE"
DIRECTORY="${SCRIPT_PATH}/${USERN}_application_files"
if [ ! -d ${DIRECTORY} ]; then
	DIRECTORY="${SCRIPT_PATH}/${USERN}_web_files"
	if [ ! -d ${DIRECTORY} ]; then
		printf "${RED}Challenge directory absent, can't deploy things.\n" >&2
		printf "Challenge directory should have this name: '${USERN}_application_files' for challenge with privilege escalation.\n" >&2
		printf "OR this name: '${DIRECTORY}' for web challenge.\n${NC}" >&2
		exit 1
	else
		CHALL_TYPE="WEB"
	fi
else
	CHALL_TYPE="APP"
fi


#######################################
#### Launch appropriate script ########
#######################################

if [[ ${CHALL_TYPE} == "WEB" ]]; then
	echo "OK, but feature not ready yet."
	exit 0
	${SCRIPT_PATH}/deploy_web.sh "${USERN}" "${JAIL}"
elif [[ ${CHALL_TYPE} == "APP" ]]; then
	export FROM_DEPLOY=1
	${SCRIPT_PATH}/deploy_app.sh "${USERN}" "${JAIL}"
else
	printf "${RED}ERROR ! Bad script.\n${NC}" >&2
	exit 1
fi

echo
echo "Everything went well you can check it out by running: ssh ${USERN}@localhost"
