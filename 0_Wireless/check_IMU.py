# Module to check the connection with all configured IMU
import socket
import time
import os
import numpy as np
import sys

# Function to read the setting file get the list of configured IMU and store the result into a dict IMU_used_dict
def read_setting_file(setting_filename):
    
    # open setting file and get all IMU ID and body part.
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

    # find the index of used IMU 
    used_sensor_ind_list = []
    sensor_flag = equip_flag[1:]
    for i, cur_flag in enumerate(sensor_flag):
        if cur_flag != '99':
            used_sensor_ind_list.append(i)
            num_used_sensor = len(used_sensor_ind_list)
            
    # Initialize the dict to store the IMU id used and their body part
    IMU_used_dict = {}

    print("Number of configured IMU: %i" %num_used_sensor)
    
    # Put the IMU id and corresponding body part into the dict
    for i in range(num_used_sensor):
        position_ind = used_sensor_ind_list[i]

        IMU_id = IMU_used_ID[position_ind]
        IMU_body_parts = body_parts[position_ind+1]

        IMU_used_dict[IMU_id] = IMU_body_parts

    print('Searching for these IMU:')
    print(IMU_used_dict)

    return IMU_used_dict

# deal the recived UDP data return the IMU id and acceleration
def deal_recv_data(recv_data,s_rate=200):
    
    # decode and cut the coming data
    str_recv_data = recv_data.decode('utf-8')
    
    # cut the data with ','
    cut_recv_data = str_recv_data.split(",",-1)
    mergeddata = cut_recv_data[0]
    
    # get IMU id
    IMU_id = mergeddata[0:14]
    
    # get acceleration x,y and z
    acc_x = mergeddata[14:-1]+mergeddata[-1]
    acc_y = cut_recv_data[1]
    acc_z = cut_recv_data[2]

    # store all the acceleration into a list
    IMU_acc = [acc_x,acc_y,acc_z]

    return IMU_id,IMU_acc

# check if all the IMU online, return 1 if all IMU online, 0 if there are some IMU offline
def check_IMU(setting_file_name):
    
    # get the dict of used IMU from setting file
    IMU_dict = read_setting_file(setting_file_name)
    
    # configure the socket ip and port
    socket_IP = '192.168.3.223'
    socket_port = 8081

    # set the maximum time out limit
    timeout_limit = 5 
    socket.setdefaulttimeout(timeout_limit)
    
    # initialize the socket s
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((socket_IP,socket_port))
    
    # recive a number of data and compare with the used IMU dict
    # if find an IMU, then delete it from the dict
    for i in range(50):
        
        try:
            recv_data = s.recv(1024)
        except Exception as e:
            print("No IMU online!")
            print(e)
            return 0
        
        [IMU_id,IMU_acc] = deal_recv_data(recv_data)
        if IMU_id in IMU_dict:
            print(IMU_id,IMU_acc)
            del IMU_dict[IMU_id]

    # if the are no key in the dict, it means that all IMU found
    if len(IMU_dict) == 0:
        print("All IMU online!")
        s.close()
        return 1
    else:
        print("These IMU not found:")
        print(IMU_dict)
        s.close()
        return 0
    s.close()

def main():
    check_IMU("/home/ubuntu/RealTimeKin/0_Wireless/test_settings/setting_paralle_rightleg.txt")

if __name__ == "__main__":

    main()
