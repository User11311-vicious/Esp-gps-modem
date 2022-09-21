import subprocess
from time import *
import os
import threading

hosts = '/home/ldprpc15/Desktop/hosts'
redirect_url = '127.0.0.1'
blocked_sites = 'http://nmcheck.gnome.org/'

def reboot(): 
    print("Internet is still down :(")
    #execute command lsusb
    feedback_lsusb = subprocess.Popen('lsusb', stdout=subprocess.PIPE)
    #read output
    text = feedback_lsusb.stdout.read()
    #traslate in string
    output = str(text)
    #division on rows
    output = output.split('\\n')
    #detect ID of modem
    del output[len(output)-1]
    for i in range(len(output)-1, -1, -1):
        if 'Huawei Technologies Co., Ltd. E353/E3131' not in output[i]:
            del output[i]

    output = str(output)
    #mark 'bus' and 'dev' of modem
    bus = output[6:9]
    dev = output[17:20]
    #commands for 'off modem' and 'on modem'
    begining = 'sudo ./hub-ctrl -b ' + str(bus) + ' -d ' + str(dev) + ' -P 1 -p 0'
    end = 'sudo ./hub-ctrl -b ' + str(bus) + ' -d ' + str(dev) + ' -P 1 -p 1'
    #execute programm in this path
    os.chdir(r"/home/ldprpc15/hub-ctrl.c")
    #next 4 rows == reboot modem
    process = subprocess.call(begining, text=True, encoding="UTF8", shell=True)
    sleep(15)
    print('OKAY')
    process = subprocess.call(end, shell=True)
    sleep(105)

def block_site():
    while True:
        print('H')
        with open('/home/ldprpc15/Desktop/hosts', 'r+') as file:
            src = file.read()
            for website in blocked_sites:
                if website in src:
                    pass
                else:
                    # mapping hostnames to your localhost IP address
                    file.write(redirect_url + " " + website + "\n")

internet = False
while not internet:
    try:
        #www.browser_name.ru, so you must write firefox, google or yandex instead of 'browser_name'
        subprocess.check_call(['ping', '-c 1',  'firefox.ru'])
        output_0 = subprocess.getoutput(["ping -c 1 firefox.ru"])
        print(output_0)
        output_0 = output_0.split(' ')
        for j in output_0:
            if 'time' in j:
                output_0 = j
                print(output_0)
                output_0 = float(output_0[5:])
                if output_0 >= 150:
                    reboot()
                break
        print("Internet is up again!")
        internet = True
    except subprocess.CalledProcessError:
        thread1 = threading.Thread(target=reboot)
        thread2 = threading.Thread(target=block_site)
        thread1.start()
        tim = threading.Timer(5.0, block_site)
        print('Reconnect')
        tim.start()
        thread1.join()
        thread2.join()
