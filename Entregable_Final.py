from tkinter.font import BOLD
import cv2
from matplotlib import pyplot as plt
from static_functions import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from time import time

import imutils
from kalmanfilter import KalmanFilter
eye_detector = EyeDetector()
kf = KalmanFilter()
global saved
saved = []
################# GUI#########################
def visualizar():
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y,path,save,img___,path_img
    global scaled_eye_x,scaled_eye_y
    global previous_time,current_time,count
    ret,frame = cap.read()
    if ret == True:
        eyes = eye_detector.eye_coords(frame)
        if eyes is not None:
            ( (ojo1_x, ojo1_y), (ojo2_x, ojo2_y) ), ( scaled_eye_x, scaled_eye_y) = eyes

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #cv2.putText(frame,f'x={(ojo1_x):.2f}',(50,60),fontFace=2,fontScale=0.5,color=(0,0,0))
            #cv2.putText(frame,f'y={(ojo1_y):.2f}',(50,75),fontFace=2,fontScale=0.5,color=(0,0,0))
            #cv2.putText(frame,f'x={(ojo2_x):.2f}',(200,60),fontFace=2,fontScale=0.5,color=(0,0,0))
            #cv2.putText(frame,f'y={(ojo2_y):.2f}',(200,75),fontFace=2,fontScale=0.5,color=(0,0,0))
            #### resize frame 
            frame = cv2.resize(frame,(75,50))
            ###########
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblvideo.configure(image=img)
            lblvideo.image=img
        
            ##### modificación de parametros de imagen importada    
            #### leer la imagen
            
            current_time=time()
            if (current_time-previous_time>7) and (count<6):
                
                path_img = path +img___[count]
                count +=1
                previous_time = time()
                elegir_img()
            if (count==6) and ((current_time-previous_time>7)):
                print('finalizar')
                finalizar()

            else:


                image_imported =cv2.imread(path_img)
                
                image_imported = cv2.resize(image_imported,(screen_width,screen_height))
                image_imported = imutils.resize(image_imported,height=screen_height) #"""height=400"""

                #### visualizar la imagen de entrada en la GUI
                image_imported = imutils.resize(image_imported,width=screen_width)
                image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)
                #img_copy = image_imported.copy()
                print('image copy')
                #print(img_copy)
                #img_copy[0:100,0:100,:] = frame[0:100,0:100,:]

                predicted = kf.predict(screen_width*scaled_eye_x,screen_height*scaled_eye_y)
                image_import = cv2.circle(image_imported,(int(screen_width*scaled_eye_x),int(screen_height*scaled_eye_y)),7,(0,0,255),4)
                image_import = cv2.circle(image_imported,(int(predicted[0]),int(predicted[1])),7,(255,0,0),4)
                saved = []
                
                im = Image.fromarray(image_import)
                img = ImageTk.PhotoImage(image=im)

                lblInputImage.configure(image=img)
                lblInputImage.image = img

                cv2.waitKey(0)
                lblInputImage.configure(image=img)
                lblInputImage.image = img
                ojo1_value_x.configure(text='{:.2f}'.format(ojo1_x),font=BOLD)
                ojo1_value_y.configure(text="{:.2f}".format(ojo1_y),font=BOLD)
                ojo2_value_x.configure(text='{:.2f}'.format(ojo2_x),font=BOLD)
                ojo2_value_y.configure(text='{:.2f}'.format(ojo2_y),font=BOLD)

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
    global path_img,path,img___
    global ojo1_x,ojo1_y
    """
    path = filedialog.askopenfilename(
        initialdir='/images',
        title='Selecciona una imagen',
        filetypes=(
        ('png files','*.png'), # any extension
        ('jpg files','*.jpg'),
        ('jpeg files','*.jpeg')
        )
    )
    """
    print('path',path_img)
    if len(path_img) >0:
        
        #### leer la imagen
        
        image_imported =cv2.imread(path_img)
        image_imported = cv2.resize(image_imported,(screen_width,screen_height))
        #image_imported.resize((screen_height-200,screen_width),Image.ANTIALIAS)
        print(image_imported)
        image_imported = imutils.resize(image_imported,height=screen_height) #"""height=400"""

        #### visualizar la imagen de entrada en la GUI
        image_imported = imutils.resize(image_imported,width=screen_width)#width=800)
       
        image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)

        image_import = cv2.circle(image_imported,((int(screen_width/2)),(int(screen_height/2)-50)),7,(0,0,255),4)
        print(screen_height)
        print(screen_width)
        im = Image.fromarray(image_import)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img
    return

def video_de_entrada():
    global cap,threshold,image_imported,path,img___,path_img
    global ojo1_value_x,ojo1_value_y,ojo2_value_x,ojo2_value_y
    global previous_time,current_time,count
    """
    from tkinter import *
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    print(width)
    print(height)

    """

    path = "C:/Users/Jesus Manuel/Documents/Tec/009 semestre/Proyectos Sistemas Inteligentes I/Investigacion-eye-tracker/img_prototype"
    img___ = [
        "/001.jpg",
        "/002.jpg",
        "/003.jpg",
        "/004.jpg",
        "/005.jpg",
        "/006.jpg"
    ]
    #image_imported =cv2.imread()
    if selected.get() == 1: 
        boton_end.configure(state='active')
        #boton_upload_file.configure(state='active')
        path_img=path+img___[0]
        elegir_img()
        previous_time = time() ### tiempo inicial 
        count = 0 ## contando el número de imagenes
        
    if selected.get() == 2: 
        #boton_upload_file.configure(state='disabled')
        rad1.configure(state='disabled')
        rad2.configure(state='disabled')
        boton_end.configure(state='active')
        lblInfoVideoPath.configure(text='')
        cap = cv2.VideoCapture(0)
        visualizar()

def finalizar():
    print('finalizar')
    lblInfoVideoPath.configure(text='')
    lblvideo.image=''
    lblInfoVideoPath.configure(text='')
    
    rad1.configure(state='active')
    rad2.configure(state='active')
    boton_end.configure(state='disabled')
    lblInputImage.image = ''
    selected.set(0)
    cap.release()
    ojo1_value_x.configure(text='0')
    ojo1_value_y.configure(text='0')
    ojo2_value_x.configure(text='0')
    ojo2_value_y.configure(text='0')

def gui():
    global cap,selected,IblInfo1,lblInfoVideoPath,rad1,rad2,boton_end,boton_upload_file,boton_upload_file
    global lblInputImage,lblvideo,entrada_1,threshold
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y
    global screen_width,screen_height ### obtención de tamaño de pantalla
    global ojo1_value_x,ojo1_value_y,ojo2_value_x,ojo2_value_y 
    ojo1_x=0
    ojo1_y=0
    ojo2_x=0
    ojo2_y=0
    
    cap = None
    root = Tk()

    IblInfo1 = Label(root,text='Entrada de Video',font='Bold')
    IblInfo1.grid(column=0,row=0,columnspan=1)

    selected = IntVar()
    rad1 = Radiobutton( ### para adjuntar imagen
        root,
        text='Inicializar visualización',
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

    rad1.grid(column=0,row=1,padx=0)
    rad2.grid(column=0,row=2,padx=0)

    ########## mostrar el pad del videos
    lblInfoVideoPath = Label(root,text='',width=20)
   # lblInfoVideoPath.grid(column=2,row=2)
    lblInfoVideoPath.grid(column=2,row=1)
    lblvideo = Label(root)
   # lblvideo.grid(column=1,row=4,columnspan=2)
    lblvideo.grid(column=2,row=0,columnspan=2,rowspan=3)

    ##### mostrar el botón para adjuntar imagen##########

    """
    boton_upload_file = Button(
        root,
        text='Siguiente',
        width = 25,
        command = elegir_img,
        state='disabled' ### estado actual
    )

    boton_upload_file.grid(
        column=0,row=3
    )
    """

    ################### segmentar donde se mostrará la imagen################
    lblInputImage=Label(root)
    lblInputImage.grid(column=0, row=3,pady=0,columnspan=5)

    ############ mostrar el botón para finalizar visualización###########
    boton_end = Button(
        root,
        text='Finalizar Visualización y limpiar',
        state='active',
        command=finalizar
        )
    boton_end.grid(column=1,row=0)
    ########## labels para ojo 1 y ojo 2 
    ojo_1_label = Label(root,text='Ojo 1')
    ojo_1_label.grid(column=2,row=0)
    ojo_2_label=Label(root,text='Ojo 2')
    ojo_2_label.grid(column=2,row=1)


    ####### visualizar posicion de ojos x e y   
    ojo1_value_x = Label(root,text=f'{ojo1_x}')
    ojo1_value_y = Label(root,text=f'{ojo1_y}')
    ojo2_value_x = Label(root,text=f'{ojo2_x}')
    ojo2_value_y = Label(root,text=f'{ojo2_y}')
    
    ojo1_value_x.grid(column=3,row=0)
    ojo1_value_y.grid(column=4,row=0)
    ojo2_value_x.grid(column=3,row=1)
    ojo2_value_y.grid(column=4,row=1)




 ##### Ingreso botón que permita ingresar información
   # inputThreshold= Label(root,text='Threshold')
  #  inputThreshold.grid(column=0,row=5)
    #entry_var = StringVar()
  #  entrada_1 = Entry(root,state=NORMAL,textvariable=entry_var)
  #  entrada_1.grid(column=0,row=6)

    #### tamaño de la pantalla obtención de datos

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() -150

    ################ Visualizando los valores en ojo izquierdo y ojo derecho ##############
    root.mainloop()

gui()