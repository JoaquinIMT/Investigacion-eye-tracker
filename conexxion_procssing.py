from socket import socket

m_socket = socket()
m_socket.bind(('localhost',5000))
m_socket.listen(5)

while True:
    conexion, addr = m_socket.accept()
    conexion.send("b")
    print("les gooo")
    print(addr)

    conexion.close()