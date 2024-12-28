#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    echo 'install fail!'
    echo "This script must be run as root." >&2
    exit 1
fi

cur_dir=$(dirname $0)
dts_dir=${cur_dir}/boot/firmware/overlays/
#echo ${cur_dir}
echo 'pwm-fan dts compiling ....'
dtc -I dts -O dtb -o ${dts_dir}/pwm-fan-lm75.dtbo ${dts_dir}/pwm-fan-lm75.dts
dtc -I dts -O dtb -o ${dts_dir}/pwm-fan-cpu.dtbo ${dts_dir}/pwm-fan-cpu.dts
echo 'pwm-fan dts compiled'
echo 'install dtbo'
cp -f ${dts_dir}/pwm-fan-lm75.dtbo /boot/firmware/overlays/
cp -f ${dts_dir}/pwm-fan-cpu.dtbo /boot/firmware/overlays/
cp -f ${dts_dir}/pciex1-compat-pi5.dtbo /boot/firmware/overlays/
echo 'install dtbo end'
echo 'enable pcie.....'
rpi-eeprom-config -a ${cur_dir}/conf/bootconf.txt
echo 'pcie enabled!'
echo 'firmware config....'
cp -f /boot/firmware/config.txt /boot/firmware/config.txt.bak
#sed -i 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/firmware/config.txt
#sed -i 's/#dtparam=spi=on/dtparam=spi=on/g' /boot/firmware/config.txt
#cat >> /boot/firmware/config.txt <<EOF
#dtoverlay=i2c-sensor,lm75,i2c1,addr=0x48
#dtparam=pciex1_gen=3
#dtoverlay=pciex1-compat-pi5,no-mip
#dtoverlay=pwm-fan-cpu
#dtoverlay=pwm-fan-lm75
#EOF
python ./utils/config.py
echo 'firmware config end'
chmod +x ${cur_dir}/utils/display/install.sh
echo 'install success, please reboot system!'
