import socket
import os
from threading import Thread
from SocketServer import ThreadingMixIn
BUFFER_SIZE=30
TCP_IP='localhost'
TCP_PORT=6000
class ClientThread(Thread):
   def __init__(self,ip,port,sock):
       Thread.__init__(self)
       self.ip=ip
       self.port=port
       self.sock=sock
#       self.sock.setblocking(0)
       print("[+] New Server thread started for "+ip+": "+str(port))
   def run(self):
       s=""
       while 1:

           s=self.sock.recv(BUFFER_SIZE)
           print("s=",s)
           x=s.split(" ")
           print(x)
           if s== "quit":
                print("Client IP "+self.ip+" port "+str(self.port)+" has exited")
                self.sock.close()
                break
           elif x[0]=="put":
                   f=open(x[1]+"2",'wb')
                   self.sock.settimeout(0.5)
                   while 1:
                       try:
                        data=self.sock.recv(BUFFER_SIZE)
                        print("Data="+data)
                       except:
                        print("File upload success!")
                        f.close()
                        break
                       if not data:
                           print("File uploaded successfully")
                           f.close()
                           break
                       f.write(data)
                   self.sock.settimeout(None)
           elif x[0]=="get":
               try:
                   print("Inside get")
                   with open(x[1],'rb') as f:
                        print("File opened")
                        while 1:
                                data=f.read(BUFFER_SIZE)
                                self.sock.send(data)
                                if not data:
                                        #self.sock.send("eof")
                                        print("File sent fully")
                                        f.close()
                                        break
               except:
                   self.sock.send(x[1]+" : no such file")
st=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
st.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
st.bind((TCP_IP,TCP_PORT))
#st.settimeout(0.5)
#st.setblocking(0)
threads=[]
while 1:
   st.listen(4)
   print("Waiting for connections")
   (conn,(host,port))=st.accept()
   #conn.setblocking(0)
   print("Got connection from "+host+str(port))
   newthread=ClientThread(host,port,conn)
   newthread.start()
   threads.append(newthread)
for t in threads:
   t.join()
