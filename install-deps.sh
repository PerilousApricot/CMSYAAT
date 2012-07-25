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

(mkdir -p $DIR/externals/WMClient
cd $DIR/externals/WMClient
git clone git://github.com/dmwm/deployment.git
cd deployment
./Deploy -s prep -t v01 $DIR/externals/WMClient wmclient@0.9.0
./Deploy -s sw -t v01 $DIR/externals/WMClient wmclient@0.9.0
./Deploy -s post -t v01 $DIR/externals/WMClient wmclient@0.9.0
)

echo "Done!"



