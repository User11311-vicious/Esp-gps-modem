from bluetooth import *
import socket
import os
from multiprocessing import Process, shared_memory

pedal = shared_memory.ShareableList([' ', ' '], name="pedal") #pedals
#nastroyki_bluetooth
addr = "24:62:AB:E1:96:7A"
channel = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((addr, channel))
##########################
def l():
    while 1:
        try:
            data = s.recv(1024)
            data = data.decode('utf-8')
            data = data.split('|')

            if 'Brake depressed' in data:
                tormos = 'Brake depressed'
                pedal[0] = tormos
            elif 'Brake pressed' in data:
                tormos = 'Brake pressed'
                pedal[0] = tormos
            elif 'Brake ready' in data:
                tormos = 'Brake ready'
                pedal[0] = tormos
            #gas_starts...
            if 'Gas depressed' in data:
                gas = 'Gas depressed'
                pedal[1] = gas
            elif 'Gas pressed' in data:
                gas = 'Gas pressed'
                pedal[1] = gas
            elif 'Gas ready' in data:
                gas = 'Gas ready'
                pedal[1] = gas
        except:
            print('A little mistake')

def r():
    os.system('''ffmpeg -i /dev/video0 -vf drawtext="fontsize=35:fontcolor=black:text={}" -vf drawtext="fontsize=35:fontcolor=black:text={}" -t 00:03:00 -q:v 4 -s 1080x720 output.avi'''.format(str(pedal[0]), str(pedal[1])))

p1 = Process(target=l)
p2 = Process(target=r)
p1.start()
p2.start()
p1.join()
p2.join()
pedal.shm.close()
pedal.shm.unlink()
