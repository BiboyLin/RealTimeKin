import numpy as np

curfile_num = 19
filepath = "/home/ubuntu/RealTimeKin/0_Wireless/recordings/IMUtest/"
filename = "raw_imu_" + str(curfile_num) + ".npy"
cur_imudata = np.load(filepath+filename, mmap_mode='r')

print(cur_imudata.shape)
imu_num = int(cur_imudata.shape[1]/6)
print("Number of IMU:"+ str(imu_num))

# for i in range(imu_num):
#     if i == 0:
#         k = i
#     else:
#         k = i*6 - 1
#     print(cur_imudata[:,k])

t_len = cur_imudata.shape[0]
print("time:" + str(t_len) + "   t_len = " + str(t_len))

# print(cur_imudata)

# for k in range(400):
#     for i in range(7):
#         print(cur_imudata[t_len-1-k,i*6:(i+1)*6])
#     print('\n')
# print(cur_imudata.shape)


