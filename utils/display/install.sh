#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo 'install fail!'
    echo "This script must be run as root." >&2
    exit 1
fi
disp_dir=$(dirname $0)
echo ${disp_dir}
#cp -rf ${cur_dir} /usr/local
apt install python3-dev libfreetype6-dev libopenblas-dev libjpeg-dev libopenjp2-7
#if ! test -d "/usr/local/share/fonts/truetype"; then
#    mkdir -p /usr/local/share/fonts/truetype
#fi
#cp -f ${disp_dir}/fonts/*.ttf /usr/local/share/fonts/truetype
rm -f ${disp_dir}/config.py
touch ${disp_dir}/config.py
if  test -d "/sys/class/i2c-adapter/i2c-1/1-0048/hwmon"; then
    echo "lm75_device_hwmon = '/sys/class/i2c-adapter/i2c-1/1-0048/hwmon'" >> ${disp_dir}/config.py

elif test -d "/sys/class/i2c-dev/i2c-1/device/1-0048/hwmon"; then
    echo "lm75_device_hwmon = '/sys/class/i2c-dev/i2c-1/device/1-0048/hwmon'" >> ${disp_dir}/config.py

else
    echo "warning:device lm75 not found!"
    exit 1
fi
if  test -d "/sys/class/i2c-adapter/i2c-1/1-0040/hwmon"; then
    echo "ina226_device_hwmon = '/sys/class/i2c-adapter/i2c-1/1-0040/hwmon'" >> ${disp_dir}/config.py
elif test -d "/sys/class/i2c-dev/i2c-1/device/1-0040/hwmon"; then
    echo "ina226_device_hwmon = '/sys/class/i2c-dev/i2c-1/device/1-0040/hwmon'" >> ${disp_dir}/config.py

else
    echo "warning:device ina226 not found!"
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
echo 'install path: /usr/local/display'
echo 'install success!'