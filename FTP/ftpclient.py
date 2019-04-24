import socket
import os
BUFFER_SIZE=30
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
st=raw_input()
x=st.split(" ")
data=""
if x[0]=="myftp":
   s.connect((x[1],int(x[2])))
#   s.setblocking(0)
   s.settimeout(0.5)
   while 1:
       st=raw_input("ftp> ")
       s.send(st)
       x=st.split(" ")
       if st=="quit":
           s.close()
           break
       elif x[0]=="put":
           try:
               f=open(x[1],'rb')
               while 1:
                   data=f.read(BUFFER_SIZE)
                   s.send(data)
                   if not data:
                       f.close()
                       break
           except:
               print(x[1]+": no such file")
       elif x[0]=="get":
           f=open(x[1]+"2",'wb')
           print("Inside get")
           while 1:
               print("Inside loop")
               try:
                        data=s.recv(BUFFER_SIZE)
               except:
                        f.close()
                        break
               #except:
                #  pass
 #                  f.close()
  #                 break
               print("Data="+data)
               if data.startswith(x[1]):
                   print(data)
                   f.close()
                   break
               if not data:
                   f.close()
                   break
               f.write(data)