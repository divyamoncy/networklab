import socket
import sys
import datetime
UDP_IP="127.0.0.1"
UDP_PORT=12000
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(2)   #setting the timeout
message=""        
x=[]                 #list to store the roundtrip times
losscount=0
for i in range(1,11):
        sendtime=datetime.datetime.now().time().microsecond #getting the sending time
        message="Ping "+str(i)+" "+str(sendtime)           
        sock.sendto(message,(UDP_IP,UDP_PORT))              #sending the packet
        try:
                (res,(ip,port))=sock.recvfrom(len(message)) #receiving the packet
                rectime=datetime.datetime.now().time().microsecond-sendtime  #calculating roundtrip time
                print("from "+str(ip)+": time="+str(rectime))
                x.append(rectime)  #adding roundtrip time to list
        except:
                losscount+=1  #updating lost packet count
                print(str(i)+": Timed out")
min=x[0]
max=x[0]
sum=x[0]
for j in range(1,len(x)):
        if x[j]<min:
           min=x[j]
        if x[j]>max:
           max=x[j]
        sum+=x[j]
print("min="+str(min)+", max="+str(max)+", avg="+str(sum/len(x))) #calculating minimum, maximum and average
print("Package loss rate= "+str(losscount*100.0/10)) #calculating packet loss rate
sock.close()