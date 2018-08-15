import socket,logging,threading,time
from time import ctime
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(levelname)s-%(message)s')

HOST = ''
PORT = 5555
BUFSIZE = 1024

class Server():
    def __init__(self):
        self.ADDR = (HOST,PORT)
        try:
            self.serversocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serversocket.bind(self.ADDR)
            self.serversocket.listen(5)
            self.STOP_STAT =False
            self.clientsocket = {}
            self.thrs ={}
            self.stops = []
        except Exception as e:
            logging.debug(e)
            return False

    def listen_client(self):
        while not self.STOP_STAT:
            logging.debug("waiting for connecting......")
            self.clientsocket, self.addr = self.serversocket.accept()
            logging.debug("...connect from " + str(self.addr))
            address = self.addr
            self.clients[address]=self.clientsocket
            self.thrs[address] = threading.Thread(target=self.readmsg,arg=[address])
            self.thrs[address].start()
            time.sleep(0.5)

    def readmsg(self,address):
        if address not in self.clients:
            return False
        client = self.clients[address]
        while True:
            try:
                data = client.recv(BUFSIZE)
            except:
                logging.error("no data")
                self.close_client(address)
                break
            if not data:
                break
            logging.debug(str(address)+' send '+data)
            # # 将获得的消息分发给链接中的client socket
            # for k in self.clients:
            #     self.clients[k].send(s.encode('utf8'))
            #     self.clients[k].sendall('sendall:' + s.encode('utf8'))
            #     print str(k)
            # print [stime], ':', data.decode('utf8')
            # # 如果输入quit(忽略大小写),则程序退出
            # STOP_CHAT = (data.decode('utf8').upper() == "QUIT")
            # if STOP_CHAT:
            #     print "quit"
            #     self.close_client(address)
            #     print "already quit"
            #     break
            client.send(('[%s] %s' %(ctime(),data)).encode())

    def close_client(self,address):
        try:
            client = self.clients.pop(address)
            self.stops.append(address)
            client.close()
            for k in self.clients:
                self.clients[k].send(str(address) + u"已经离开了")
        except:
            pass
        logging.debug(str(address) + u'已经退出')

if __name__ =="__neme__":
    tserver = Server()
    tserver.listen_client()