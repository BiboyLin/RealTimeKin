import numpy as np

curfile_num = 21
filename = "raw_imu_" + str(curfile_num) + ".npy"
cur_imudata = np.load(filename)

# print(cur_imudata.shape[1])
imu_num = int(cur_imudata.shape[1]/6)
print("Number of IMU:"+ str(imu_num))

for i in range(imu_num):
    if i == 0:
        k = i
    else:
        k = i*6 - 1
    print(cur_imudata[:,k])


print(cur_imudata[10,24:30])
print(cur_imudata[10,41:47])
print(cur_imudata.shape)
