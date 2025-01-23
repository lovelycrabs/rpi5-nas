#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo 'install fail!'
    echo "This script must be run as root." >&2
    exit 1
fi
disp_dir=$(dirname $0)
echo ${disp_dir}
#cp -rf ${cur_dir} /usr/local
apt install python3-dev libfreetype6-dev
#if ! test -d "/usr/local/share/fonts/truetype"; then
#    mkdir -p /usr/local/share/fonts/truetype
#fi
#cp -f ${disp_dir}/fonts/*.ttf /usr/local/share/fonts/truetype
rm -f ${disp_dir}/config.py
touch ${disp_dir}/config.py
if test -d "/sys/class/i2c-adapter/i2c-1/1-0048"; then
    echo "lm75_device_hwmon = '/sys/class/i2c-adapter/i2c-1/1-0048/hwmon'" >> ${disp_dir}/config.py
    echo "ina226_device_hwmon='/sys/class/i2c-adapter/i2c-1/1-0040/hwmon'" >> ${disp_dir}/config.py
#   sed -i 's/{LM75_DEVICE_HW}/\/sys\/class\/i2c-adapter\/i2c-1\/1-0048\/hwmon/g' ${disp_dir}/main.py
elif test -d "/sys/class/i2c-dev/i2c-1/device/1-0048"; then
#   sed -i 's/{LM75_DEVICE_HW}/\/sys\/class\/i2c-dev\/i2c-1\/device\/1-0048\/hwmon/g' ${disp_dir}/main.py
    echo "lm75_device_hwmon = '/sys/class/i2c-dev/i2c-1/device/1-0048/hwmon'" >> ${disp_dir}/config.py
        echo "ina226_device_hwmon='/sys/class/i2c-dev/i2c-1/device/1-0040/hwmon'" >> ${disp_dir}/config.py
else
   echo "display install fail,lm75 device not found!"
   exit 1
fi
python3 -m venv ${disp_dir}/venv
${disp_dir}/venv/bin/pip install -r ${disp_dir}/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
#/usr/local/display/venv/bin/python /usr/local/display/main.py
if ! test -d "/usr/local/display"; then
    mkdir -p /usr/local/display
fi
cp -rf ${disp_dir}/* /usr/local/display
cp -f ${disp_dir}/spiled.service /etc/systemd/system
systemctl enable spiled.service
systemctl start spiled.service
