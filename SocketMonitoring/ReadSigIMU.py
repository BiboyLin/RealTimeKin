from socketserver import BaseRequestHandler, ThreadingUDPServer
import socketserver
import threading
import numpy

import time
import os
# from AUKF_filter import AUKF

global all_recv_data

def recv_data_deal(recv_data,s_rate):
    # 切分当前数据
    cut_recv_data = recv_data.split(str=",",num=-1)


def npy_file_OR(recv_data,file_name):
    # open raw_data recording create 

BUF_size = 1024
IMUIP='10.0.0.1'
IMU_port_list = [8080,8081]


# class IMU_raw_data:
    # b'WT5300001183030.134,-0.021,0.956,0.000,0.000,0.000,-1.279,-7.998,-55.777,-196,132,13,44.76,4.20,-47,13004,0\r\n'
    # b'WT5300001183 03 [0.134,-0.021,0.956],[0.000,0.000,0.000],[-1.279,-7.998,-55.777],[-196,132,13],[44.76,4.20,-47,13004],0\r\n'
    # ID编号格式：WT + 型号 + 编号；
    # 加速度X	-0.102
    # 加速度Y	-0.442
    # 加速度Z	1.110

    # 角速度X	0.000
    # 角速度Y	0.000
    # 角速度Z	0.000

    # 角度X	-21.720
    # 角度Y	5.729
    # 角度Z	96.301

    # 磁场X	71
    # 磁场Y	5
    # 磁场Z	-34

    # 温度	-56.3 单位：℃
    # 电量	50
    # 信号	-063
    # 版本号	0.16211
    # 报警信号	0
    # 结束符 \r\n
    # acc = 



# def ReadSigIMU(IMUIP='10.0.0.1',IMUport,sm):
#     s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     s.bind((IMUIP,IMUport))

#     while True:
#         recv_data = s.recvfrom(1024)
#         # print(recv_data.type)

class MyUDP_IMUreader(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        # while True:
        recv_data = conn.recv(BUF_size)
        print(recv_data)
            # print(recv_data)



def ini_IMUreader(IMU_port,Server_dir,cur_server_name):
    try:
        Server_dir[cur_server_name] = socketserver.ThreadingUDPServer((IMUIP,IMU_port),MyUDP_IMUreader)
        print("Success to init IMU_reader for IMU_" + str(IMU_port) )
        
    except Exception as e:
        print("Failed to init IMU_reader for IMU_" + str(IMU_port) )
        print(e)


def main():
    IMU_num = 1
    Server_dir = {}
    print("Start Initialization...")

    # Init the Server
    for i in range(IMU_num):
        IMU_ind = i
        cur_server_name = "IMUreader_" + str(IMU_ind)
        ini_IMUreader(IMU_port_list[i],Server_dir,cur_server_name)

    print(Server_dir)

    # Protect the Server Threadings   
    for i in range(IMU_num):
        IMU_ind = i
        cur_server_name = "IMUreader_" + str(IMU_ind)
        Server_dir[cur_server_name].serve_forever()


if __name__ == "__main__":
    main()