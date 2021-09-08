import os
import re
 
port = 8081
def kill_process():
        ret = os.popen("netstat -nao|findstr " + str(port))
        #注意解码方式和cmd要相同，即为"gbk"，否则输出乱码
        # str_list = ret.read().decode('gbk')
        str_list = ret.read()
        ret_list = re.split('',str_list)
        try:
                process_pid = list(ret_list[0].split())[-1]
                os.popen('taskkill /pid ' + str(process_pid) + ' /F')
                print("端口已被释放")
        except:
                print("端口未被使用")

if __name__ == '__main__':
        kill_process()