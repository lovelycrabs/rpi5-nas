## Installation
1.config system
```shell
git clone https://github.com/lovelycrabs/rpi5-nas.git
cd rpi5-nas
sudo chmod +x install.sh
sudo ./install.sh
sudo reboot
```
3.5寸4盘位RPI5_NAS_H4需要修改/boot/firmware/config.txt,该版本的风扇支持二线、三线、四线通用风扇、pwm风扇的周期改成20000000ns即频率为50hz
sudo nano /boot/firmware/config.txt
```shell
dtoverlay=pwm-fan-lm75,period=20000000
```
可以通过 cat /sys/class/i2c-dev/i2c-1/device/1-0040/hwmon/hwmon*/power1_input查看系统功率
cat /sys/class/i2c-dev/i2c-1/device/1-0040/hwmon/hwmon*/in1_input查看输入电压

2.install spi oled service
```shell
cd rpi5-nas/utils/display
sudo ./install.sh
```
