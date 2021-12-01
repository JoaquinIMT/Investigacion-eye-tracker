from tkinter.font import BOLD
import cv2
from matplotlib import pyplot as plt
from static_functions import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from time import time
import os

import imutils
from kalmanfilter import KalmanFilter
eye_detector = EyeDetector()
kf = KalmanFilter()
global saved
saved = []
################# GUI#########################
def visualizar():
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y,path,save,img___,path_img, saved_img,change
    global scaled_eye_x,scaled_eye_y
    global previous_time,current_time,count
    ret,frame = cap.read()
    if ret == True:
        eyes = eye_detector.eye_coords(frame)
        if eyes is not None:
            ( (ojo1_x, ojo1_y), (ojo2_x, ojo2_y) ), ( scaled_eye_x, scaled_eye_y) = eyes
            scaled_eye_x = 1-scaled_eye_x
            
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            #### resize frame 
            frame = cv2.resize(frame,(75,50))
            ###########
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblvideo.configure(image=img)
            lblvideo.image=img
        
            ##### modificación de parametros de imagen importada    
            #### leer la imagen
            
            
            if count==0:
                saved_img = None

            if count!=0:
                change=write_to_file(scaled_eye_x,scaled_eye_y,count,change)
            
            current_time=time()
            if (current_time-previous_time>7) and (count<6):
                
                path_img = path +img___[count]
                count +=1
                change=True
                saved_img = None
                previous_time = time()
                elegir_img()
            if (count==6) and ((current_time-previous_time>7)):
                print('finalizar')
                finalizar()

            else:
                if saved_img is None:

                    image_imported =cv2.imread(path_img)
                    
                    image_imported = cv2.resize(image_imported,(screen_width,screen_height))
                    image_imported = imutils.resize(image_imported,height=screen_height) #"""height=400"""

                    #### visualizar la imagen de entrada en la GUI
                    image_imported = imutils.resize(image_imported,width=screen_width)
                    image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)
                    saved_img = image_imported.copy()
                else:
                    image_imported = saved_img.copy()

                predicted = kf.predict(screen_width*scaled_eye_x,screen_height*scaled_eye_y)
                image_import = cv2.circle(image_imported,(int(predicted[0]),int(predicted[1])),5,(0,0,255),4)
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
  
    if len(path_img) >0:
        
        #### leer la imagen
        
        image_imported =cv2.imread(path_img)
        image_imported = cv2.resize(image_imported,(screen_width,screen_height))
        image_imported = imutils.resize(image_imported,height=screen_height) #"""height=400"""

        #### visualizar la imagen de entrada en la GUI
        image_imported = imutils.resize(image_imported,width=screen_width)#width=800)
       
        image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)

        image_import = cv2.circle(image_imported,((int(screen_width/2)),(int(screen_height/2)-50)),7,(0,0,255),4)
        im = Image.fromarray(image_import)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img
    return

def video_de_entrada(): #Aqui esta el array de fotos
    global cap,threshold,image_imported,path,img___,path_img
    global ojo1_value_x,ojo1_value_y,ojo2_value_x,ojo2_value_y
    global previous_time,current_time,count

    path = os.path.join(os.getcwd(),"img_prototype")

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
        path_img=path+img___[0]
        elegir_img()
        previous_time = time() ### tiempo inicial 
        count = 0 ## contando el número de imagenes
        
    if selected.get() == 2: 
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
    write_to_file(screen_width,screen_height,50,change=True)
    guardar_images()

def guardar_images():
    f = open("logs.txt",'r')
    variable= True
    all_data ={}
    for i in range(7):
        imagen=[]
        while variable:
            line = f.readline()
            if line=="\n":
                break
            
            if line[0]!='I':      
                dato=line.split(sep='\n')[0].split(sep=',')
                imagen.append([float(dato[0]),float(dato[1])])
            # print('dato')
            if i==6 and line[0]!='I':
                dato=line.split(sep='\n')[0].split(sep=',')
                imagen.append([float(dato[0]),float(dato[1])])
                variable=False

        variable=True
        all_data[i]=imagen

    ### filtro de información

    print(all_data)

    screen_width=all_data[6][0][0]
    screen_height=all_data[6][0][1]
    path = os.path.join(os.getcwd(),"img_prototype")

    img___ = [
        "/001.jpg",
        "/002.jpg",
        "/003.jpg",
        "/004.jpg",
        "/005.jpg",
        "/006.jpg"
    ]

    for i in range(len(img___)):
        #### leer la imagen
        print(path+img___[i])
        image_imported =cv2.imread(path+img___[i])
        print(image_imported)
        image_imported = cv2.resize(image_imported,(int(screen_width),int(screen_height)))
        image_imported = imutils.resize(image_imported,height=int(screen_height)) #"""height=400"""

        #### visualizar la imagen de entrada en la GUI
        image_imported = imutils.resize(image_imported,width=int(screen_width))#width=800)
        
        #image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)
        
        #image_import = cv2.circle(image_imported,((int(screen_width/2)),(int(screen_height/2)-50)),7,(0,0,255),cv2.FILLED) #4
        image_import = None
        for j in range(len(all_data[i])):
            x = all_data[i][j][0]
            y = all_data[i][j][1]
            
            if j==0:
                image_import = cv2.circle(image_imported,((int(screen_width*x)),(int(screen_height*y))),7,(0,255,0),4)
            else:
                image_import = cv2.circle(image_import,((int(screen_width*x)),(int(screen_height*y))),7,(0,255,0),4)

        cv2.imwrite(f'{i} '+'view.jpg',image_import)


def gui():
    global cap,selected,IblInfo1,lblInfoVideoPath,rad1,rad2,boton_end,boton_upload_file,boton_upload_file
    global lblInputImage,lblvideo,entrada_1,threshold
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y
    global screen_width,screen_height ### obtención de tamaño de pantalla
    global ojo1_value_x,ojo1_value_y,ojo2_value_x,ojo2_value_y,change
    ojo1_x=0
    ojo1_y=0
    ojo2_x=0
    ojo2_y=0
    
    change=True ### el valor de cambio inicial para imagenes
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
    lblInfoVideoPath.grid(column=2,row=1)
    lblvideo = Label(root)
    lblvideo.grid(column=2,row=0,columnspan=2,rowspan=3)

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

    #### tamaño de la pantalla obtención de datos

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() -150

    ################ Visualizando los valores en ojo izquierdo y ojo derecho ##############
    root.mainloop()

gui()