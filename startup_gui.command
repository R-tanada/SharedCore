#!/bin/bash
sntp -sS ntp.nict.jp
script_dir=$(cd $(dirname $0); pwd)
cd $script_dir
source .venv/bin/activate
source config/core_activate.sh
python wg_sharedavatar_cake_expt/collaborative_app.py
