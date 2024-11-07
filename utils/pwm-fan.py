#!/usr/bin/python
import time
import os

temp_sensor_dir = "/sys/class/i2c-dev/i2c-1/device/1-0048/hwmon/"


for dir in os.listdir(temp_sensor_dir):
    temp_sensor_file = os.path.join(temp_sensor_dir, dir, "temp1_input")

temp_cpu_file = "/sys/class/hwmon/hwmon0/temp1_input"

pwm_fans_dir = ["/sys/devices/platform/fan1/hwmon",]
pwm_fans = list()
for pwm_fan in pwm_fans_dir:
    for pwm_dir in os.listdir(pwm_fan):
        pwm_fan_file = os.path.join(pwm_fan,pwm_dir, "pwm1")
        pwm_fans.append(pwm_fan_file)
test_passive_dutty = float(os.getenv("TEST_PASSIVE_DUTTY", "2"))
test_active_dutty = float(os.getenv("TEST_ACTIVE_DUTTY", "0.5"))
#风扇关闭温度
temp_sensor_passive = int(os.getenv("TEMP_SENSOR_PASSIVE", "38000")) 

#风扇开启温度
temp_sensor_min = int(os.getenv("TEMP_SENSOR_MIN", "40000"))
temp_sensor_max = int(os.getenv("TEMP_SENSOR_MAX", "80000"))

#风扇关闭温度
temp_cpu_passive = int(os.getenv("TEMP_CPU_PASSIVE", "63000"))

#风扇开启温度
temp_cpu_min = int(os.getenv("TEMP_CPU_MIN", "65000"))
temp_cpu_max = int(os.getenv("TEMP_CPU_MAX", "80000"))

fan_min = int(os.getenv("FAN_MIN", "50"))
fan_max = int(os.getenv("FAN_MAX", "150"))


working = True

sensor_e = float(fan_max - fan_min) / float(temp_sensor_max - temp_sensor_min)
cpu_e = float(fan_max - fan_min) / float(temp_cpu_max - temp_cpu_min)

DEBUG = os.getenv('PWM_FAN_DEBUG')


def get_temp(file):
    temp = 0
    with open(file, 'r') as f:
        temp = int(f.read())
    return temp;


def get_temp_st(temp, min, e):
    return (temp - min) * e


def test_temp():
    sensor_temp = get_temp(temp_sensor_file)
    cpu_temp = get_temp(temp_cpu_file)
    if DEBUG:
        print("sensor temp: %d, cpu temp: %d" % (sensor_temp, cpu_temp,))
    sensor_dt = get_temp_st(sensor_temp, temp_sensor_min, sensor_e)
    cpu_dt = get_temp_st(cpu_temp, temp_cpu_min, cpu_e)
    if sensor_dt > 0 or cpu_dt > 0:
        dt = sensor_dt if sensor_dt > cpu_dt else  cpu_dt
        write_fan(int(fan_min + dt))
    else:
        if working:
            if sensor_temp <= temp_sensor_passive and cpu_temp <= temp_cpu_passive:
                write_fan(0)
            else:
                write_fan(fan_min)


def write_fan(v):
    global working
    if v == 0 and not working:
	    return
    if v > 0:
        working = True
    else:
        working = False
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    for fan in pwm_fans:
        with open(fan, 'w') as f:
            f.write(str(v))
    if DEBUG:
        print("pwm value: %d" % v)


if __name__=='__main__':
    write_fan(0)
    while True:
        test_temp()
        if working:
            time.sleep(test_active_dutty)
        else:
            time.sleep(test_passive_dutty)

