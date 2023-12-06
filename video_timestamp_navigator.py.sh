#!/bin/zsh
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH"

#which python
#which python3
#pip install python-vlc pynput
python ./video_timestamp_navigator.py

cd -
