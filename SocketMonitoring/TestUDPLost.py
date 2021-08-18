# def TestUDPLost(sm):

import socketserver
class Mysocket(socketserver.StreamRequestHandler): #重写setup和finish方法
    def handle(self):  #处理链接
        print("建立新连接，对方地址为：{}".format(self.client_address))
        while 1:
            data = self.request.recv(1024)
            self.request.send(data)
            print(data.decode())

if __name__ == '__main__':
    AddrPort = ('10.0.0.1',8081)
    server = socketserver.ThreadingTCPServer(AddrPort,Mysocket) #多线程创建实例链接
    print("Finish")
    # server.serve_forever()  #循环接收链接