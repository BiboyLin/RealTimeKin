# JY91_WIFI
# IMU_COLL_0 = 
import numpy as np
import os
from multiprocessing import Process, Queue

class JY91_WIFI_Read(object):
    def __init__(self,sync_data_pool,used_idx):
        # self.COLL_name = IMU_COLL_name
        self.idx = used_idx
        self.data = sync_data_pool
        self.acceleration = self.get_acceleration()
        self.gyro = self.get_gyro()
        self.angle = self.get_angle()

    # def get_cur_data(fifo_file_path):
    #     os.open(fifo_file_path,os.O_RDONLY)
    def print_cur_data(self):
        print(self.data)

    def get_acceleration(self):
        try:
            self.acceleration = self.data[self.idx][1:4]
            self.acceleration = map(float,self.acceleration)
            self.acceleration = list(self.acceleration)
        except Exception as e:
            print("ReadError: acc with " + str(self.idx))
            print(e)
            self.acceleration = (0, 0, 0)
        return self.acceleration

    def get_gyro(self):
        try:
            self.gyro = self.data[self.idx][4:7]
            self.gyro = map(float,self.gyro)
            self.gyro = list(self.gyro)
            self.gyro = np.divide(self.gyro,57.13)
        except Exception as e:
            print("ReadError: gyro with " + str(self.idx))
            print(e)
            self.gyro = (0, 0, 0)
        return self.gyro

    def get_angle(self):
        try:
            self.angle = self.data[self.idx][7:10]
            self.angle = map(float,self.angle)
            self.angle = list(self.angle)
        except Exception as e:
            print("ReadError: angle with " + str(self.idx))
            self.angle = (0, 0, 0)
        return self.angle
    
    def get_mag(self):
        try:
            self.mag = self.data[self.idx][10:13]
            self.mag = map(float,self.mag)
            self.mag = list(self.mag)
        except Exception as e:
            print("ReadError: mag with " + str(self.idx))
            self.mag = (0, 0, 0)
        return self.mag