#!/bin/zsh
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH"

pip install python-vlc pynput
python ./video_timestamp_navigator.py

cd -
