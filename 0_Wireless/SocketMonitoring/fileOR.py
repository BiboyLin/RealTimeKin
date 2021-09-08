from test import IMU_0
from TestUDP import IMU_raw_data
import socket
import time
import os
import numpy as np
from datetime import datetime


def npy_file_OR(all_IMU_raw_data,cur_ID):
   
    # create folder using date and file_cnt
    now_time = datetime.date.today()
    fold_cnt = sum([os.path.isdir(listx) for listx in os.listdir("../data")])
    fold_name = now_time + fold_cnt
    data_save_path = "../data/" + fold_name
    print(data_save_path)
   
    try:
        os.makedirs(data_save_path) 
    except Exception as e:
        print(e)
    finally:
        print("Data Fold Created as" + fold_name)

    # create npy for all_recv_data for each IMU


def main():
    IMU_raw_data = np.zeros(10)
    cur_ID = IMU_0
