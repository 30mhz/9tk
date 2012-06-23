#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Checking python debian packages ..."

declare -a PKGS
PKGS=(python python-dev python-pip)

for PKG in "${PKGS[@]}"
do
    EXISTS=$(dpkg -s ${PKG} | grep installed)
    if [ EXISTS == "" ]; then
        echo "${PKG} is not installed"
        apt-get -force-yes --yes install ${PKG}
    else
        echo "${PKG} is installed"
    fi
done

echo ""
echo "Checking python libraries ..."

declare -a LIBS
LIBS=(pip virtualenv boto)

TMP_LIST="/tmp/python_lib_installed"
$(pip freeze >> ${TMP_LIST})
for LIB in "${LIBS[@]}"
do
    EXISTS=$(grep ${LIB} ${TMP_LIST})
    if [ EXISTS == "" ]; then
        echo "${LIB} is not installed"
        pip --upgrade ${LIB}
    else
        echo "${LIB} is installed"
    fi
done

echo ""
read -p "Do you want to setup backups (requires user-data)? [y/N] "
ANSWER=$REPLY
if [ "$ANSWER" == "y" ]; then
    echo "Configuring backup ..."
    python backup/backup.py setup
else
    echo "Skipping backup ..."
fi

echo ""
read -p "Do you want to setup an EIP (requires user-data)? [y/N] "
ANSWER=$REPLY
if [ "$ANSWER" == "y" ]; then
    echo "Configuring EIP ..."
    python eip/eip.py start
else
    echo "Skipping EIP ..."
fi

echo ""
read -p "Do you want to setup mount points (requires user-data)? [y/N] "
ANSWER=$REPLY
if [ "$ANSWER" == "y" ]; then
    echo "Configuring mount points ..."
    python mount/mount.py mount
else
    echo "Skipping mount points ..."
fi
