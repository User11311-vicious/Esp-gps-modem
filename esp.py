from bluetooth import *
from time import sleep
from multiprocessing import Process, shared_memory
import socket

indi = shared_memory.ShareableList([0], name="indicate")

addr = "24:62:AB:E1:96:7A"
channel = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((addr, channel))

while True:
    try:
        if indi[0] == 1:
            addr = "24:62:AB:E1:96:7A"
            channel = 1
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            s.connect((addr, channel))
            indi[0] = 0
        data = s.recv(1024)
        data = data.decode('utf-8')
        data = data.split('|')
        print ("received [%s]" % data)
        sleep(1)
    except:
        indi[0] = 1
        print('boulll')
        sleep(1)

indi.shm.close()
indi.shm.unlink()
