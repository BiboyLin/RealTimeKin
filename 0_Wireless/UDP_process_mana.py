import socket
import time
import os
import numpy as np
import pandas as pd
import sys
import csv

global header_table,ele_num,fifo_file_path
savespace = '/home/ubuntu/RealTimeKin/0_Wireless/'
workspace = '/home/ubuntu/RealTimeKin/0_Wireless/SocketMonitoring'
# Interval_file_name = savespace + 'Interval_IMU_data.csv'
# fifo_file_path = '/tmp/fifo_imu'

sys.path.append(workspace)
from Release_socket import release_port


header_table = ['ID','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','ang_x','ang_y','ang_z','mag_x','mag_y','mag_z']
# header_format = 'str','f','f','f','f','f','f','f','f','f','f','f','f'
ele_num = len(header_table)

# 建class 尝试建立中间数据文件
def init_for_IMUdata(sync_data_pool,setting_filename):
    global IMU_data_structure
    IMU_data_structure = header_table

    init_IMUdata_coll = sync_data_pool

    # open setting file and get IMU ID
    with open(setting_filename, 'r') as f:
        for cnt, line in enumerate(f):
            if cnt == 0:
                body_parts = line.split(',')
                num_parts = len(body_parts)
            elif cnt == 1:
                equip_flag = line.split(',')
                if num_parts != len(equip_flag):
                    print("Wrong number of IMU_idx given, doesn't match number of body parts.")
                equip_flag = equip_flag[:-1]
            elif cnt == 7:
                IMU_used_ID = line.strip()
                IMU_used_ID = IMU_used_ID.split(',')
    f.close()

    # find the number of used_IMU 
    used_sensor_ind_list = []
    sensor_flag = equip_flag[1:]
    for i, cur_flag in enumerate(sensor_flag):
        if cur_flag != '99':
            used_sensor_ind_list.append(i)
            num_used_sensor_list = len(used_sensor_ind_list)
            
    # IMU dict:{IMU_IND:EQ_ID}
    global IMU_used_dict
    IMU_used_dict = {}

    # #  create fifo file
    # if os.path.exists(fifo_file_path):
    #     os.remove(fifo_file_path)

    # try:
    #     os.mkfifo(fifo_file_path)
    # except Exception as e:
    #     print(e)


    # global IMU_COLL_0,IMU_COLL_1,IMU_COLL_2,IMU_COLL_3
    # # Try to open/create .csv file to store the UDP recived data
    # with open(Interval_file_name,'w',encoding='utf8',newline='') as f:
    #     cw = csv.writer(f)
    #     cw.writerow(header_table)
    
    #     # create np struct array for each IMU
    #     for i in range(num_used_sensor_list):
    #         IMU_ID_name_str = IMU_used_ID[i]
    #         IMU_ID_name = IMU_ID_name_str
    #         # IMU_ID_name_int = int(IMU_ID_name_str[-5:])

    #         IMU_IND = str(i+1)
    #         # np_name = "IMU_COLL_" + IMU_IND
            
    #         cur_init_list = [0]* ele_num
    #         cur_init_list[0] = IMU_ID_name

    #         written_data = cur_init_list
    #         # written_data = str(cur_init_list)
            
    #         cw.writerow(written_data)
    #         print(written_data)

    #         cur_dict = {IMU_ID_name:IMU_IND}
    #         IMU_used_dict.update(cur_dict)
    # f.close()

    for i in range(num_used_sensor_list):
        IMU_ID_name_str = IMU_used_ID[i]
        IMU_ID_name = IMU_ID_name_str
        # IMU_ID_name_int = int(IMU_ID_name_str[-5:])

        IMU_IND = str(i+1)
        # np_name = "IMU_COLL_" + IMU_IND
        
        cur_init_list = [0]* ele_num
        cur_init_list[0] = IMU_ID_name

        init_IMUdata_coll.append(cur_init_list)

        # written_data = cur_init_list
        # # written_data = str(cur_init_list)
        
        # print(written_data)

        cur_dict = {IMU_ID_name:IMU_IND}
        IMU_used_dict.update(cur_dict)

    print('Init for the following IMU data array structure is done:')
    print(IMU_used_dict)
    print(init_IMUdata_coll)

    return init_IMUdata_coll
    

def recv_data_deal(recv_data,s_rate=200):
    # decode and cut the coming data in btyes 
    str_recv_data = recv_data.decode('utf-8')
    # print(str_recv_data)
    cut_recv_data = str_recv_data.split(",",-1)
    mergeddata = cut_recv_data[0]
    
    # 实例化当前IMU类
    # cur_IMU_raw_data = IMU_raw_data()
    # 赋予类数据
    cur_ID = mergeddata[0:14]
    # acc
    acc_x = mergeddata[14:-1]+mergeddata[-1]
    acc_y = cut_recv_data[1]
    acc_z = cut_recv_data[2]
    # gyro
    gyro_x = cut_recv_data[3]
    gyro_y = cut_recv_data[4]
    gyro_z = cut_recv_data[5]
    # angle
    ang_x = cut_recv_data[6]
    ang_y = cut_recv_data[7]
    ang_z = cut_recv_data[8]
    # mag
    mag_x = cut_recv_data[9]
    mag_y = cut_recv_data[10]
    mag_z = cut_recv_data[11]

    acc = [acc_x,acc_y,acc_z]
    gyro = [gyro_x,gyro_y,gyro_z]
    ang = [ang_x,ang_y,ang_z]
    mag = [mag_x,mag_y,mag_z]
    
    cur_IMU_raw_data = [cur_ID] + acc + gyro + ang + mag

    # print (cur_IMU_raw_data)
    return cur_ID,cur_IMU_raw_data

def Match_update(cur_ID,cur_IMU_raw_data,newest_IMUdata_coll):

    Inter_var_idx = int(IMU_used_dict[cur_ID])
    # print(Inter_var_idx)

    newest_IMUdata_coll[Inter_var_idx-1] = cur_IMU_raw_data

    # print(newest_IMUdata_coll)
    return newest_IMUdata_coll
    # try:
    #     with open(Interval_file_name,'rw',encoding='utf8',newline='') as f:
    #         reader = csv.DictReader(f)
    #         for line in reader:
    #             for line in reader[1:]:
    #                 line_res_ID = line.split(',')[0]
    #                 # dealed_line_res_ID = line_res_ID.replace('[','').strip('\'')
    #                 # print(dealed_line_res_ID)

    #                 if cur_ID == dealed_line_res_ID:
    #                     lines[Inter_file_line_idx] = cur_IMU_raw_data
    #                 else:
    #                     print("Can't write data, cos' cur ID can't be found")
    #             f.write(lines)
    # except Exception as e:
    #     print(e)
    # finally:
    #     if f:
    #         f.close()
    
    # print("After"+ cor_np_name)
    # print(globals()[cor_np_name])



def UDP_process(sync_data_pool,setting_file_name):
    init_IMUdata_coll = init_for_IMUdata(sync_data_pool,setting_file_name)

    # socket_list = [8080,8081]
    socket_IP = '192.168.3.223'
    socket_port = 8081
    release_port(socket_port)

    time.sleep(0.5)
    # 设置超时时间
    timeout_limit = 5 
    socket.setdefaulttimeout(timeout_limit)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    s.bind((socket_IP,socket_port))

    cnt = 0
    Atime = time.time()
    Dtime_all = []

    # wf = open(fifo_file_path,os.O_WRONLY)
    
    newest_IMUdata_coll = init_IMUdata_coll

    # time.sleep(2)
    print("----------------UDP Start Reciving----------------")

    while True:
    # while cnt<=400:
        Stime = time.time()
        # recv_data = 0
        try:
            recv_data = s.recv(1024)

            # if recv_data != 0:
            # 接收并处理数据
            Btime = time.time()
            cur_ID,dealed_data = recv_data_deal(recv_data,200)
            
            # print(dealed_data)
            # 写入fifo文件
            # wf.write(dealed_data + "/n")
            # print(dealed_data)
            # 更新变量
            newest_IMUdata_coll = Match_update(cur_ID,dealed_data,newest_IMUdata_coll)
            
            # # 计算用时和速度
            # Etime = time.time()
            # d = Etime-Btime
            # # print("Recive and match cost: %f" %d)

            # # Record time cost
            # Etime = time.time()
            # Dtime = Etime - Stime
            # # print("Dealing rate = " + str(1/Dtime))
            # # print("Cost time = " + str(Dtime))
            # Dtime_all.append(Dtime)
            # cnt = cnt + 1
            
        except Exception as e:
            s.close()
            print("No data Reciving!")
            print(e)
            cnt = cnt + 1

    Btime = time.time()
                

    print("Total time cost = %f" %(Btime-Atime))
    print("Single recive time cost = %f" %np.mean(Dtime_all))
    print("Mean dealing sample rate = %f" %(1/np.mean(Dtime_all)))

    print(newest_IMUdata_coll)
    
    time.sleep(1)
    s.close()


if __name__ == "__main__":
    sync_data_pool = []
    UDP_process(sync_data_pool,'/home/ubuntu/RealTimeKin/0_Wireless/0_settings_test.txt')