import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("please enter name of the server and port number you want to connect")

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def socketconnect():
    server_name=input()
    port=int(input())
    s.connect((server_name,port))
    conversation()
    s.close()
def framesum(frame):
    ans= sum(bytearray(frame))
    ans=ans%1011
    return ans

def conversation():
    msg=str(s.recv(102400),"utf-8")
    if msg=="1":
        print("Connection is established successfully!! \nPlease enter the valid filename:")
        filename=input()
        f= open(filename,'rb')
        s.send(bytes(filename,"utf-8"))
        for piece in read_in_chunks(f):
            frame_sum=str(framesum(piece))
            print(frame_sum)
            piece=str(frame_sum)+str(piece)
            s.send(bytes(piece,"utf-8"))
        # s.send(bytes("stop","utf-8"))
        print("Succesfull!!")


socketconnect()   
















