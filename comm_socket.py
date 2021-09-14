#pip install python-socketio
#pip install eventlet
import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

"""import socket

m_socket = socket.socket()

m_socket.bind(('localhost',8001))
m_socket.listen(5)

while True:
    conexion, addr = m_socket.accept()
    print("les gooo")
    print(addr)
    conexion.send('12'.encode("ascii"))
    conexion.close()
"""