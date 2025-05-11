#!/usr/bin/env python3
import sys

from PIL import Image, ImageDraw, ImageFont
import time
import st7789
import psutil
import os

hwmon_base_path = "/sys/class/hwmon"

def get_string(file):
    str = None
    with open(file, 'r') as f:
        str = f.read().strip()
    return str

def get_hwmon_path(dev_name):
    for dir in os.listdir(hwmon_base_path):
        full_path = os.path.join(hwmon_base_path, dir)
        dev_name_file = os.path.join(full_path, "name")
        if os.path.exists(dev_name_file):
            hw_name = get_string(dev_name_file)
            #print(hw_name)
            if hw_name == dev_name:
                return full_path

    return None

temp_cpu_file = hwmon_base_path + "/hwmon0/temp1_input"
lm75_hwmon_path = get_hwmon_path("lm75")
ina226_hwmon_path = get_hwmon_path("ina226")

int_addresses =list()

def get_temp(file):
    temp = 0
    with open(file, 'r') as f:
        temp = int(f.read())
    return temp

def draw_text(disp, text, x, y, w, h, font_size):
    img = Image.new("RGB", (w, h), color=(0, 0, 0))
    font = ImageFont.truetype("fonts/FreeSansBold.ttf", font_size)
    #font = ImageFont.default()
    textdraw = ImageDraw.Draw(img)
    textdraw.text((0, 0), text, font=font, fill=(255,255,255))
    disp.display(img, x, y, w, h)

def draw_time(disp, x, y, w, h, font_size):
    now_time = time.localtime()
    current_time = time.strftime('%a,    %Y-%m-%d %H:%M:%S', now_time)
    draw_text(disp,current_time,x,y,w,h,font_size)

def draw_cpuinfo(disp, x, y, w, h, font_size):
    cpu_info=psutil.cpu_percent()
    pids = psutil.pids()
    draw_text(disp,"cpu:{0}%,    pids:{1}".format(cpu_info, len(pids)),x,y,w,h,font_size)

def draw_mem(disp, x, y, w, h, font_size):
    mem_info = psutil.virtual_memory()
    draw_text(disp,"mem total:{0}M, used:{1}%".format(format(mem_info.total/1024/1024,".0f"), mem_info.percent),x,y,w,h,font_size)

def ip_changed(a, b):
    if len(a)!=len(b):
        return True
    for i in range(0, len(a)):
        if a[i]!=b[i]:
            return True
    return False

def draw_net(disp, x, y, w, h, font_size):
    interfaces = psutil.net_if_addrs()
    global int_addresses
    new_addresses = list()
    h_offset=0
    for name, addrs in interfaces.items():
        if name == "lo":
            continue
        ip_add = "{0}:{1}".format(name, addrs[0].address)
        new_addresses.append(ip_add)
    if ip_changed(int_addresses, new_addresses):
        int_addresses = new_addresses
        img = Image.new("RGB", (w, h), color=(0, 0, 0))
        font = ImageFont.truetype("fonts/FreeSansBold.ttf", font_size)
        textdraw = ImageDraw.Draw(img)
        #textdraw.text((0, 0), text, font=font, fill=(255,255,255))
        for ipstr in new_addresses:
            textdraw.text((0, h_offset), ipstr, font=font, fill=(255,255,255))
            h_offset = h_offset + font_size+2

        disp.display(img, x, y, w, h)

def draw_temp(disp, x, y, w, h, font_size):
    cpu_temp = get_temp(temp_cpu_file)
    if lm75_hwmon_path:
        temp_hwmon_file = os.path.join(lm75_hwmon_path, "temp1_input")
        if os.path.exists(temp_hwmon_file):
            temp_value = get_temp(temp_hwmon_file)
            board_temp = format(temp_value/1000,'.1f')
        else:
            board_temp = "err"
    else:
        board_temp = "err"
    draw_text(disp,"cpu temp:{0}, board temp:{1}".format(format(cpu_temp/1000,'.1f'), board_temp),x,y,w,h,font_size)

def draw_power(disp, x, y, w, h, font_size):
    if not ina226_hwmon_path:
        draw_time(disp, x, y, w, h, font_size)
        return
    pw_file = os.path.join(ina226_hwmon_path, 'power1_input')
    if os.path.exists(pw_file):
        pw_val = get_temp(pw_file)
        pw = format(pw_val/1000000, '.2f')
    else:
        pw = "err"
    vol_file = os.path.join(ina226_hwmon_path, 'in1_input')
    if os.path.exists(vol_file):
        vol_val = get_temp(vol_file)
        vol = format(vol_val/1000, '.2f')
    else:
        vol = "err"
    draw_text(disp , "power:{0}w, vol:{1}v".format(pw, vol), x, y, w, h, font_size)


disp = st7789.ST7789(
    height=135,
    width=240,
    rotation=0,
    port=0,
    cs=0,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=23,
    rst=24,
    backlight=13,  # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=2000000,
    offset_left=40,
    offset_top=53,
)


# Initialize display.
disp.begin()
#disp.reset()
WIDTH = disp.width
HEIGHT = disp.height
disp.fill_rect((0,0,0),0,0)

while(True):
    draw_net(disp,0,0,WIDTH, 40, 16)
    draw_power(disp,0, 115, WIDTH, 20, 18)
    draw_cpuinfo(disp,0,44,WIDTH, 20, 18)
    draw_mem(disp,0, 64, WIDTH, 20, 16)
    draw_temp(disp, 0, 84,WIDTH, 20, 16)
    time.sleep(1)
