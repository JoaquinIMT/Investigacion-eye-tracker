import cv2
from matplotlib import pyplot as plt
from static_functions import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

import imutils

eye_detector = EyeDetector()

################# GUI#########################
def visualizar():
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y,path
    ret,frame = cap.read()
    if ret == True:
        eyes = eye_detector.eye_coords(frame)
        if eyes is not None:
            (ojo1_x, ojo1_y), (ojo2_x, ojo2_y) = eyes

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            cv2.putText(frame,f'x={(ojo1_x):.2f}',(50,60),fontFace=2,fontScale=0.5,color=(0,0,0))
            cv2.putText(frame,f'y={(ojo1_y):.2f}',(50,75),fontFace=2,fontScale=0.5,color=(0,0,0))
            cv2.putText(frame,f'x={(ojo2_x):.2f}',(200,60),fontFace=2,fontScale=0.5,color=(0,0,0))
            cv2.putText(frame,f'y={(ojo2_y):.2f}',(200,75),fontFace=2,fontScale=0.5,color=(0,0,0))
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblvideo.configure(image=img)
            lblvideo.image=img

            ##### modificación de parametros de imagen importada
                    
            #### leer la imagen
            image_imported =cv2.imread(path)
            image_imported = imutils.resize(image_imported,height=400)

            #### visualizar la imagen de entrada en la GUI
            image_imported = imutils.resize(image_imported,width=800)
            image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)

            image_import = cv2.circle(image_imported,(int(800*ojo1_x),int(400*ojo1_y)),7,(0,0,255),4)
            im = Image.fromarray(image_import)
            img = ImageTk.PhotoImage(image=im)

            lblInputImage.configure(image=img)
            lblInputImage.image = img
            print(ojo1_x,ojo1_y)
            cv2.waitKey(0)
            lblInputImage.configure(image=img)
            lblInputImage.image = img

        lblvideo.after(1,visualizar)
    else:
        lblvideo.image = ''
        lblInfoVideoPath.configure(text='')
        rad1.configure(state='active')
        rad2.configure(state='active')
        selected.set(0) ### esto es para que no este seleccionado ningujo 
            #### de las redondas
        boton_end.configure(state='active')
        cap.release()

def elegir_img():
    global path
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
        global ojo1_x,ojo1_y
        #### leer la imagen
        image_imported =cv2.imread(path)
        image_imported = imutils.resize(image_imported,height=400)

        #### visualizar la imagen de entrada en la GUI
        image_imported = imutils.resize(image_imported,width=800)
        image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)

        image_import = cv2.circle(image_imported,(400,200),7,(0,0,255),4)
        im = Image.fromarray(image_import)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img
    return

def video_de_entrada():
    global cap,threshold
    
    if selected.get() ==2:
        threshold = int(entrada_1.get())
        print(threshold)
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
    global lblInputImage,lblvideo,entrada_1,threshold
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y
    ojo1_x=0
    ojo1_y=0
    ojo2_x=0
    ojo2_y=0
    
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
        state='active',
        command=finalizar
        )
    boton_end.grid(column=0,row=7,columnspan=2,pady=10)

     ##### Ingreso botón que permita ingresar información
    inputThreshold= Label(root,text='Threshold')
    inputThreshold.grid(column=0,row=5)
    entry_var = StringVar()
    entrada_1 = Entry(root,state=NORMAL,textvariable=entry_var)
    entrada_1.grid(column=0,row=6)

    ################ Visualizando los valores en ojo izquierdo y ojo derecho ##############
    root.mainloop()

gui()