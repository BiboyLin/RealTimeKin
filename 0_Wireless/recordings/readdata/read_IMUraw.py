import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

nfile = 19
filepath = "/home/ubuntu/RealTimeKin/0_Wireless/recordings/IMUtest/"
filename = "raw_imu_" + str(nfile) + ".npy"
data = np.load(filepath+filename, mmap_mode='r')

x = range(data.shape[0])

sns.set()

plt.plot(x,data[:,0])

plt.show()