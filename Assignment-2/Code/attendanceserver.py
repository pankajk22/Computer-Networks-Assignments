import socket
import csv
import traceback
import threading

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def openfile(username):
    
    filename="attendance.csv"
    with open(filename,'r')as csvfile:
        csv_file = csv.reader(csvfile, delimiter=",")

        for row in csv_file:
            if(row[1]==username):
                attend=0
                for i in row :
                    if(i=="Done"):
                        attend=attend+1
                if((float(attend)/8.0)>=0.8):
                    return 1
                
    
    
    
ihost=socket.gethostname()
host=socket.gethostbyname(ihost)
iport=[]
hostfile="host.csv"
with open(hostfile,'r')as host_file:
    csv_hfile = csv.reader(host_file, delimiter=",")
    for row in csv_hfile:
        iport.append(row[1])
port=int(iport[5])
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
        username=str(conn.recv(1024),"utf-8")
        password=str(conn.recv(1024),"utf-8")
        res=openfile(username)
        if res==1:
            print("with priviledges")
            conn.send(bytes("1","utf-8"))
            conn.send(bytes("1","utf-8"))
        else:
            print("No priviledges")
            conn.send(bytes("2","utf-8"))
            conn.send(bytes("2","utf-8"))
            # print("sent.....")
                
        



# def checkusr(username):
#     if username in usrpass:
#         return 1
#     else:
#         print("Invalid Username")
#         return -1


# def checkpass(username,password):
#     if usrpass[username]==password:
#         return 1
#     else:
#         print("Invalid Password")
#         return -1


            
                
            
def main():
    socketbind()
    socketaccept()
    # count=0
    # while (count<6):
    #     new_thread=threading.Thread(target =socketaccept)
    #     new_thread.start()
    #     count=count+1
   
main()