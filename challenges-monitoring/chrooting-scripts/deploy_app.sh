#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

if [[ ! $FROM_DEPLOY == 1 ]]; then
	read -p "This script should be called by deploy.sh and shouldn't be called without it. Do you still want to proceed ? (Y/n)" -n 1 -r
	echo
	if [[ ! $REPLY =~ ^[Yy]$ ]]
	then
	    exit 1
	fi
fi

USERN=${1:-user}
USERN_CRACKED="${USERN}_cracked"
JAIL=${2:-/srv/jail/}
SCRIPT_PATH="$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )"

DIRECTORY=${3:-${SCRIPT_PATH}/${USERN}_application_files}

echo "Running APP script with user: ${USERN}, jail: ${JAIL} and dir: ${DIRECTORY}"
echo

#######################################
### Checking & Settings ###############
#######################################

CHALL_NAME=""
if [ -f ${DIRECTORY}/${USERN}_chall ]; then
	CHALL_NAME="${USERN}_chall"

	SOURCE_FILE=""
	if [ -f ${DIRECTORY}/${USERN}_chall_source.c ]; then
		SOURCE_FILE="${DIRECTORY}/${USERN}_chall_source.c"
	fi
else
	if [ -f ${DIRECTORY}/${USERN}_chall.py ]; then
		CHALL_NAME="${USERN}_chall.py"
	elif [ -f ${DIRECTORY}/${USERN}_chall.php ]; then
		CHALL_NAME="${USERN}_chall.php"
	elif [ -f ${DIRECTORY}/${USERN}_chall.pl ]; then
		CHALL_NAME="${USERN}_chall.pl"
	elif [ -f ${DIRECTORY}/${USERN}_chall.sh ]; then
		CHALL_NAME="${USERN}_chall.sh"
	else
		printf "${RED}No challenge file here : ${DIRECTORY}/\n" >&2
		printf "The challenge file can be a binary file (${DIRECTORY}/${USERN}_chall), a python file (.py), PHP file (.php), PERL file (.pl) or a bash file (.sh).\n${NC}" >&2
		exit 1
	fi

	WRAPPER_SOURCE_FILE="${SCRIPT_PATH}/wrapper_template.c"
	if [ ! -f ${WRAPPER_SOURCE_FILE} ]; then
		printf "${RED}The wrapper template is absent.\n${NC}" >&2
		exit 1
	fi
fi

FLAG_FILE=""
if [ -f ${DIRECTORY}/${USERN}_flag ]; then
	FLAG_FILE="${DIRECTORY}/${USERN}_flag"
fi

#######################################
### End checking ######################
#######################################

#######################################
### Running things... #################
#######################################
### USERS #############################
#######################################
echo "Running :"
echo "useradd ${USERN} -s /bin/bash"
if ! useradd ${USERN} -s /bin/bash; then
	printf "${RED}Error adding user.\n${NC}" >&2
	exit 1
fi

echo "Running :"
echo "echo ${USERN}:PASS | chpasswd"
if ! echo ${USERN}:${USERN} | chpasswd; then
	printf "${RED}Error changing user's passwd.\n${NC}" >&2
	exit 1
fi

echo "Running :"
echo "useradd ${USERN_CRACKED} -s /bin/bash"
if ! useradd ${USERN_CRACKED} -s /bin/bash; then
	printf "${RED}Error adding user cracked.\n${NC}" >&2
	exit 1
fi

echo "Running :"
echo "usermod --lock ${USERN_CRACKED}"
if ! usermod --lock ${USERN_CRACKED}; then
#if ! echo ${USERN_CRACKED}:${USERN_CRACKED} | chpasswd; then
	printf "${RED}Error disabling user cracked's passwd.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo "adduser ${USERN} sshusers"
if ! adduser ${USERN} sshusers; then
	printf "${RED}Error adding user to sshusers group.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo 'cat /etc/group | egrep "${USERN}:x:[0-9]+:.*" >> ${JAIL}etc/group'
if ! cat /etc/group | egrep "${USERN}:x:[0-9]+:.*" >> ${JAIL}etc/group; then
        printf "${RED}Error adding user to jail's /etc/group file.\n${NC}" >&2
        exit 1
fi

echo
echo "Running :"
echo 'cat /etc/group | egrep "${USERN_CRACKED}:x:[0-9]+:.*" >> ${JAIL}etc/group'
if ! cat /etc/group | egrep "${USERN_CRACKED}:x:[0-9]+:.*" >> ${JAIL}etc/group; then
	printf "${RED}Error adding user cracked to jail's /etc/group file.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo 'cat /etc/passwd | egrep "${USERN}:x:[0-9]+:[0-9]+::/home/.*" >> ${JAIL}etc/passwd'
if ! cat /etc/passwd | egrep "${USERN}:x:[0-9]+:[0-9]+::/home/.*" >> ${JAIL}etc/passwd; then
	printf "${RED}Error adding user to jail's /etc/passwd file.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo 'cat /etc/passwd | egrep "${USERN_CRACKED}:x:[0-9]+:[0-9]+::/home/.*" >> ${JAIL}etc/passwd'
if ! cat /etc/passwd | egrep "${USERN_CRACKED}:x:[0-9]+:[0-9]+::/home/.*" >> ${JAIL}etc/passwd; then
	printf "${RED}Error adding user cracked to jail's /etc/passwd file.\n${NC}" >&2
	exit 1
fi
#######################################
### END USERS #########################
#######################################

#######################################
### Creating/moving files #############
#######################################
echo
echo "Running :"
echo "mkdir ${JAIL}home/${USERN}/"
if ! mkdir ${JAIL}home/${USERN}/; then
	printf "${RED}Error creating user's home folder.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo "cp ${DIRECTORY}/${CHALL_NAME} ${JAIL}home/${USERN}/${CHALL_NAME}"
if ! cp ${DIRECTORY}/${CHALL_NAME} ${JAIL}home/${USERN}/${CHALL_NAME}; then
	printf "${RED}Error copying challenge file.\n${NC}" >&2
	exit 1
fi

echo
echo "Running :"
echo "chmod 550 ${JAIL}home/${USERN}/${CHALL_NAME}"
if ! chmod 550 ${JAIL}home/${USERN}/${CHALL_NAME}; then
	printf "${RED}Error changing mod challenge file.\n${NC}" >&2
	exit 1
fi

if [ ${CHALL_NAME} == "${USERN}_chall" ]; then
	if [[ ! ${SOURCE_FILE} == "" ]]; then
		echo
		echo "Running :"
		echo "cp ${SOURCE_FILE} ${JAIL}home/${USERN}/${USERN}_chall_source.c"
		if ! cp ${SOURCE_FILE} ${JAIL}home/${USERN}/${USERN}_chall_source.c; then
			printf "${RED}Error copying source file.\n${NC}" >&2
			exit 1
		fi

		echo
		echo "Running :"
		echo "chmod 440 ${JAIL}home/${USERN}/${USERN}_chall_source.c"
		if ! chmod 440 ${JAIL}home/${USERN}/${USERN}_chall_source.c; then
			printf "${RED}Error changing mod source file.\n${NC}" >&2
			exit 1
		fi

	fi
else
	echo
	echo "Running :"
	echo "sed 's/SCRIPT_PATH_IN_JAIL/\/home\/${USERN}\/${CHALL_NAME}/g' ${WRAPPER_SOURCE_FILE} > ${JAIL}home/${USERN}/wrapper.c"
	sed 's/SCRIPT_PATH_IN_JAIL/\/home\/'"${USERN}"'\/'"${CHALL_NAME}"'/g' ${WRAPPER_SOURCE_FILE} > ${JAIL}home/${USERN}/wrapper.c
	if ! [ $? -eq 0 ]; then
		printf "${RED}Error changing template wrapper.\n${NC}" >&2
		exit 1
	fi

	echo
	echo "Running :"
	echo "gcc ${JAIL}home/${USERN}/wrapper.c -o ${JAIL}home/${USERN}/wrapper"
	if ! gcc ${JAIL}home/${USERN}/wrapper.c -o ${JAIL}home/${USERN}/wrapper; then
		printf "${RED}Error while compiling wrapper.\n${NC}" >&2
		exit 1
	fi

	echo
	echo "Running :"
	echo "chmod 440 ${JAIL}home/${USERN}/wrapper.c"
	if ! chmod 440 ${JAIL}home/${USERN}/wrapper.c; then
		printf "${RED}Error changing mod wrapper.c .\n${NC}" >&2
		exit 1
	fi
fi

echo
echo "Running :"
echo "chown ${USERN_CRACKED}:${USERN} ${JAIL}home/${USERN} && chmod 550 ${JAIL}home/${USERN}/ && chattr -R +i ${JAIL}home/${USERN}/"
change_posix=$(chown ${USERN_CRACKED}:${USERN} ${JAIL}home/${USERN} -R && chmod 550 ${JAIL}home/${USERN}/)
if ! [ $? -eq 0 ] ; then
	printf "${RED}Error changing POSIX in defaults files in user's home.\n${NC}" >&2
	exit 1
fi

if [[ ! ${FLAG_FILE} == "" ]]; then
	echo
	echo "Running :"
	echo "cp ${FLAG_FILE} ${JAIL}home/${USERN}/${USERN}_flag"
	if ! cp ${FLAG_FILE} ${JAIL}home/${USERN}/${USERN}_flag; then
		printf "${RED}Error copying flag file.\n${NC}" >&2
		exit 1
	fi

	echo
	echo "Running :"
	echo "chmod 400 ${JAIL}home/${USERN}/${USERN}_flag"
	if ! chmod 400 ${JAIL}home/${USERN}/${USERN}_flag; then
		printf "${RED}Error changing mod flag file.\n${NC}" >&2
		exit 1
	fi

	echo
	echo "Running :"
	echo "chown ${USERN_CRACKED}:${USERN_CRACKED} ${JAIL}home/${USERN}/${USERN}_flag"
	if ! chown ${USERN_CRACKED}:${USERN_CRACKED} ${JAIL}home/${USERN}/${USERN}_flag; then
		printf "${RED}Error changing owner source file.\n${NC}" >&2
		exit 1
	fi
fi

# we change the suid bit AFTER changing owner, otherwise suid is reset
if [ ${CHALL_NAME} == "${USERN}_chall" ]; then
	echo
	echo "Running :"
	echo "chmod u+s ${JAIL}home/${USERN}/${CHALL_NAME}"
	if ! chmod u+s ${JAIL}home/${USERN}/${CHALL_NAME}; then
		printf "${RED}Error applying uidbit to challenge file.\n${NC}" >&2
		exit 1
	fi
else
	echo
	echo "Running :"
	echo "chmod 4550 ${JAIL}home/${USERN}/wrapper"
	if ! chmod 4550 ${JAIL}home/${USERN}/wrapper; then
		printf "${RED}Error changing mod wrapper (adding suid bit and exec).\n${NC}" >&2
		exit 1
	fi
fi

echo
echo "Running:"
echo "chattr -R +i ${JAIL}home/${USERN}/"
if ! chattr -R +i ${JAIL}home/${USERN}/; then
	printf "${RED}Error while +i to attr (to avoid users to delete or change challenge)\n${NC}" >&2
	exit 1
fi

#######################################
### End Creating/moving files #########
#######################################


