#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo 'install fail!'
    echo "This script must be run as root." >&2
    exit 1
fi
disp_dir=$(dirname $0)
echo ${disp_dir}
#cp -rf ${cur_dir} /usr/local
apt install python3-dev
#if ! test -d "/usr/local/share/fonts/truetype"; then
#    mkdir -p /usr/local/share/fonts/truetype
#fi
#cp -f ${disp_dir}/fonts/*.ttf /usr/local/share/fonts/truetype
python3 -m venv ${disp_dir}/venv
${disp_dir}/venv/bin/pip install -r ${disp_dir}/requirements.txt
#/usr/local/display/venv/bin/python /usr/local/display/main.py
if ! test -d "/usr/local/display"; then
    mkdir -p /usr/local/display
fi
cp -rf ${disp_dir}/* /usr/local/display
cp -f ${disp_dir}/spiled.service /etc/systemd/system
systemctl enable spiled.service
systemctl start spiled.service
