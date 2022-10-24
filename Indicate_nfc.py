import os, signal
from multiprocessing import Process
import subprocess

def func():
    os.system("ffplay 1")

def fun():
    while True:
        output = subprocess.check_output(['nfc-list'])
        if '93' in str(output):
            l = os.getpid()
            os.kill(l, signal.SIGKILL)

if __name__ == "__main__":
    p1 = Process(target=func)
    p2 = Process(target=fun)
    p1.start()
    p2.start()
