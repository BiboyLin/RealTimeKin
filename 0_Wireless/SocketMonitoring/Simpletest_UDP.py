import socket
import time
import os
import numpy as np
import sys

def main():
    socket_IP = '192.168.3.223'
    socket_port = 8081

    timeout_limit = 5 
    # 设置超时时间
    socket.setdefaulttimeout(timeout_limit)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    s.bind((socket_IP,socket_port))
    cnt =1
    while cnt<=10:
       rec = s.recv(1024)
       print(rec)
       cnt = cnt+1

    s.close()

if __name__ == "__main__":

    main()
