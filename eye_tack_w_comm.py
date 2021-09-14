import cv2
import socket
import numpy as np
import time

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
                    eyes_frames.append(eye)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                    kp_coordinate = (0,0)
                    kp_size = 0
                    for kp in keypoints:
                        if kp.size > kp_size:
                            kp_size = kp.size
                            kp_coordinate = kp.pt
                    if len(keypoints) > 0:
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

def eye_position(eye, eye_coord):
    h,w = eye.shape[0]-eye.shape[0]*.05, eye.shape[1]-eye.shape[1]*.1
    w_R = eye_coord[0]/w
    h_R = eye_coord[1]/h
    return w_R,h_R

def send_data(frame, face, face_coords, eye_coords,eyes,ms):
    fc = face_scale(frame, face)
    eyes_coords = []
    for i in range(len(eye_coords)):
        eyes_coords.append(eye_position(eyes[i],eye_coords[i]))

    #    eye_coords = list(map(lambda i,eye=eye,eye_coords=eye_coords: list(map(lambda coord,eye[i],i=i  : eye_position(eye,eye_coords),eye_coords)), np.arange(len(eye_coords)))
    msj = str(fc)+"_"
    msj += str(face_scale(frame,face_coords))+"_"
    if len(eyes_coords) > 1:
        msj += str(eyes_coords[0])+"#"+str(eyes_coords[1])
    else:
        msj += str(eyes_coords[0])+"#"+str(eyes_coords[0])
    msj = msj.replace("(","").replace(")","").replace(" ","") #Limpiamos la cadena

    connection, _ = ms.accept()
    if(connection != None):
        connection.send(msj.encode())
        print(msj)
        connection.close()

main()