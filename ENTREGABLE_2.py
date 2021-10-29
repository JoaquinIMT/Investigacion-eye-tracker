import cv2
import socket
from matplotlib import pyplot as plt
from static_functions import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

import imutils



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

##### parámetros de openCV
blob_detector_params = cv2.SimpleBlobDetector_Params()
blob_detector_params.filterByArea = True
blob_detector_params.maxArea = 150
blob_detector = cv2.SimpleBlobDetector_create(blob_detector_params)


################# GUI#########################


def deteccion_facial(faces,frame):
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray,1.5,5)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        return frame



def visualizar():
    global cap
    ret,frame = cap.read()
    if ret == True:
        frame= imutils.resize(frame,width=640)
        #frame = deteccion_facial(frame)
        #print('deteccion')
       # print(frame)
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
            #inas+=1
            frame = cv2.cvtColor(face_frame,cv2.COLOR_BGR2RGB)
            if len(eye_coords) > 0:
            #Descomentar para usar con processing
               send_data(frame.shape[:2],face_frame.shape[:2],face_coords,eye_coords,eyes_frames)
        
            #frame = deteccion_facial(face_frame,frame)
            #print(frame) --> Visualización de cada cuadro en consola
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblvideo.configure(image=img)
            lblvideo.image=img
        lblvideo.after(1,visualizar)
    else:
        lblvideo.image = ''
        lblInfoVideoPath.configure(text='')
        rad1.configure(state='active')
        rad2.configure(state='active')
        selected.set(0) ### esto es para que no este seleccionado ningujo 
            #### de las redondas
        boton_end.configure(state='disabled')
        cap.release()

def elegir_img():
    path = filedialog.askopenfilename(
        initialdir='/images',
        title='Selecciona una imagen',
        filetypes=(
        ('png files','*.png'), # any extension
       # ('all files','*.*')  #any name, any extension
        ('jpg files','*.jpg'),
        ('jpeg files','*.jpeg')
        )
    )
    if len(path) >0:
        
        #### leer la imagen
        image =cv2.imread(path)
        image = imutils.resize(image,height=400)

        #### visualizar la imagen de entrada en la GUI
        image_show = imutils.resize(image,width=800)
        image_show = cv2.cvtColor(image_show,cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image_show)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        #### label imagen de entrada
        # Label IMAGEN DE ENTRADA
        #lblInfo1 = Label(root, text="IMAGEN DE ENTRADA:")
        #lblInfo1.grid(column=0, row=1, padx=5, pady=5)

    return
def video_de_entrada():
    global cap
    if selected.get() == 1: 
        #rad1.configure(state='disabled')
        #rad2.configure(state='disabled')
        boton_end.configure(state='active')
        boton_upload_file.configure(state='active')
    if selected.get() == 2: 
        boton_upload_file.configure(state='disabled')
        rad1.configure(state='disabled')
        rad2.configure(state='disabled')
        boton_end.configure(state='active')
        lblInfoVideoPath.configure(text='')
        cap = cv2.VideoCapture(0)
        visualizar()

def finalizar():
    lblInfoVideoPath.configure(text='')
    lblvideo.image=''
    lblInfoVideoPath.configure(text='')
    
    rad1.configure(state='active')
    rad2.configure(state='active')
    boton_end.configure(state='disabled')
    lblInputImage.image = ''
    selected.set(0)
    cap.release()

def gui():
        
    global cap,selected,IblInfo1,lblInfoVideoPath,rad1,rad2,boton_end,boton_upload_file,boton_upload_file
    global lblInputImage,lblvideo
    

    cap = None
    root = Tk()

    IblInfo1 = Label(root,text='Entrada de Video',font='Bold')
    IblInfo1.grid(column=0,row=0,columnspan=2)

    selected = IntVar()
    rad1 = Radiobutton( ### para adjuntar imagen
        root,
        text='Adjuntar Imagen',
        width=20,
        variable=selected,
        value=1,
        command=video_de_entrada
    )

    rad2 = Radiobutton( ## para poder visualizar la imagen de video
        root, 
        text='Ver Video en Vivo',
        width=20,
        variable=selected,
        value=2,
        command=video_de_entrada

    )

    rad1.grid(column=0,row=1)
    rad2.grid(column=1,row=1)

    ########## mostrar el pad del videos

    lblInfoVideoPath = Label(root,text='',width=20)
    lblInfoVideoPath.grid(column=1,row=2)
    lblvideo = Label(root)
    lblvideo.grid(column=1,row=4,columnspan=2)

    ##### mostrar el botón para adjuntar imagen##########
    boton_upload_file = Button(
        root,
        text='Ingrese una imagen',
        width = 25,
        command = elegir_img,
        state='disabled' ### estado actual
    )

    boton_upload_file.grid(
        column=0,row=3
    )
    ################### segmentar donde se mostrará la imagen################

    lblInputImage=Label(root)
    lblInputImage.grid(column=0, row=4)
    ############ mostrar el botón para finalizar visualización###########

    boton_end = Button(
        root,
        text='Finalizar Visualización y limpiar',
        state='disabled',
        command=finalizar
        )
    boton_end.grid(column=0,row=6,columnspan=2,pady=10)

    root.mainloop()





class Variable:
    def _init_(self):
        self.value = 0


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
        yn.value = yn.value + (0.7)*(yn0-yn.value)
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
        return raw_valx.value,1-yn.value
    return  xn.value,1-yn.value

def send_data(frame, face, face_coords, eye_coords,eyes):#,ms):
    fc = face_scale(frame, face)
    eyes_coords = []
    for i in range(len(eye_coords)):
        eyes_coords.append(eye_position(eyes[i],eye_coords[i],i))
    #o = input(eyes_coords)
    #eyes_coords[0][0] = xn
    #plt.axis([0,hist_xn1.value+2,0,1])
    #plt.ion()
    #colors = ['bo','ro']
    #plt.plot(hist_xn.value,xn.value,'bo')
    #plt.plot(hist_xn1.value,xn1.value,'ro')
    #plt.plot(hist_xn2.value,xn2.value,'go')
    #plt.plot(hist_xn3.value,xn3.value,'mo')
    #plt.plot(hist_xn4.value,xn4.value,'ko')
    # for i in range(len(eyes_coords)):
    #     plt.plot(xn,eyes_coords[i][1],colors[i])
    #plt.draw()
    #plt.show()
    #plt.pause(0.001) 
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
    print('message',msj)
    """
    #msj = msj.replace("[","").replace("]","")
    connection, _ = ms.accept()
    if(connection != None):
        connection.send(msj.encode())
        #print(msj)
        #print(max_x.value,min_X.value,max_y.value,min_y.value)
        print(xn.value,yn.value)
        connection.close()

    """

    
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

gui()