import tkinter as tk
import tkinter.font
import RPi.GPIO as GPIO
import time
import numpy as np
from picamera import PiCamera
from PIL import ImageTk, Image

#toma una foto, la guarda en disco y la muestra en pantalla
def takePicture():
    global dc
    #time.sleep(2.5)
    cam=PiCamera()
    cam.resolution = (320, 240)
    cam.brightness = 50
    cam.exposure_mode = 'night'
    #modificar si la imagen no sale bien
    #cam.contrast = 50
    #cam.image_effect = 'colorbalance'

    cam.capture('foto.jpg',use_video_port=True)
    img = ImageTk.PhotoImage(Image.open("foto.jpg"))
    panel.configure(image = img)
    panel.image=img
    
    #calcula el color promedio de los pixeles en la imagen
    im = Image.open('foto.jpg')
    pix_val = list(im.getdata())
    #pix_val_flat = [x for sets in pix_val for x in sets]
    text2.set('Intensidad: '+ str(np.round(np.average(pix_val))))

    #panel = tk.Label(win, textvariable=text)
    #panel.pack(fill=tk.BOTH, expand=True)

    time.sleep(0.1)
    cam.close()  

#cambia el estado del LED
def changeLEDstate():
    global dc
    global last_read
    if dc:                
        dc=False
        last_read=slider.get()
        pwm.ChangeDutyCycle(0)
        slider.set(0)
    else:   
        dc=True
        pwm.ChangeDutyCycle(last_read)
        slider.set(last_read)
  
def exitProgram():
    win.destroy()
            
try:
    GPIO.setwarnings(False)
    #configura la ventana principal(tamaño, título, fullscreen)
    win=tk.Tk()
    win.geometry('480x320')
    win.title("Integrador 2")
    myFont=tkinter.font.Font(family = 'Helvetica', size = 12, weight =  "bold")
    win.attributes('-fullscreen', True)
    win.bind('<Escape>',lambda e: win.destroy())
    
    GPIO.setmode(GPIO.BOARD)
    inputPins=[11,13,15,16] #configura los pines que se usan como la entrada del potenciómetro
    for pin in inputPins:
        GPIO.setup(pin, GPIO.IN)
    
    #configura el pin que se usa para controlar la intensidad del led
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 100)
    dc = True #estado del led(false=off,true=on)
    last_read = 0 #intensidad del led antes de apagarse
    pwm.start(0)
    
    #reading=0 #lectura actual del pot
    last_reading=0 #lectura previa del pot
    
    #panel para mostrar la imagen
    text = tk.StringVar()    
    panel = tk.Label(win, textvariable=text)
    panel.pack(fill=tk.BOTH, expand=True)
    
    #label para mostrar la intensidad de la imagen capturada
    text2 = tk.StringVar()    
    panel2 = tk.Label(win, textvariable=text2)
    panel2.pack(fill=tk.BOTH, expand=True)
    text2.set('Intensidad: ')
    
    #slider para controlar la intensidad del led
    slider = tk.Scale(win, from_=100, to=0)
    slider.pack(fill=tk.X, expand=True)
    
    #botón para tomar foto
    camShot=tk.Button(win, text="Tomar foto", font=myFont, command= lambda: takePicture(), bg='bisque2')
    camShot.pack(fill=tk.X, expand=True)
    
    #botón de encendido/apagado del led
    onButton=tk.Button(win, text='Led (On/Off)', font=myFont, command= lambda: changeLEDstate(), bg='bisque2')
    onButton.pack(fill=tk.X, expand=True)
    
    #botón de configuración(no hace nada)
    #configButton=tk.Button(win, text='Configuración', font=myFont, bg='cyan')
    #configButton.pack(fill=tk.X, expand=True)
    
    #botón para salir
    exitButton=tk.Button(win, text='Salir', font=myFont, command=exitProgram, bg='cyan')
    exitButton.pack(fill=tk.X, expand=True)
    
    backup_slider = slider.get()
    
    #toma el valor del potenciómetro y cambia la intensidad según este valor
    def getPotValue():
        #toma la lectura del ADC y la concatena en un binario
        global last_reading
        tmp=""
        for i,pin in enumerate(inputPins):
            tmp+=str(GPIO.input(pin))
            
        #convierte la lectura de binario a decimal    
        reading=int(tmp[::-1],2)
        
        #cambia la intensidad del led solo si la lectura del potenciómetro cambió
        print("current:" + str(reading) + "last: " + str(last_reading))
        if reading != last_reading:
            last_reading = reading
            reading = int((reading/15)*100) #mapea la lectura de 0-15(resolución del ADC) a 0-100
            pwm.ChangeDutyCycle(reading)
            slider.set(reading)
        #time.sleep(1)
        
    while True:     
        #actualiza la GUI
        win.update_idletasks()
        win.update()
        
        #cambia la intensidad del led solo si la posición del slider cambió
        if slider.get() != backup_slider:
            backup_slider = slider.get()
            pwm.ChangeDutyCycle(backup_slider)
            
            #muestra el valor del slider en un label 
            #text = tk.StringVar()    
            #panel = tk.Label(win, textvariable=text)
            #panel.pack(fill=tk.BOTH, expand=True)
            #text.set('Intensidad: '+str(backup_slider))
        
        #cambia la intensidad del led con el valor del potenciómetro (comentar si no hay pot)
        getPotValue()
                        
        #time.sleep(0.5)
        
finally:
    pwm.stop()                         
    GPIO.cleanup()
