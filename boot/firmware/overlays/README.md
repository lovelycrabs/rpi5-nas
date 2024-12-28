## overlays配置
### 1，pwm-fan 配置
dts编译：
```shell
dtc -I dts -O dtb -o pwm-fan-lm75.dtbo pwm-fan-lm75.dts
dtc -I dts -O dtb -o pwm-fan-cpu.dtbo pwm-fan-cpu.dts
sudo cp pwm-fan-lm75.dtbo /boot/firmware/overlays
sudo cp pwm-fan-cpu.dtbo /boot/firmware/overlays
```
pwm-fan-lm75 为根据背板的温度传感器温度进行风扇调速

pwm-fan-cpu  根据cpu温度对风扇进行调速， 如果使用cpu进行调速，树莓派的3p风扇会无法动态调速。


配置：
编辑 /boot/firmware/config.txt

追加一下内容：

dtoverlay=pwm-fan-lm75

如果想根据cpu温度调节风扇的速度可以改成

dtoverlay=pwm-fan-cpu


### 2,PCIE配置
拷贝 pciex1-compat-pi5.dtbo 到 /boot/firmware/overlays

编辑 /boot/firmware/config.txt 并添加一下内容

dtparam=pciex1_gen=3

dtoverlay=pciex1-compat-pi5,no-mip
