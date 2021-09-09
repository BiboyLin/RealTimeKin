import socket
import time
import os
import numpy as np

from Release_socket import release_port
# class IMU_raw_data():
#     def __init__(self) -> None:
#         self = np.array([("IMU_ID_name",np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3))],dtype=IMU_data_structure)
#         # self.ID = []
        # self.acc = []
        # self.gyro = []
        # self.mag = []
        # self.ang = []

# class IMU_saved_data():
#     def __init__(self,cur_ID):
#         self.ID = cur_ID
#         self.acc = np.zeros(3)
#         self.gyro = []
#         self.mag = []
#         self.ang = []

def init_for_IMUdata(setting_filename):
    global IMU_data_structure
    IMU_data_structure = {'names':('ID','acc','gyro','mag','ang'),'formats':('S14','3f','3f','3f','3f')}
    # open setting file and get IMU ID
    with open(setting_filename, 'r') as f:
        for cnt, line in enumerate(f):
            if cnt == 7 :
                IMU_used_ID = line.replace('\n','').split(r',')
                IMU_used_num = len(IMU_used_ID)
            elif cnt == 8 :
                Body_part = line.split(',')
                Body_num = len(Body_part)
    f.close()

    # IMU dict:{IMU_IND:IMU_ID}
    global IMU_dict
    IMU_dict = {}
    
    global IMU_COLL_0,IMU_COLL_1,IMU_COLL_2,IMU_COLL_3

    # create np struct array for each IMU
    
    for i in range(IMU_used_num):
        IMU_ID_name = IMU_used_ID[i]
        IMU_IND = str(i)

        # IMU_data_structure = {'names':('ID','acc','gyro','mag','ang'),'formats':('S14','3f','3f','3f','3f')}
        np_name = "IMU_COLL_" + IMU_IND
        
        globals()[np_name]= np.array([(IMU_ID_name,np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3))],dtype=IMU_data_structure)

        cur_dict = {IMU_ID_name:np_name}
        IMU_dict.update(cur_dict)

    print('Init for the following IMU data array is done:')
    print(IMU_dict)
    

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
    acc_x = mergeddata[15:-1]
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
    
    cur_IMU_raw_data_ndarray = np.array([(cur_ID,acc,gyro,ang,mag)],dtype=IMU_data_structure)

    return cur_ID,cur_IMU_raw_data_ndarray

def Match_update(cur_ID,cur_IMU_raw_data):
    # Match
    cor_np_name = IMU_dict[cur_ID]
    # print("Before " + cor_np_name )
    # print(globals()[cor_np_name])

    # update array
    
    globals()[cor_np_name] = np.append(globals()[cor_np_name],cur_IMU_raw_data)

    # print("After"+ cor_np_name)
    # print(globals()[cor_np_name])


def main():
    init_for_IMUdata('/home/ubuntu/RealTimeKin/0_Wireless/SocketMonitoring/IMU_settings_test.txt')

    # socket_list = [8080,8081]
    socket_IP = '127.0.0.1'
    socket_port = 8081
    release_port(socket_port)

    timeout_limit = 5 
    # 设置超时时间
    socket.setdefaulttimeout(timeout_limit)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    s.bind((socket_IP,socket_port))

    cnt = 0
    Atime = time.time()
    Dtime_all = []

    while cnt<=2000:
        Stime = time.time()
        # recv_data = 0
        try:
            recv_data = s.recv(1024)
    
            # if recv_data != 0:
            # 接收并处理数据
            cur_ID,dealed_data = recv_data_deal(recv_data,200)
            # 匹配ID并放入数组
            Match_update(cur_ID,dealed_data)

            # print(cur_ID)

            # Record time cost
            Etime = time.time()
            Dtime = Etime - Stime
            # print("Dealing rate = " + str(1/Dtime))
            # print("Cost time = " + str(Dtime))
            Dtime_all.append(Dtime)
            cnt = cnt + 1
            
        except Exception as e:
            
            s.close()
            print("No data Reciving!")
            print(e)
            break
            # cnt = cnt + 1

    Btime = time.time()

    print("Recived data = %u from IMU_COLL_0" % (IMU_COLL_0['acc'].shape[0]-1))
    print("Recived data = %u from IMU_COLL_1" % (IMU_COLL_1['acc'].shape[0]-1))

    print("Total time cost = %f" %(Btime-Atime))
    print("Single recive time cost = %f" %np.mean(Dtime_all))
    print("Mean dealing sample rate = %f" %(1/np.mean(Dtime_all)))


    s.close()

if __name__ == "__main__":

    main()

# def npy_file_OR(IMU_raw_data,cur_ID):
#     now_time = datetime.date.today()
#     # open raw_data recording create 
#     # create folder using date and file_cnt
#     fold_cnt = sum([os.path.isdir(listx) for listx in os.listdir("../")])
#     fold_name = now_time + fold_cnt
#    print
#     try:
#         os.makedirs("../fold_name") 