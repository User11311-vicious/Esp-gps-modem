import serial
from datetime import datetime
from time import sleep
from math import pi
import csv

start_time = datetime.now()
ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200
csv_main = 'lohghggh.csv'
a = True
ig = ''
a_x, g_x, velocity, v0, info_gps, gps_vel_2, a_y, r = 0.0, 0.0, 0.0, 0.0, '', '', 0.0, 0.0
fieldnames = ['Date', 'Speed, km/h', 'X-axis acceleration, m/s^2', 'Y-axis acceleration, m/s^2', 'Angular acceleration, rad/s^2', 'GPS']
while True:
    try:
        data_gps = ser.readline().decode('ISO-8859-1')
        if '$GNVTG' in data_gps:
            info_gps += data_gps
            info_gps = str(info_gps)
            info_gps = info_gps.split(',')
            velocity = float(info_gps[7])
            a_x = (velocity - v0)/0.36
            v0 = velocity
            info_gps = ''
        if 'GNRMC' in data_gps:
            gps_vel_2 += data_gps
            g_x = float(gps_vel_2[9])
            g_x = round((g_x/180)*pi, 2)
            if g_x != 0:
                r = a_x/(g_x/0.25)
            a_y = round(g_x**2*r, 2)
            gps_vel_2 = ''
        ig = ig + data_gps
        print('Ускорение по x: ', a_x)
        print('Уксорение по y: ', a_y)
        print('Скорость: ', velocity)
        print('Угловое ускорение: ', g_x)
        with open(csv_main, mode="a+", encoding='ISO-8859-1') as a:
            writer = csv.DictWriter(a, fieldnames=fieldnames)
            if a == True:
                writer.writeheader()
                a = False 
            writer.writerows([{'Date': datetime.now(), 'Speed, km/h': str(velocity), 'X-axis acceleration, m/s^2': a_x, 'Y-axis acceleration, m/s^2': a_y, 'Angular acceleration, rad/s^2': str(g_x)}])
            if 'GNGLL' in ig:
                writer.writerows([{'Date': datetime.now(), 'Speed, km/h': str(velocity), 'X-axis acceleration, m/s^2': a_x, 'Y-axis acceleration, m/s^2': a_y, 'Angular acceleration, rad/s^2': str(g_x), 'GPS': info_gps}])        
                ig = ''
    except BaseException as err:
        print(err)
    except:
        print('hahahah')