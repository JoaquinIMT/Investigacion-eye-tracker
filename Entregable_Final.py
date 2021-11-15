import cv2
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
def visualizar():
    global cap
    ret,frame = cap.read()
    if ret == True:
        frame= imutils.resize(frame,width=640)
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
    return

def video_de_entrada():
    global cap
    if selected.get() == 1: 
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

gui()