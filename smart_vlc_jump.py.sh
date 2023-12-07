#!/bin/zsh
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "$SCRIPTPATH"

python ./smart_vlc_jump.py "/Users/huangyingw/mini/media/usb_backup_crypt_8T_1/cartoon/" "./dragonball/第一部/龙珠 第一部 日语配音/七龙珠146.rmvb:13:57,:09:56"

cd -
