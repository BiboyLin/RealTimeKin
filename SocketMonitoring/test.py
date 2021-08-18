import socket
import time
import os
import numpy as np
from numpy.lib import recfunctions
from datetime import datetime

IMU_data_structure = {'names':('ID','acc','gyro','mag','ang'),'formats':('S14','3f','3f','3f','3f')}
IMU_0 = np.array([("IMU",np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3))],dtype=IMU_data_structure)

IMU_1 = np.array([("IMU",np.ones(3),np.zeros(3),np.zeros(3),np.zeros(3))],dtype=IMU_data_structure)

app_nda = np.append(IMU_0,IMU_1)
# app_nda = np.lib.recfunctions.join_by(['ID','acc','gyro','ang','mag'],IMU_0,IMU_1,'outer')

print(app_nda['acc'])