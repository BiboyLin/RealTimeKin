import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

filepath = "/home/ubuntu/RealTimeKin/0_Wireless/calibration/gyro_offsets.npy"
data = np.load(filepath, mmap_mode='r')

x = range(data.shape[0])

print(data)