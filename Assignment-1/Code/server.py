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
print("Please Enter the port number you want to listen to:")
port=int(input())
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
        if (len(username)<=0):
            print("Invalid Username")
            #conn.send(bytes("Invalid Username!!! \n Enter a valid username","utf-8"))
            conn.send(bytes("-1","utf-8"))

        else: 
            result=int(checkusr(username))
            if result==1:
                print("Valid Username")
                conn.send(bytes("1","utf-8"))
                password=str(conn.recv(1024),"utf-8")
                res=checkpass(username,password)
                if res==1:
                    print("Valid Password!")
                    conn.send(bytes("1","utf-8"))
                    conn.close()
                    print("Connection is closed!!")
                    print("Socket is Listening")
                    socketaccept()
                    #socketaccept()
                else:
                    conn.send(bytes("-1","utf-8"))
                    conn.close()
                    print("Connection is closed!!")
                    print("Socket is Listening")
                    socketaccept()
            else:
                conn.send(bytes("-1","utf-8"))
                conn.close()
                print("Connection is closed!!")
                print("Socket is Listening")
                socketaccept()
        



def checkusr(username):
    if username in usrpass:
        return 1
    else:
        print("Invalid Username")
        return -1


def checkpass(username,password):
    if usrpass[username]==password:
        return 1
    else:
        print("Invalid Password")
        return -1


            
                
            
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