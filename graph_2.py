import cv2
import socket
import numpy as np
import time
from matplotlib import pyplot as plt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def show_img(img, name='my image'):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#Iteración 3
def detect_eyes(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = classifier.detectMultiScale(gray_frame, 1.07, 3) # detect eyes
    width = np.size(img, 1) # get face frame width
    height = np.size(img, 0) # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]
    return left_eye, right_eye

def detect_faces(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = classifier.detectMultiScale(gray_frame, 1.3, 5)
    x,y = 0,0
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None, None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
    return frame, (y, x)

def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 5)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
    return img

def blob_process(img, detector):
    _, img = cv2.threshold(img, 42, 250, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=5)
    img = cv2.dilate(img, None, iterations=6)
    img = cv2.medianBlur(img, 7)
    keypoints = detector.detect(img)
    return keypoints

def my_testing(keypoints,img):
    if len(keypoints)>0:
        print("========pausa eye:",img.shape)
        kp_coordinate = (0,0)
        kp_size = 0
        for kp in keypoints:
            if kp.size > kp_size:
                kp_size = kp.size
                kp_coordinate = kp.pt
        print("=================Size:",kp_size)
        print("=================coordinate:",kp_coordinate)
        show_img(img,"0")

        
        
class Variable:
    def _init_(self):
        self.value = 0


def main():
   
    ms = socket.socket()
    ms.bind(('localhost',5000))
    ms.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    ms.listen(5)
    blob_detector_params = cv2.SimpleBlobDetector_Params()
    blob_detector_params.filterByArea = True
    blob_detector_params.maxArea = 150
    blob_detector = cv2.SimpleBlobDetector_create(blob_detector_params)
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 150)
    
    
    inas=0
    while True:
        _, frame = cap.read()
        face_frame, face_coords = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            eye_coords = []
            eyes_frames = []
            for eye in eyes:
                if eye is not None:
                    eye = cut_eyebrows(eye)
                    keypoints = blob_process(eye, blob_detector)
                  
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                    kp_coordinate = (0,0)
                    kp_size = 0
                    for kp in keypoints:
                        if kp.size > kp_size:
                            kp_size = kp.size
                            kp_coordinate = kp.pt
                    if len(keypoints) > 0:
                        eyes_frames.append(eye)
                        eye_coords.append(kp_coordinate)
            inas+=1
            cv2.imshow('showing', face_frame)
            if len(eye_coords) > 0:
                send_data(frame.shape[:2],face_frame.shape[:2],face_coords,eye_coords,eyes_frames,ms)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()   

#Face coords
def face_scale(frame, face):
    width = face[1]/frame[1]
    height = face[0]/frame[0]
    return width, height

def eye_position(eye, eye_coord,i):
    maximo = 1
    B = 1
    h,w = eye.shape[0]-eye.shape[0]*.05, eye.shape[1]-eye.shape[1]*.1
    w_R = eye_coord[0]/w
    h_R = eye_coord[1]/h
    raw_valx.value = w_R
    raw_valy.value = h_R
    if(max_y.value<h_R):
        max_y.value = h_R
    if(min_y.value>h_R):
        min_y.value = h_R

    if(max_x.value<w_R):
        max_x.value = w_R
    if(min_X.value>w_R):
        min_X.value = w_R
        if(min_X.value<0.1):
            min_X.value = 0.1
    if(max_x.value>0):
        #w_Rp = ((w_R)*maximo)/(max_x.value)
        try:
            w_R = ((w_R-min_X.value*B)*maximo)/(max_x.value-min_X.value*B)
        except ZeroDivisionError:
            pass
    if(max_y.value>0 and min_y.value != max_y.value):
        h_R = ((h_R-min_y.value*B)*maximo)/(max_y.value-min_y.value*B)
    #kalman with scaling
    if(i==0):
        xn0 = w_R
        yn0 = h_R
        #Kalman static gain
        xnx = xn.value + (0.8)*(xn0-xn.value)
        xn.value = xnx
        yn.value = yn.value + (0.8)*(yn0-yn.value)
        #Kalman iterational gain
        xnx = xn1.value + (1/alpha.value)*(xn0-xn1.value)
        xn1.value = xnx
        xn2.value = raw_valx.value
        xn3.value = xn3.value + (1/alpha.value)*(raw_valx.value-xn3.value)
        xn4.value = xn0

    alpha.value = alpha.value + 1
    if(alpha.value>9):
        alpha.value = 1
    if(raw_valx.value>0.5 and raw_valx.value<0.65):
        return raw_valx.value,raw_valy.value
    return  xn.value+0.1,1-yn.value

def send_data(frame, face, face_coords, eye_coords,eyes,ms):
    fc = face_scale(frame, face)
    eyes_coords = []
    for i in range(len(eye_coords)):
        eyes_coords.append(eye_position(eyes[i],eye_coords[i],i))
    #o = input(eyes_coords)
    #eyes_coords[0][0] = xn
    plt.axis([0,hist_xn1.value+2,0,1])
    plt.ion()
    colors = ['bo','ro']
    plt.plot(hist_xn.value,xn.value,'bo')
    plt.plot(hist_xn1.value,xn1.value,'ro')
    plt.plot(hist_xn2.value,xn2.value,'go')
    plt.plot(hist_xn3.value,xn3.value,'mo')
    plt.plot(hist_xn4.value,xn4.value,'ko')
    # for i in range(len(eyes_coords)):
    #     plt.plot(xn,eyes_coords[i][1],colors[i])
    plt.draw()
    plt.show()
    plt.pause(0.001) 
    hist_xn.value = hist_xn.value + 1
    hist_xn1.value = hist_xn1.value + 1
    hist_xn2.value = hist_xn2.value + 1
    hist_xn3.value = hist_xn3.value + 1
    hist_xn4.value = hist_xn4.value + 1
    #    eye_coords = list(map(lambda i,eye=eye,eye_coords=eye_coords: list(map(lambda coord,eye[i],i=i  : eye_position(eye,eye_coords),eye_coords)), np.arange(len(eye_coords)))
    msj = str(fc)+"_"
    msj += str(face_scale(frame,face_coords))+"_"
    if len(eyes_coords) > 1:
        msj += str(eyes_coords[0])+"#"+str(eyes_coords[1])
    else:
        msj += str(eyes_coords[0])+"#"+str(eyes_coords[0])
    msj = msj.replace("(","").replace(")","").replace(" ","") #Limpiamos la cadena
    #msj = msj.replace("[","").replace("]","")
    connection, _ = ms.accept()
    if(connection != None):
        connection.send(msj.encode())
        #print(msj)
        print(max_x.value,min_X.value,max_y.value,min_y.value)
        #print(xn.value,yn.value)
        connection.close()
    
max_x = Variable()
max_x.value= 0
max_y = Variable()
max_y.value = 0
min_y = Variable()
min_y.value = 1
min_X = Variable()
min_X.value = 1
yn = Variable()
yn.value = 0.5
xn = Variable()
xn.value = 0.4375
alpha = Variable()
alpha.value = 1
xn1 = Variable()
xn1.value = xn.value
xn2 = Variable()
xn2.value = xn.value
xn3 = Variable()
xn3.value = xn.value
xn4 = Variable()
xn4.value = xn.value
hist_xn = Variable()
hist_xn.value = 1
hist_xn1 = Variable()
hist_xn1.value = 1
hist_xn2 = Variable()
hist_xn2.value = 1
hist_xn3 = Variable()
hist_xn3.value = 1
hist_xn4 = Variable()
hist_xn4.value = 1
raw_valy = Variable()
raw_valy.value = yn.value
raw_valx = Variable()
raw_valx.value = xn.value

main()