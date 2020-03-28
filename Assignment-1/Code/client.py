import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("please enter name of the server and port number you want to connect")
def socketconnect():
    server_name=input()
    port=int(input())
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
                print("Valid Username \nPlease enter valid password:")
                password=input()
                s.send(str.encode(password))
                msg2=str(s.recv(1024),"utf-8")
                if msg2=="1":
                    print("Login Successfull!!")
                    s.close()
                    break
                    # conversation() 
                else:
                    print("Wrong Password--->Login Failed")
                    break
            else:
                print("Invalid Username !!! Try again")
                break    
        else:
            print("Connection not established please enter valid server and port number!!")
            socketconnect()
        

socketconnect()   
















