#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
DIR="$( dirname "$SOURCE" )"
while [ -h "$SOURCE" ]
do 
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd )"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

echo "Configuring CMSYAAT...."
echo "Direct any complaints to andrew.melo@gmail.com"

export PYTHONPATH=$DIR/src:$PYTHONPATH
export PATH=$DIR/bin:$PATH

if [ ! -e $DIR/externals/WMClient/current/etc/wmclient.sh ]; then
    echo "WARNING: It doesn't appear you have WMClient installed"
    echo "             If you don't know what that means, run install-deps.sh"
else
    . $DIR/externals/WMClient/current/etc/wmclient.sh
fi
