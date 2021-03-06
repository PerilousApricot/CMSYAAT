#!/bin/bash

echo "Retrieving dependencies for CMSYAAT"
SOURCE="${BASH_SOURCE[0]}"
DIR="$( dirname "$SOURCE" )"
while [ -h "$SOURCE" ]
do 
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd )"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
if [ ! -e $DIR/externals/WMClient ]; then
    echo "Installing WMClient..."
    (mkdir -p $DIR/externals/WMClient
    cd $DIR/externals/WMClient
    git clone git://github.com/dmwm/deployment.git
    cd deployment
    ./Deploy -R wmagent@0.9.30 -t v01 $DIR/externals/WMClient admin/devtools@0.9.30 wmclient@0.9.10
    #./Deploy -R wmagent@0.9.30 -t v01 $DIR/externals/WMClient admin/devtools@0.9.30 wmagent@0.9.30
    if [ $? -ne 0 ]; then
        echo "***Externals installation failed!***"
        echo "There are additional logs at bootstrap-\$arch.log, somewhere"
        echo "within this directory tree"
        exit 1
    fi
    ./Deploy -s post -t v01 $DIR/externals/WMClient admin/devtools wmclient
    )
else
    echo "WMClient appears to already be installed"
fi

echo "Done!"

