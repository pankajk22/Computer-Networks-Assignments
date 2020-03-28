import socket
import csv

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def socketconnect():
    # server_name="172.21.15.43"
    iport=[]
    ip=[]
    hostfile="host.csv"
    with open(hostfile,'r')as host_file:
        csv_hfile = csv.reader(host_file, delimiter=",")
        for row in csv_hfile:
            iport.append(row[1])
            ip.append(row[2])
    port=int(iport[1])
    server_name=ip[1]
    s.connect((server_name,port))
    conversation()
    s.close()

def conversation():
    while True:
        msg=str(s.recv(1024),"utf-8")
        if msg=="1":
            print("Connection is established successfully!! \nPlease enter the valid username:")
            username=input()
            s.send(str.encode(username))
            msg1=str(s.recv(1024),"utf-8")
            if msg1=="1":
                print("Username Forwarded to server ...Please enter valid password:")
                password=input()
                s.send(str.encode(password))
                msg2=str(s.recv(1024),"utf-8")
                if msg2=="1":
                    print("Login Successfull!! with extra priviledges")
                    s.close()
                    break
                    # conversation() 
                if msg2=="2":
                    print("Login Successfull!! with no priviledges")
                    s.close()
                    break
                    # conversation() 
                if msg2=="-1":
                    print("Login Failed")
                    s.close()
                    break
                    # conversation() 
                
                    
            else:
                print("Username not forwarded please Try again")
                break    
        else:
            print("Connection not established please enter valid server and port number!!")
            socketconnect()
        

socketconnect()   
















