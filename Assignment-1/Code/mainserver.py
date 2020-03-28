import socket
import csv
import traceback
import threading
import random

socketlist=[]
s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketlist.append(s1)
s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketlist.append(s2)
s3=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketlist.append(s3)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
att=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ihost=socket.gethostname()
host=socket.gethostbyname(ihost)
iport=[]
ip=[]
hostfile="host.csv"
with open(hostfile,'r')as host_file:
    csv_hfile = csv.reader(host_file, delimiter=",")
    for row in csv_hfile:
        iport.append(row[1])
        ip.append(row[2])

i=0
while(i<3):
    port=int(iport[i+2])
    i_p=ip[i+2]
    socketlist[i].connect((i_p,port))
    i=i+1

usrpass={}
total=0
def openfile():
    
    filename="login_credentials.csv"
    with open(filename,'r')as csvfile:
        csv_file = csv.reader(csvfile, delimiter=",")
        for col in csv_file:
            usrpass[col[0]]=col[1]
    usrpass.pop("Username")
    total=len(usrpass)
    #print(usrpass)
    

port=int(iport[5])
i_p=ip[5]
att.connect((i_p,port))   
ihost=socket.gethostname()
host=socket.gethostbyname(ihost)
port=int(iport[1])
def socketbind():

    try:
        s.bind(('',port))
        print("Bind with host at port number : "+str(port))
        s.listen(10)
        print("Socket is listening!!")

    except socket.error as msg:
        print("Error in Binding: "+ str(msg)+"\n Retrying....")
        socketbind()

def socketaccept():
    conn,add=s.accept()
    print("connection is established with IP : "+str(add[0])+" and Port Number : "+str(add[1]))
    conn.send(bytes("1","utf-8"))
    conversation(conn)
    conn.close()

def conversation(conn):
    while True:
        #conn.send(bytes("Send Username please:","utf-8"))
        username=str(conn.recv(1024),"utf-8")
        print("Username Recieved!!")
        conn.send(bytes("1","utf-8"))
        password=str(conn.recv(1024),"utf-8")
        part=total/3
        flag=0
        servernum=-1
        for n in range(0,22):
            if(username==list(usrpass)[n]):
                servernum=1
                flag=1
        if(flag==0):
            for n in range(22,44):
                if(username==list(usrpass)[n]):
                    servernum=2
                    flag=1
        if(flag==0):
            for n in range(44,67):
                if(username==list(usrpass)[n]):
                    servernum=3
        
                    
        if(servernum==-1):
            conn.send(bytes("-1","utf-8"))
            print("Invalid Username--->Login Failed!!")
            conn.close()
            print("Connection is closed!!")
            print("Socket is Listening")
            socketaccept()
        else:
            
            res=int(checkpass(username,password,servernum))
            if res==1:
                priv=int(checkattendance(username,password))
                print("Login Successfull!!")
                if(priv==1):
                    print("with priviledges")
                    conn.send(bytes("1","utf-8"))
                else:
                    print("with no priviledges")
                    conn.send(bytes("2","utf-8"))
                conn.close()
                print("Connection is closed!!")
                print("Socket is Listening")
                socketaccept()
                #socketaccept()
            else:
                conn.send(bytes("-1","utf-8"))
                print("Invalid Password--->Login Failed")
                conn.close()
                print("Connection is closed!!")
                print("Socket is Listening")
                socketaccept()

        
            
            
            
            
        
    



# def checkusr(username,i):

#     socketlist[i-1].send(str.encode(username))
#     message=str(socketlist[i].recv(1024),"utf-8")
#     return message

        
        


def checkpass(username,password,i):
    socketlist[i-1].send(str.encode(username))
    socketlist[i-1].send(str.encode(password))
    message=str(socketlist[i-1].recv(1024),"utf-8")
    message=str(socketlist[i-1].recv(1024),"utf-8")
    return message

def checkattendance(username,password):
    att.send(str.encode(username))
    att.send(str.encode(password))
    message=str(att.recv(1024),"utf-8")
    # print("recieved...."+message)
    message=str(att.recv(1024),"utf-8")
    # print("recieved...."+message)
    return message
            
                
            
def main():
    openfile()
    socketbind()
    # socketaccept()
    count=0
    while (count<6):
        new_thread=threading.Thread(target =socketaccept)
        new_thread.start()
        count=count+1
   
main()