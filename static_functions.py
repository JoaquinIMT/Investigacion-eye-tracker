import cv2
import socket
import numpy as np
import pyautogui


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
        if y > height / 2 or y<.3*height:
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

def blob_process(img, detector, threshold=40):
    _, img = cv2.threshold(img, threshold, 250, cv2.THRESH_BINARY)
    #cv2.imshow('blured4', img)
    img = cv2.erode(img, None, iterations=4)
    #cv2.imshow('blured3', img)
    img = cv2.dilate(img, None, iterations=6)
    #cv2.imshow('blured2', img)
    img = cv2.medianBlur(img, 7)
    #cv2.imshow('blured', img)
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

#Face coords
def face_scale(frame, face):
    width = face[1]/frame[1]
    height = face[0]/frame[0]
    return width, height

def eye_position(eye, eye_coord):
    h,w = eye.shape[0]-eye.shape[0]*.05, eye.shape[1]-eye.shape[1]*.1
    w_R = eye_coord[1]/w
    h_R = eye_coord[0]/h
    
    return w_R,h_R