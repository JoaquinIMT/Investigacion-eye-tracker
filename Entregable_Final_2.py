from kalmanfilter import KalmanFilter 
import numpy as np
import mediapipe as mp


from tkinter.font import BOLD
import cv2
from matplotlib import pyplot as plt
#from static_functions import *
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from time import time

import imutils
from kalmanfilter import KalmanFilter


kf = KalmanFilter()
global saved
saved = []
################# GUI#########################
def visualizar():
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y,path,save,img___,path_img, saved_img
    global scaled_eye_x,scaled_eye_y
    global previous_time,current_time,count
    global cap,ojo1_x,ojo1_y,ojo2_x,ojo2_y,path,image_imported
    ret,frame = cap.read()
    #frame = imutils.resize(frame,width=100,height=100)
    image = frame
    if ret == True:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        # Image
        height, width, _ = image.shape
        
        def locateref(arr,j,face_landmarks,width=width,height=height):
            pt2 = face_landmarks.landmark[arr[j]]
            x1,y1 = int(pt2.x * width),int(pt2.y * height)
            return x1,y1
        array = [473,473]
        array1 = [474,469]
        array2 = [362,263]#[133,33]
        array3 = [374,385]#386
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        #cap = cv2.VideoCapture(0)
        eye_coords = []
        pointsR.value = []
        pointsL.value = []
        pointsL1.value = []
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        # mp_drawing.draw_landmarks(
                        #     image=image,
                        #     landmark_list=face_landmarks,
                        #     connections=mp_face_mesh.FACEMESH_IRISES,
                        #     landmark_drawing_spec=drawing_spec,)
                        for j,i in enumerate(array):
                            pt1 = face_landmarks.landmark[i]
                            x = int(pt1.x * width)
                            y = int(pt1.y * height)
                            cv2.circle(image, (x, y), 2, (0,0, 255), -1)
                            x1,y1 = locateref(array1,j,face_landmarks)
                            #cv2.circle(image, (x1, y1), 2, (0,0, 255), -1)
                            pointsR.value.append([x1,y1])
                            x1,y1 = locateref(array2,j,face_landmarks)
                            boundingB_fit = [9,10]#11,9
                            x1 = x1 - boundingB_fit[j]*(np.power(-1,j+1))
                            cv2.circle(image, (x1, y1), 2, (0,0, 100), -1)
                            pointsL.value.append([x1,y1])
                            x2,y2 = locateref(array3,j,face_landmarks)
                            if(j==1):
                                xx,y3 = locateref([386],0,face_landmarks)
                                y2 = (y2 + y3)/2
                                y2 = int(y2 + 1 )
                                x2 = int((x2 + xx)*0.5)
                            else:
                                y2 = y2 - 3
                            cv2.circle(image, (x2, y2), 2, (0,0, 100), -1)
                            pointsL1.value.append([x2,y2])
                           
                            eye_coords.append([x,y])
                            #cv2.putText(image, str(i), (x, y), 0, 1, (0, 0, 0))
                    # cv2.imshow("Image", image)
                    #   cv2.waitKey(1)
                    # count+=1
                    # cap.release()
                    # cv2.destroyAllWindows()   
            #inas+=1
        frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(75,50))

        cv2.putText(frame,f'x={(ojo1_x):.2f}',(50,60),fontFace=2,fontScale=0.5,color=(0,0,0))
        cv2.putText(frame,f'y={(ojo1_y):.2f}',(50,75),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'xU={(max_xkppt.value[0]):.2f}',(200,60),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'xL={(min_xkppt.value[0]):.2f}',(200,75),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'x={(trueposition.value):.2f}',(400,60),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'y={(tr.value):.2f}',(400,75),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'yU={(max_xkppt.value[1]):.2f}',(300,60),fontFace=2,fontScale=0.5,color=(0,0,0))
        # cv2.putText(frame,f'yl={(min_xkppt.value[1]):.2f}',(300,75),fontFace=2,fontScale=0.5,color=(0,0,0))
        
        if len(eye_coords) > 0:
        #Descomentar para usar con processing
            send_data(frame.shape[:2],image.shape[:2],image,eye_coords,image) ### necesito coordenadas de ojo izq y derecho
    
        #frame = deteccion_facial(face_frame,frame)
        #print(frame) --> Visualización de cada cuadro en consola
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblvideo.configure(image=img)
        lblvideo.image=img
  
        if count==0:
            saved_img = None
        current_time=time()
        if (current_time-previous_time>7) and (count<6):
            
            path_img = path +img___[count]
            count +=1
            saved_img = None
            previous_time = time()
            elegir_img()
        if (count==6) and ((current_time-previous_time>7)):
            print('finalizar')
            finalizar()

        else:
            print(type(saved_img))
            if saved_img is None:

                image_imported =cv2.imread(path_img)
                
                image_imported = cv2.resize(image_imported,(screen_width,screen_height))
        

                #### visualizar la imagen de entrada en la GUI
        
                image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)
                saved_img = image_imported.copy
            image_imported1 = image_imported.copy()
            #img_copy = image_imported.copy()
            #print('image copy')
            #print(img_copy)
            #img_copy[0:100,0:100,:] = frame[0:100,0:100,:]

            #predicted = kf.predict(screen_width*scaled_eye_x,screen_height*scaled_eye_y)
            image_import = cv2.circle(image_imported1,(int(ojo1_x),int(ojo1_y)),7,(0,0,255),4)
            #image_import = cv2.circle(image_imported,(int(predicted[0]),int(predicted[1])),5,(255,0,0),4)
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
    #print('path',path_img)
    if len(path_img) >0:
        
        #### leer la imagen
        
        image_imported =cv2.imread(path_img)
        image_imported = cv2.resize(image_imported,(screen_width,screen_height))
        #image_imported.resize((screen_height-200,screen_width),Image.ANTIALIAS)
        #print(image_imported)
        image_imported = imutils.resize(image_imported,height=screen_height) #"""height=400"""

        #### visualizar la imagen de entrada en la GUI
        image_imported = imutils.resize(image_imported,width=screen_width)#width=800)
       
        image_imported = cv2.cvtColor(image_imported,cv2.COLOR_BGR2RGB)

        image_import = cv2.circle(image_imported,((int(screen_width/2)),(int(screen_height/2)-50)),7,(0,0,255),4)
        #print(screen_height)
        #print(screen_width)
        im = Image.fromarray(image_import)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img
    return

def video_de_entrada(): #Aqui esta el array de fotos
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

    path = "img_prototype"
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
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() -150
    screen_shape.value = [screen_width,screen_height]
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
class Variable:
    def init(self):
        self.value = 0


#Face coords
def face_scale(frame, face):
    width = face[1]/frame[1]
    height = face[0]/frame[0]
    return width, height

def eye_position(eye_coord):
    WD, HD = screen_shape.value[0],screen_shape.value[1]
    # h,w = eye.shape[0]-eye.shape[0]*0.1, eye.shape[1]-eye.shape[1]*0.05
    # w_R = eye_coord[0]/w
    # h_R = eye_coord[1]/h
    xn0 = eye_coord[0]
    yn0 = eye_coord[1]
    #Kalman static gain
    xnx = xn.value[0] + (0.3)*(xn0-xn.value[0])
    xn.value[0] = xnx
    yn.value[0] = yn.value[0] + (0.3)*(yn0-yn.value[0])
    A = xn.value[0]
    B = yn.value[0]
    trueposition.value = eye_coord[0]
    tr.value = eye_coord[1]
    # if(max_xkppt.value[0]<A):
    #     max_xkppt.value[0] =A
    # if(min_xkppt.value[0]>A):
    #     min_xkppt.value[0] = A
    maxx = pointsL.value[1][0] 
    minn = pointsL.value[0][0] 
    maxxx = pointsL1.value[0][1]
    minnn = pointsL1.value[1][1]
    #print(pointsL1.value,"wsasa")
    prediction = kf.predict(maxx,minn)
    maxx = prediction[0]
    minn = prediction[1]
    max_xkppt.value = [maxx,maxxx]
    min_xkppt.value = [minn,minnn]
    # maxx = maxx + (maxx-minn)
    # minn = minn - (pointsR.value[0][0]-pointsL.value[1][0])
    # maxx = max_xkppt.value
    # minn = min_xkppt.value
    A = ((A-minn)/(maxx-minn+0.01))
    
    if(A>0.5):
        A2 = (1-A)*WD-50#*1.5-(450)
    if(A<0.5):
        A2 = (1-A)*WD+50#*1.5-(450)
    B = ((B-minnn)/(maxxx-minnn+0.01))
    if(B>0.5):
        B2 = (1-B)*HD-10#*1.5-(450)
    if(B<0.5):
        B2 = (1-B)*HD+10#*1.5-(450)
    print
    xn0 = A2
    yn0 = B2
    xnx = xn.value[1] + (0.3)*(xn0-xn.value[1])
    xn.value[1] = xnx
    yn.value[1] = yn.value[1] + (0.3)*(yn0-yn.value[1])
    if(xn.value[1]>WD):
        xn.value[1] = WD
    if(xn.value[1]<0):
        xn.value[1] = 0
    if(yn.value[1]>500):
        yn.value[1] = 500
    if(yn.value[1]<0):
        yn.value[1] = 0    
    A2 = xn.value[1]
    B2 = yn.value[1]
    return  A2,B2

def send_data(frame, face, face_coords, eye_coords,eyes):#,ms):
    global ojo1_x,ojo1_y,ojo2_x,ojo2_y
    eyes_coords = []
    eyes_coords.append(eye_position(eye_coords[1]))
    if len(eyes_coords) > 0:
        ojo1_x,ojo1_y = eyes_coords[0]  ##### coordenadas en x e y para el ojo 1  
    ############### fixed 2 digits##############
    else:
        return (0,0)
trueposition = Variable()
trueposition.value = 1
lastposition = Variable()
lastposition.value =-1
tr = Variable()
tr.value = 0
max_xkppt = Variable()
min_xkppt = Variable()
max_xkppt.value = [1,1]
min_xkppt.value = [800,400]
yn = Variable()
yn.value = [300,300]
xn = Variable()
xn.value = [300,300]
# alpha = Variable()
# alpha.value = 1
xn1 = Variable()
xn1.value = xn.value
pointsR = Variable()
pointsR.value = []
pointsL = Variable()
pointsL.value = []
pointsL1 = Variable()
pointsL1.value = []
kf = KalmanFilter()
ktk = Variable()
ktk.value = 0
screen_shape = Variable()

gui()