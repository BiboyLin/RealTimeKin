# -*- coding: utf-8 -*-
"""
@ auth : Bobby
@ time : 2020-7-7
"""

import os
def release_port(port):
    #查找端口对应的pid :
    #  lsof -i:8081
    cmd_find = 'lsof -i:%s' %port
    # print(cmd_find)
    #返回命令执行结果
    result = os.popen(cmd_find).read()
    # print(result)

    if str(port) and 'python3' in result:
        #获取端口对应的pid进程
        # COMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
        #python3 7282 ubuntu    3u  IPv4 225705      0t0  UDP ubuntu:8081 
        start = result.index('\n') + len('python3 ') 
        end = result.index('ubuntu  ')
        pid = result[start:end].strip()
        print(port)
        print(pid)
        print('port %s is used by process %s ' %(port,pid))

        #关闭被占用端口的pid
        cmd_kill = 'kill -9 %s' %pid
        # print(cmd_kill)
        os.popen(cmd_kill)
        print('port %s is released!!!' %port)
    else:
        print('port %s is available !' %port)

if __name__ == '__main__':
    host = '10.42.0.1'
    port = 8081
    release_port(port)