import socket
import csv
import traceback
import threading

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
usrpass={}
def openfile():
    
    filename="login_credentials.csv"
    with open(filename,'r')as csvfile:
        csv_file = csv.reader(csvfile, delimiter=",")
        for col in csv_file:
            usrpass[col[0]]=col[1]
    usrpass.pop("Username")
    #print(usrpass)
    
    
ihost=socket.gethostname()
host=socket.gethostbyname(ihost)
iport=[]
hostfile="host.csv"
with open(hostfile,'r')as host_file:
    csv_hfile = csv.reader(host_file, delimiter=",")
    for row in csv_hfile:
        iport.append(row[1])
port=int(iport[2])
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
        servertype=str(conn.recv(1024),"utf-8")
        if(servertype=='main'):
            username=str(conn.recv(1024),"utf-8")
            password=str(conn.recv(1024),"utf-8")
            res=checkpass(username,password)
            if res==1:
                print("Valid Password!")
                conn.send(bytes("1","utf-8"))
                conn.send(bytes("1","utf-8"))
                socketfileaccpet(conn)
            else:
                conn.send(bytes("-1","utf-8"))
                conn.send(bytes("-1","utf-8"))
        if(servertype=='helper'):
            socketfileaccpet(conn)    
        



# def checkusr(username):
#     if username in usrpass:
#         return 1
#     else:
#         print("Invalid Username")
#         return -1


def checkpass(username,password):
    if usrpass[username]==password:
        return 1
    else:
        print("Invalid Password")
        return -1

def iframesum(frame):
    # data=bytes(frame,"utf-8")
    ans= sum(bytearray(frame))
    ans=ans%1011
    return ans
            
                
            
def main():
    openfile()
    socketbind()
    # socketaccept()
    count=0
    while (count<6):
        new_thread=threading.Thread(target =socketaccept)
        new_thread.start()
        count=count+1

def socketfileaccpet(conn):
    filename=str(conn.recv(102400),"utf-8")
    filename="server-1"+filename
    file=open(filename,'ab')
    i=0
    print("Opening File!!!")
    while True:
        # check=str(conn.recv(1024),"utf-8")
        # print(check)
        # if(check=='-1'):
        #     break
        
        filedata=conn.recv(102400)
        # print("recieved!!!!")
        # conn.send(bytes("1","utf-8"))
        # print("recieving!!")
        # print(filedata)
        if filedata==b'stop':
            # conn.send(bytes("1","utf-8"))
            # conn.send(bytes("1","utf-8"))
            print("Closing file!!!")
            file.close()
            break
        else:
            conn.send(bytes("1","utf-8"))
            ifiledata=str(filedata,"utf-8")
            framesum,data=ifiledata.split('!@#$%^&*()',1)
            # print(framesum)
            print(data)
            frame=bytes(data,"utf-8")
            checksum=str(iframesum(frame))
            if(framesum==checksum):
                conn.send(bytes("sumverified","utf-8"))
                file.write(frame)
            else:
                conn.send(bytes("resend the frame!!!","utf-8"))
                file.write(frame)
            # print("framesum:"+framesum+"    checksum:"+checksum)
            # print(filedata)
            # write=bytes(filedata,"utf-8")
            
            # i=i+1

    
    print("File transmission successfull!!")
   
main()