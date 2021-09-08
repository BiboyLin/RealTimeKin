import socket
import time
import os
import numpy as np
import sys
from multiprocessing import Process, Manager

from UDP_process_mana import UDP_process
from JY91_WIFI import JY91_WIFI_Read


# cur_IMU_raw_data = [cur_ID] + acc + gyro + ang + mag

def IMU_process(sync_data_pool,used_idx):
    cnnt = 1
    while cnnt<=200:
        cur_used_sensor = JY91_WIFI_Read(sync_data_pool,used_idx)
        
        cur_used_sensor.acc = cur_used_sensor.get_acceleration()
        cur_used_sensor.gyro = cur_used_sensor.get_gyro()
        cur_used_sensor.angle = cur_used_sensor.get_angle()
        
        cur_used_sensor.print_cur_data()

        print(cur_used_sensor.acc)
        print(cur_used_sensor.gyro)
        print(cur_used_sensor.angle)  

        time.sleep(0.01)
        cnnt = cnnt + 1

def test_000():
    manager = Manager()
    sync_data_pool = manager.list()

    used_idx = 1


    UDPproc = Process(target=UDP_process,args=(sync_data_pool,))
    UDPproc.start()

    # time.sleep(1)

    IMUproc = Process(target=IMU_process,args=(sync_data_pool,used_idx))
    IMUproc.start()

    UDPproc.join()
    print(sync_data_pool)



if __name__ == "__main__":
    test_000()