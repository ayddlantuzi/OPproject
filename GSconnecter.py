from socket import socket,AF_INET,SOCK_STREAM

class GSconnection:
    def __init__(self,GSname,addr,family = AF_INET,type = SOCK_STREAM,BUFSIZ = 2048):
        '''
        连接GameServer 的client类
        :param addr:   tuple  (host,port)
        :param family:
        :param type:
        :param BUFSIZ:
        '''
        self.GSname = GSname
        self.addr = addr
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.BUFSIZ = BUFSIZ
        self.sock = None

    def connect(self):
        '''
        连接方法
        :return: True成功  False失败
        '''
        try:
            self.sock = socket(self.family,self.type)
            self.sock.connect(self.addr)
            return True
        except Exception as e:
            print(e)
            return False

    def close(self):
        try:
            self.sock.close()
            self.sock = None
        except Exception as e:
            print(e)

    def send(self,data):
        try:
            self.sock.send(data.encode())
            return True
        except Exception as e:
            print(e)
            return False

    def receive(self):
        try:
            data = self.sock.recv(self.BUFSIZ).decode()
            return data
        except Exception as e:
            print(e)

if __name__ == '__main__':

    HOST = '121.196.201.156'
    PORT = 21567
    addr = (HOST,PORT)
    a = GSconnection('game1',addr)
    b = GSconnection('game2',addr)
    c = GSconnection('game2',addr)

    listConn = [a,b,c]
    n = 0

    for conn in listConn:
        n += 1
        if conn.connect():
            conn.send(str(n))
        # print(conn.receive())
        # conn.close()

    # for conn in listConn:
    #     n += 1
    #     if conn.connect():
    #         conn.send(str(n))
    #     print(conn.receive())
    #     conn.close()


    # if a.connect():
    #     a.send('aaa')
    # print(a.receive())
    # a.close()