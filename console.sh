#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Checking python debian packages ..."

declare -a PKGS
PKGS=("python" "python-dev" "python-pip")

for PKG in "${PKGS[@]}"
do
    EXISTS=$(dpkg -s ${PKG} | grep installed)
    if [ "${EXISTS}" == "" ]; then
        echo "${PKG} is not installed"
        apt-get --yes install ${PKG}
    fi
done

echo ""
echo "Checking python libraries ..."

declare -a LIBS
LIBS=("virtualenv" "boto" "pystache" "mock")

TMP_LIST="/tmp/python_lib_installed"
$(pip freeze >> ${TMP_LIST})
for LIB in "${LIBS[@]}"
do
    EXISTS=$(grep ${LIB} ${TMP_LIST})
    if [ "${EXISTS}" == "" ]; then
        echo "${LIB} is not installed"
        pip install --upgrade ${LIB}
    fi
done

echo ""

python ./cli.py