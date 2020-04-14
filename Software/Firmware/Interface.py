#!/usr/bin/env python3

#copyright Tom Schimansky 2020
import os
#os.system("export DISPLAY=:0")

import tkinter, time
from PIL import Image, ImageTk

from tkinter import messagebox

from ph_manage import *

time.sleep(3)

#import ph_MeasurementFirmware as MF
import socket

#sudo apt update
#sudo apt-get install python-imaging
#sudo apt-get install python-imaging python-imaging-tk

HOST = 'localhost'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
while not connected:
    try:
        s.connect((HOST, PORT))
        connected = True
    except Exception as e:
        pass

running = True; first = True; t2 = time.time()
tk = tkinter.Tk(); tk.title("Window Frame");
tk.attributes('-fullscreen', True)

FPS = 25 #1000
WIDTH = tk.winfo_screenwidth()
HEIGHT = tk.winfo_screenheight()
#MAIN_PATH = os.path.dirname(os.path.abspath("__file__"))
MAIN_PATH = "/home/pi/Photometer"
print(MAIN_PATH)

PERCENT = WIDTH/1040
MEASUREMENT = "EMPTY"

REFERENCE_LABEL = ""

def resize_image(image):
    img = image.resize((int(image.size[0]*PERCENT), int(image.size[1]*PERCENT)), Image.ANTIALIAS)
    return img

start_img         = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/start.png")))
start_pressed_img = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/start_pressed.png")))
exit_img          = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/exit.png")))
exit_pressed_img  = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/exit_pressed.png")))
radio_green_img   = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/g.png")))
radio_blue_img    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/b.png")))
radio_img         = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/radio.png")))
background_img    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/back.png")))

image_0    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/0.png")))
image_1    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/1.png")))
image_2    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/2.png")))
image_3    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/3.png")))
image_4    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/4.png")))
image_5    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/5.png")))
image_6    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/6.png")))
image_7    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/7.png")))
image_8    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/8.png")))
image_9    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/9.png")))

image_comma    = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/comma.png")))
image_c        = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/c.png")))

ref_img        = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/ref.png")))
enter_img      = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/enter.png")))
ref_label_img  = ImageTk.PhotoImage(resize_image(Image.open(MAIN_PATH+"/images/ref_label.png")))

def on_closing(event=0):
    global running
    running = False
    tk.destroy()
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.bind("<Command-q>", on_closing)
tk.bind("<Command-w>", on_closing)

def keyEvent(event):
    if event.keysym == "Return":
        pass
tk.bind("<Key>", keyEvent)

def start_button_press():
    #label1.config(text="REFERENCE_LABEL: "+str(REFERENCE_LABEL))
    start_button.config(image=start_pressed_img);tk.update()
    time.sleep(0.1)
    start_button.config(image=start_img);tk.update()

    text_label.config(text="MEASUREMENT IN PROGRESS...");tk.update()

    data = []
    data_INT = []
    data_EXT = []
    data_CON = []

    if sum(cha == "." for cha in REFERENCE_LABEL) > 1 or REFERENCE_LABEL == ".":
        text_label.config(text="REFERENCE VALUE INCORRECT!\nTOO MANY DOTS");tk.update()
        return

    if MEASUREMENT == "EMPTY":
        data, extinction = doEmptyMeasurement(s, "Leermessung")
        s.sendall(('colors/255/0/0/635/'+str(round(data[0], 3))+'/0/255/0/525/'+str(round(data[1], 3))+'/0/0/255/471/'+str(round(data[2], 3))+'\n').encode())
        text_label.config(text="EMPTY INTENSITIES:\n\n"+
                          "  RED: "+str(round(data[0],3))+" Lux  \nGREEN: "+str(round(data[1], 3))+" Lux  \n BLUE: "+str(round(data[2], 3))+" Lux  ");tk.update()

    elif MEASUREMENT == "REFERENCE":
        if REFERENCE_LABEL != "":
            data_INT, data_EXT, data_COE, success = doReferenceMeasurement(float(str(REFERENCE_LABEL)), s, "Referenzmessung")
            if success == True:
                s.sendall(('reference/'+str(REFERENCE_LABEL)+'/'+str(round(data_INT[0], 3))+'/'+str(round(data_EXT[0], 3))+'/'+str(round(data_COE[0],3))+'/'+str(round(data_INT[1],3))+'/'+str(round(data_EXT[1], 3))+'/'+str(round(data_COE[1], 3))+'/'+str(round(data_INT[2], 3))+'/'+str(round(data_EXT[2], 3))+'/'+str(round(data_COE[2], 3))+'\n').encode())
                text_label.config(text="REFERENCE INTENSITIES:\n\n"+
                          "  RED: "+str(round(data_INT[0], 3))+" Lux  \nGREEN: "+str(round(data_INT[1], 3))+" Lux  \n BLUE: "+str(round(data_INT[2], 3))+" Lux  ");tk.update()
            else:
                text_label.config(text="MEASUREMENT FAILED!\n\nDO EMPTY MEASUREMENT AND\nENTER REFERENCE CONCENTRATION\nTHEN TRY AGAIN.");tk.update()
        else:
            text_label.config(text="MEASUREMENT FAILED!\n\nDO EMPTY MEASUREMENT AND\nENTER REFERENCE CONCENTRATION\nTHEN TRY AGAIN.");tk.update()

    elif MEASUREMENT == "NORMAL":
        data_INT, data_EXT, data_CON, success = doOrdinaryMeasurement(s, "Normalmessung")
        if success == True:
            s.sendall(('measurements/'+str(round(data_INT[0], 3))+'/'+str(round(data_EXT[0], 3))+'/'+str(round(data_CON[0], 3))+'/'+str(round(data_INT[1], 3))+'/'+str(round(data_EXT[1], 3))+'/'+str(round(data_CON[1], 3))+'/'+str(round(data_INT[2], 3))+'/'+str(round(data_EXT[2], 3))+'/'+str(round(data_CON[2], 3))+'\n').encode())
            text_label.config(text="CONCENTRATIONS:\n"+"  RED: "+str(round(data_CON[0], 3))+" mol/L  \nGREEN: "+str(round(data_CON[1], 3))+" mol/L  \n BLUE: "+str(round(data_CON[2], 3))+" mol/L  \nAVERAGE:         "+str(round(((data_CON[0]+data_CON[1]+data_CON[2])/3), 3))+" mol/L");tk.update()
        else:
            text_label.config(text="MEASUREMENT FAILED!\n\nENTER REFERENCE CONCENTRATION\nAND DO REFERENCE MEASUREMENT.\nTHEN TRY AGAIN.");tk.update()

    #data = MF.getMeasureIntensity()
    time.sleep(0.1)

    pass

def exit_button_press():
    exit_button.config(image=exit_pressed_img);tk.update()
    time.sleep(0.1)
    exit_button.config(image=exit_img);tk.update()
    shutdown = messagebox.askyesnocancel(title="EXIT", message="Do you want to shutdown?")
    if shutdown: on_closing(); os.system("sudo shutdown -h now")
    elif shutdown == False: on_closing()

def ref_value_press():
    frame_1.pack_forget()
    frame_2.pack(side="top", fill="both", expand=True)
    pass

def press_0():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "0"
    pass
def press_1():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "1"
    pass
def press_2():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "2"
    pass
def press_3():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "3"
    pass
def press_4():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "4"
    pass
def press_5():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "5"
    pass
def press_6():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "6"
    pass
def press_7():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "7"
    pass
def press_8():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "8"
    pass
def press_9():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "9"
    pass
def comma_press():
    global REFERENCE_LABEL
    REFERENCE_LABEL += "."
    pass
def c_press():
    global REFERENCE_LABEL
    REFERENCE_LABEL = ""
    pass


def enter_press():
    frame_2.pack_forget()
    frame_1.pack(side="top", fill="both", expand=True)
    pass

def button_press_1():
    global MEASUREMENT
    MEASUREMENT = "EMPTY"
    button1.config(image=radio_blue_img)
    button2.config(image=radio_green_img)
    button3.config(image=radio_green_img)
    pass

def button_press_2():
    global MEASUREMENT
    MEASUREMENT = "REFERENCE"
    button1.config(image=radio_green_img)
    button2.config(image=radio_blue_img)
    button3.config(image=radio_green_img)
    pass

def button_press_3():
    global MEASUREMENT
    MEASUREMENT = "NORMAL"
    button1.config(image=radio_green_img)
    button2.config(image=radio_green_img)
    button3.config(image=radio_blue_img)
    pass

frame_1 = tkinter.Frame(tk, width = WIDTH, height = HEIGHT)
frame_1.pack(side="top", fill="both", expand=True)

frame_2 = tkinter.Frame(tk, width = WIDTH, height = HEIGHT)

label1 = tkinter.Label(master=frame_1, bg='gray89')
label1.place(x=20,y=20)

start_button = tkinter.Button(frame_1, command=start_button_press)
start_button.config(image=start_img, width=str(start_img.width()), height=str(start_img.height()))
start_button.place(x=33*PERCENT, y= 36*PERCENT)

exit_button = tkinter.Button(frame_1, command=exit_button_press)
exit_button.config(image=exit_img, width=str(exit_img.width()), height=str(exit_img.height()))
exit_button.place(x=33*PERCENT, y= 240*PERCENT)

ref_button = tkinter.Button(frame_1, command=ref_value_press)
ref_button.config(image=ref_img, width=str(ref_img.width()), height=str(ref_img.height()))
ref_button.place(x=288*PERCENT, y= 240*PERCENT)

radio_label = tkinter.Label(frame_1)
radio_label.config(image=radio_img, width=str(radio_img.width()), height=str(radio_img.height()))
radio_label.place(x=544*PERCENT, y= 37*PERCENT) # y was before 28

button1 = tkinter.Button(frame_1, command=button_press_1, highlightthickness=0, bg='#434243')
button1.config(image=radio_blue_img, width=str(radio_blue_img.width()), height=str(radio_blue_img.height()))
button1.place(x=573*PERCENT, y= 66*PERCENT)

button2 = tkinter.Button(frame_1, command=button_press_2, highlightthickness=0, bg='#434243')
button2.config(image=radio_green_img, width=str(radio_green_img.width()), height=str(radio_green_img.height()))
button2.place(x=573*PERCENT, y= 165*PERCENT)

button3 = tkinter.Button(frame_1, command=button_press_3, highlightthickness=0, bg='#434243')
button3.config(image=radio_green_img, width=str(radio_green_img.width()), height=str(radio_green_img.height()))
button3.place(x=573*PERCENT, y= 266*PERCENT)

textfield_label = tkinter.Label(frame_1)
textfield_label.config(image=background_img,width=str(background_img.width()),height=str(background_img.height()))
textfield_label.place(x=35*PERCENT, y= 408*PERCENT)

text_label = tkinter.Label(frame_1, bg='#434243', font=("Avenir Next", int(25*PERCENT)), fg="white", width=40 )
text_label.place(x=135*PERCENT, y= 425*PERCENT)  #x was before 99

#---------- FRAME 2

yd = -8

enter_button = tkinter.Button(frame_2, command=enter_press)
enter_button.config(image=enter_img, width=str(enter_img.width()), height=str(enter_img.height()))
enter_button.place(x=640*PERCENT, y= 540*PERCENT+yd)

ref_label_i = tkinter.Label(frame_2)
ref_label_i.config(image=ref_label_img ,width=str(ref_label_img.width()) ,height=str(ref_label_img.height()))
ref_label_i.place(x=640*PERCENT, y= 40*PERCENT+yd)

ref_label = tkinter.Label(frame_2, bg='#323232', font=("Courier", int(52*PERCENT)), fg="white", width=7 )
ref_label.place(x=669.5*PERCENT, y= 73*PERCENT+yd)

button_0 = tkinter.Button(frame_2, command=press_0)
button_0.config(image=image_0, width=str(image_0.width()), height=str(image_0.height()))
button_0.place(x=250*PERCENT, y= 540*PERCENT+yd)
button_1 = tkinter.Button(frame_2, command=press_1)
button_1.config(image=image_1, width=str(image_1.width()), height=str(image_1.height()))
button_1.place(x=450*PERCENT, y= 380*PERCENT+yd)
button_2 = tkinter.Button(frame_2, command=press_2)
button_2.config(image=image_2, width=str(image_2.width()), height=str(image_2.height()))
button_2.place(x=250*PERCENT, y= 380*PERCENT+yd)
button_3 = tkinter.Button(frame_2, command=press_3)
button_3.config(image=image_3, width=str(image_3.width()), height=str(image_3.height()))
button_3.place(x=50*PERCENT, y=380*PERCENT+yd)
button_4 = tkinter.Button(frame_2, command=press_4)
button_4.config(image=image_4, width=str(image_4.width()), height=str(image_4.height()))
button_4.place(x=450*PERCENT, y= 205*PERCENT+yd)
button_5 = tkinter.Button(frame_2, command=press_5)
button_5.config(image=image_5, width=str(image_5.width()), height=str(image_5.height()))
button_5.place(x=250*PERCENT, y= 205*PERCENT+yd)
button_6 = tkinter.Button(frame_2, command=press_6)
button_6.config(image=image_6, width=str(image_6.width()), height=str(image_6.height()))
button_6.place(x=50*PERCENT, y= 205*PERCENT+yd)
button_7 = tkinter.Button(frame_2, command=press_7)
button_7.config(image=image_7, width=str(image_7.width()), height=str(image_7.height()))
button_7.place(x=450*PERCENT, y= 40*PERCENT+yd)
button_8 = tkinter.Button(frame_2, command=press_8)
button_8.config(image=image_8, width=str(image_8.width()), height=str(image_8.height()))
button_8.place(x=250*PERCENT, y= 40*PERCENT+yd)
button_9 = tkinter.Button(frame_2, command=press_9)
button_9.config(image=image_9, width=str(image_9.width()), height=str(image_9.height()))
button_9.place(x=50*PERCENT, y= 40*PERCENT+yd)
button_comma = tkinter.Button(frame_2, command=comma_press)
button_comma.config(image=image_comma, width=str(image_comma.width()), height=str(image_comma.height()))
button_comma.place(x=50*PERCENT, y= 540*PERCENT+yd)
button_c = tkinter.Button(frame_2, command=c_press)
button_c.config(image=image_c, width=str(image_c.width()), height=str(image_c.height()))
button_c.place(x=450*PERCENT, y= 540*PERCENT+yd)

while True:
    t1 = time.time()
    a_fps = round(1/(t1-t2))
    t2 = time.time()
    if ((1/FPS)-(t1-t2))>0: time.sleep((1/FPS)-(t1-t2))

    if running == True:
        try:
            label1.config(text="FPS: "+str(a_fps))

            ref_label.config(text=REFERENCE_LABEL)

            ## Code here

            if first == True:
                ## Window initialisation

                first = False
            pass
            tk.update()
        except Exception as e:
            print("-- missed frame --")
            print(e)
            time.sleep(1/FPS)
    else:
        print("-- program ended --")
        break
