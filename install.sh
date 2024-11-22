#!/bin/bash
cur_dir=$(dirname $0)
dts_dir=${cur_dir}/boot/firmware/overlays/
#echo ${cur_dir}
echo 'pwm-fan dts compiling ....'
dtc -I dts -O dtb -o ${dts_dir}/pwm-fan.dtbo ${dts_dir}/pwm-fan.dts
dtc -I dts -O dtb -o ${dts_dir}/pwm-fan-auto.dtbo ${dts_dir}/pwm-fan-auto.dts
echo 'pwm-fan dts compiled'
echo 'install dtbo'
cp -f ${dts_dir}/pwm-fan.dtbo /boot/firmware/overlays/
cp -f ${dts_dir}/pwm-fan-auto.dtbo /boot/firmware/overlays/
cp -f ${dts_dir}/pciex1-compat-pi5.dtbo /boot/firmware/overlays/
echo 'install dtbo end'
echo 'config pcie.....'
cp -f /boot/firmware/config.txt /boot/firmware/config.txt.bak
sed -i 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/firmware/config.txt
sed -i 's/#dtparam=spi=on/dtparam=spi=on/g' /boot/firmware/config.txt
cat >> /boot/firmware/config.txt <<EOF
dtoverlay=i2c-sensor,lm75,i2c1,addr=0x48
dtparam=pciex1_gen=3
dtoverlay=pciex1-compat-pi5,no-mip
dtoverlay=pwm-fan-auto
#dtoverlay=pwm-fan
EOF
echo 'config pcie end'
echo 'install success, please reboot system!'
