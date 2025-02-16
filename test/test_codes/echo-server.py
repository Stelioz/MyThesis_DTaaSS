import socket

HOST = '127.0.0.1' 
PORT = 8080

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("binding...")
        s.bind((HOST, PORT))
        print("listening...")
        s.listen()
        print("accepting...")
        conn, addr = s.accept()
        with conn:
            while True:
                print("receiving...")
                data = conn.recv(1024)
                print("received data", data)
                if not data:
                    break
                print("sending")
                conn.sendall(data)
        print("something happened, closing...")
        s.close()