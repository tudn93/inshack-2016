#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

USERN=${1:-user}
USERN_CRACKED="${USERN}_cracked"
JAIL=${2:-/srv/jail/}
echo "Running script with user: ${USERN} and jail : ${JAIL}"

if [[ ! "${USERN}" =~ ^[a-zA-Z][a-zA-Z0-9_-]{0,48}[a-zA-Z]$ ]]; then
	printf "${RED}Username must be less than 50 characters. Must start and end with a letter. Must contain only letters, numbers or '-' and '_'.\n${NC}" >&2
	exit 1
fi

if [ ! -d ${JAIL}home/${USERN} ]; then
        printf "${RED}The user is absent from jail. Exiting..\n${NC}" >&2
        exit 1
fi

if ! id -u ${USERN} > /dev/null 2>&1; then
	printf "${RED}User ${USERN} does not exists\n${NC}" >&2
	exit 1
fi

if ! id -u ${USERN_CRACKED} > /dev/null 2>&1; then
	printf "${RED}User ${USERN_CRACKED} does not exists\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo "userdel ${USERN}"
if ! userdel ${USERN}; then
	printf '${RED}Error deleting user\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "userdel ${USERN_CRACKED}"
if ! userdel ${USERN_CRACKED}; then
	printf '${RED}Error deleting user cracked\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "chattr -R -i ${JAIL}home/${USERN}/"
if ! chattr -R -i ${JAIL}home/${USERN}/; then
	printf '${RED}Error removing i attr from user home.\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "chmod 700 ${JAIL}home/${USERN}/ -R"
if ! chmod 700 ${JAIL}home/${USERN}/ -R; then
	printf '${RED}Error chmoding up user home POSIX.\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "rm -rf ${JAIL}home/${USERN}/"
if ! rm -rf ${JAIL}home/${USERN}/; then
	printf '${RED}Error deleting user home.\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "rm -rf ${JAIL}home/${USERN}/"
if ! rm -rf ${JAIL}home/${USERN}/; then
	printf '${RED}Error deleting user home.\n${NC}' >&2
	exit 1
fi

echo
echo "Running :"
echo "sed -r '/${USERN}(_cracked)?:x:[0-9]+:[0-9]+::\/home\/.*/d' ${JAIL}etc/passwd > ${JAIL}etc/passwd "
sed -r '/'"${USERN}"'(_cracked)?:x:[0-9]+:[0-9]+::\/home\/.*/d' ${JAIL}etc/passwd > /tmp/passwd_temp
if ! [ $? -eq 0 ]; then
	printf "${RED}Error deleting user cracked entry in jail's /etc/passwd.\n${NC}" >&2
	exit 1
else
	cat /tmp/passwd_temp > ${JAIL}etc/passwd
fi

echo
echo "Running :"
echo "sed -r '/${USERN}(_cracked)?:x:[0-9]+:.*/d' ${JAIL}etc/group > ${JAIL}etc/group"
sed -r '/'"${USERN}"'(_cracked)?:x:[0-9]+:.*/d' ${JAIL}etc/group > /tmp/group_temp
if ! [ $? -eq 0 ]; then
	printf "${RED}Error deleting user cracked entry in jail's /etc/group.\n${NC}" >&2
	exit 1
else
        cat /tmp/group_temp > ${JAIL}etc/group
fi

echo
echo "Please check passwd file there :"
tail -n10 ${JAIL}etc/passwd

echo
echo "Please check group file there :"
tail -n10 ${JAIL}etc/group

echo
echo "Please check jail's home folder :"
ls -la ${JAIL}home

echo
echo "Thanks ! All good."
