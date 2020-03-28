import socket
import csv
import time
s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
iport=[]
ip=[]

def socketconnect():
    # server_name="172.21.15.43"
    
    hostfile="host.csv"
    with open(hostfile,'r')as host_file:
        csv_hfile = csv.reader(host_file, delimiter=",")
        for row in csv_hfile:
            iport.append(row[1])
            ip.append(row[2])
    port1=int(iport[1])
    server_name1=ip[1]
    
    s1.connect((server_name1,port1))
    
    conversation()
    s1.close()

def conversation():
    while True:
        msg=str(s1.recv(1024),"utf-8")
        if msg=="1":
            print("Connection is established successfully!! \nPlease enter the valid username:")
            username=input()
            s1.send(str.encode(username))
            msg1=str(s1.recv(1024),"utf-8")
            if msg1=="1":
                print("Username Forwarded to server ...Please enter valid password:")
                password=input()
                s1.send(str.encode(password))
                msg2=str(s1.recv(1024),"utf-8")
                if msg2=="1":
                    print("Login Successfull!! ")
                    port2=int(iport[6])
                    server_name2=ip[6]
                    s2.connect((server_name2,port2))
                    s2.send(bytes(username,"utf-8"))
                    sendfile()
                    s1.close()
                    s2.close()
                    break
                    # conversation()  
                if msg2=="-1":
                    print("Login Failed")
                    s1.close()
                    break
                    # conversation() 
                
                    
            else:
                print("Username not forwarded please Try again")
                break    
        else:
            print("Connection not established please enter valid server and port number!!")
            socketconnect()

def sendfile():
    i=0
    print("Connection is established successfully!! \nPlease enter the valid filename:")
    ifilename=input()
    print("enter the value of p suck that 1/p frames are corrupted(default value:10)")
    prob=int(input())
    f= open(ifilename,'rb')
    s1.send(bytes(ifilename,"utf-8"))
    s2.send(bytes(ifilename,"utf-8"))
    
    for piece in read_in_chunks(f):
        # print(piece)
        data=bytes.decode(piece)
        idata=bytes(data,"utf-8")
        frame_sum=str(framesum(idata,i,prob))+"!@#$%^&*()"
        # print(frame_sum)
        piece=str(frame_sum)+data
        # print("p-->>>"+str(prob)+"  i-->>"+str(i))
        
        if i%2==0:
            print("data send to main server!")
            s1.send(bytes(piece,"utf-8"))
            # s1.send(piece)
            conf=str(s1.recv(1024),"utf-8")
            if conf=="-1":
                print("waiting for acknowldgement!!!!")
            else:
                print("frame sent successfully!!!")
                print("checking for verification!!")
                verifier=str(s1.recv(1024),"utf-8")
                # print(verifier)
                if i%prob==0:
                    print("Sum not matched-->> Resending the frame!")
                    time.sleep(0.1)
                   
                if verifier=="resend the frame!!!":
                    print("Sum matched -->> Verified!")
                    
        

        else:
            print("data send to helper server!")
            s2.send(bytes(piece,"utf-8"))
            # s2.send(piece)
            conf=str(s2.recv(1024),"utf-8")
            if conf=="-1":
                print("waiting for acknowldgement!!!!")
            else:
                print("frame sent successfully!!!")
                print("checking for verification!!")
                verifier=str(s2.recv(1024),"utf-8")
                # print(verifier)
                if i%prob==0:
                    print("Sum not matched-->> Resending the frame!")
                    time.sleep(0.1)
                   
                if verifier=="resend the frame!!!":
                    print("Sum matched -->> Verified!")
        

        print("delaying by 0.5 seconds")
        time.sleep(0.5)
        i=i+1
    s1.send(bytes('stop',"utf-8"))
    s2.send(bytes('stop',"utf-8"))
    print("Stop signal send successfully!!")
    # conf=str(s.recv(1024),"utf-8")
    print("File Transmission Succesfull!!")
        
def read_in_chunks(file_object, chunk_size=10240):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def framesum(frame,i,prob):
    # data=bytes(frame,"utf-8")
    # print("i-->>"+str(i))
    ans= sum(bytearray(frame))
    ans=ans%1011
    if i%prob==0:
        return ans+5
    else:
        return ans
    

socketconnect()   
















