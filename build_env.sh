#!/bin/bash

ENV_ROOT=./.env

if [ $# != "1" ];
then
    echo "Usage: $0 [install|activate]"
    exit
fi

if [ "$1" == "install" ]; then
    virtualenv --no-site-packages $ENV_ROOT
    source $ENV_ROOT/bin/activate
    pip install -r REQUIREMENTS

elif [ "$1" == "activate" ]; then
    source $ENV_ROOT/bin/activate
    bash
else
    echo "Usage: $0 [install|activate]"
fi
