import tkinter as tk
import tkinter.font
##import picamera
import RPi.GPIO as GPIO
import time
from PIL import ImageTk, Image
import os

try:
    win=tk.Tk()
    win.geometry('480x320')
    win.title("Integrador 2")
    myFont=tkinter.font.Font(family = 'Helvetica', size = 12, weight =  "bold")
    win.attributes('-fullscreen', True)
    win.bind('<Escape>',lambda e: win.destroy())

    inputPins=[11,13,15,16]
    inputs=[0,0,0,0]
    reading=""
    last_reading=0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    for pin in inputPins:
        GPIO.setup(pin, GPIO.IN)
    
    pwm = GPIO.PWM(12, 100)
    dc = False
    pwm.start(0)

    def takePicture(pwm):
        global dc
        #pwm.ChangeDutyCycle(50)
        time.sleep(2.5)
        cam=picamera.PiCamera()
        cam.resolution = (320, 240)
        cam.capture('foto.jpg',use_video_port=True)
        #img = ImageTk.PhotoImage(Image.open("foto.jpg"))
        #panel.configure(image = img)
        #panel.image=img
        cam.close()
        time.sleep(2.5)
        if dc:
            pwm.ChangeDutyCycle(slider.get())
        else:
            pwm.ChangeDutyCycle(0)
            
    def exitProgram():
        win.destroy()


    def changeLEDstate(pwm,val):
        global dc
        if dc:                
            dc=False
            pwm.ChangeDutyCycle(0)
        else:   
            dc=True
            pwm.ChangeDutyCycle(val)
        
            

    def changeLedIntensity(value):
        pwm.ChangeDutyCycle(value)

    #panel para mostrar la intensidad
    text = tk.StringVar()    
    panel = tk.Label(win, textvariable=text)
    panel.pack(fill=tk.BOTH, expand=True)
    
    #slider para controlar la intensidad del led
    slider = tk.Scale(win, from_=100, to=0)
    slider.pack(fill=tk.X, expand=True)
    
    #boton tomar foto
    camShot=tk.Button(win, text="Tomar foto", font=myFont, command= lambda: takePicture(pwm), bg='bisque2')
    camShot.pack(fill=tk.X, expand=True)
    
    #boton de encendido/apagado del led
    onButton=tk.Button(win, text='Led (On/Off)', font=myFont, command= lambda: changeLEDstate(pwm,slider.get()), bg='bisque2')
    onButton.pack(fill=tk.X, expand=True)
    
    #boton de configuracion
    configButton=tk.Button(win, text='Configuración', font=myFont, bg='cyan')
    configButton.pack(fill=tk.X, expand=True)
    
    #baton para salir
    exitButton=tk.Button(win, text='Salir', font=myFont, command=exitProgram, bg='cyan')
    exitButton.pack(fill=tk.X, expand=True)

    backup_slider = slider.get()
    
    while True:
        win.update_idletasks()
        win.update()
        #if slider.get() != backup_slider and dc:
        if slider.get() != backup_slider:
            backup_slider = slider.get()
            text.set('Intensidad: '+str(backup_slider))
            pwm.ChangeDutyCycle(backup_slider)
        for i,pin in enumerate(inputPins):
            inputs[i] = GPIO.input(pin)
            reading+=str(inputs[i])
        
        print(int(reading[::-1],2))
        reading=int(reading[::-1],2)
        
        if reading != last_reading:
            last_reading = reading
            reading = (reading/15)*100
            pwm.ChangeDutyCycle(reading)
            slider.set(reading)
        reading = ""          
        #time.sleep(0.5)
        
finally:
        pwm.stop()                         
        GPIO.cleanup()
