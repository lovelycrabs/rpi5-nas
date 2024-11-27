#!/usr/bin/python
import re

CONF_FILE_NAME = '/boot/firmware/config.txt'
config_lines = list()

class ConfigLine(object):
    selection = None
    line = None
    available = False
    def __init__(self,s,n,a=False):
        self.selection = s
        self.line = n
        self.available = a
        #if n.startswith('#')
        #    self.available = True

def read_config():
    selection = None
    global config_lines
    with open(CONF_FILE_NAME, 'r') as file:
        for line in file:
            #config_lines.append(line)
            item = line.strip()
            if not item:
                continue
            a = re.findall(r'[\[](.*?)[]]',item)
            if a:
                selection = a[0]
            available = item and not item.startswith('#')
            #print(line)
            config_lines.append(ConfigLine(selection, line, available))

def line_exists(selection, n):
    for line in config_lines:
        #print(line.line)
        if line.selection == selection and line.line.strip() == n.strip():
            return True
    return False

def get_selection_index(selection):
    for i in range(0,len(config_lines)):
        line = config_lines[i]
        if line.selection == selection:
            for j in range(i, len(config_lines)):
                if config_lines[j].selection != selection:
                    return j
            return j+1
    return i+1

def config_add(selection, line):
    if not line_exists(selection, line):
        idx = get_selection_index(selection)
        config_lines.insert(idx,ConfigLine(selection, line+'\n'))

def save_config():
    with open(CONF_FILE_NAME,'w') as file:
        file.writelines([line.line for line in config_lines])

if __name__=='__main__':
    read_config()
    config_add(None, 'dtparam=i2c_arm=on')
    config_add(None, 'dtparam=spi=on')
    config_add("all", 'dtoverlay=i2c-sensor,lm75,i2c1,addr=0x48')
    config_add("all", 'dtparam=pciex1_gen=3')
    config_add("all", 'dtoverlay=pciex1-compat-pi5,no-mip')
    config_add("all", 'dtoverlay=pwm-fan-auto')
    config_add("all", '#dtoverlay=pwm-fan')
    #config_add("cm5", "dd=ss")
    #config_add(None, "hh=bb")
    #config_add("all", "kk=aa")
    for line in config_lines:
        print(line.line)
    save_config()


