#!/usr/bin/env python3

"""
sudo apt update
sudo apt-get install python-imaging
sudo apt-get install python-imaging python-imaging-tk

os.system("export DISPLAY=:0")
"""

GUI_DEBUG_MODE = False

import os
import tkinter
import time
import socket
from PIL import Image, ImageTk
from tkinter import messagebox

if not GUI_DEBUG_MODE:
    from ph_manage import *
    time.sleep(3)  # wait for server to start

reference_number_string = ""
measurement_state = "EMPTY"

tk = tkinter.Tk()
tk.title("Photometer")
tk.attributes('-fullscreen', True)

if not GUI_DEBUG_MODE:
    MAIN_PATH = "/home/pi/Photometer"
else:
    MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

HOST = 'localhost'
PORT = 5000
WIDTH = tk.winfo_screenwidth()
HEIGHT = tk.winfo_screenheight()
PERCENT = WIDTH / 1040
Y_DIFF = 8

GRAY_LIGHT = '#434243'
GRAY_DARK = '#323232'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if not GUI_DEBUG_MODE:
    connected = False
    while not connected:
        try:
            server_socket.connect((HOST, PORT))
            connected = True
        except Exception as e:
            pass


class DigitButtonManager(object):
    def __init__(self, image_manager, frame):
        self.buttons = []
        self.image_manager = image_manager
        self.frame = frame
        self.create_buttons()

    def create_buttons(self):
        self.buttons.append(self.create_button(0, x=250 * PERCENT, y=540 * PERCENT + Y_DIFF, string="0"))
        self.buttons.append(self.create_button(1, x=450 * PERCENT, y=380 * PERCENT + Y_DIFF, string="1"))
        self.buttons.append(self.create_button(2, x=250 * PERCENT, y=380 * PERCENT + Y_DIFF, string="2"))
        self.buttons.append(self.create_button(3, x=50 * PERCENT, y=380 * PERCENT + Y_DIFF, string="3"))
        self.buttons.append(self.create_button(4, x=450 * PERCENT, y=205 * PERCENT + Y_DIFF, string="4"))
        self.buttons.append(self.create_button(5, x=250 * PERCENT, y=205 * PERCENT + Y_DIFF, string="5"))
        self.buttons.append(self.create_button(6, x=50 * PERCENT, y=205 * PERCENT + Y_DIFF, string="6"))
        self.buttons.append(self.create_button(7, x=450 * PERCENT, y=40 * PERCENT + Y_DIFF, string="7"))
        self.buttons.append(self.create_button(8, x=250 * PERCENT, y=40 * PERCENT + Y_DIFF, string="8"))
        self.buttons.append(self.create_button(9, x=50 * PERCENT, y=40 * PERCENT + Y_DIFF, string="9"))

    def create_button(self, digit, x=0, y=0, string="") -> object:
        button = tkinter.Button(self.frame, command=self.create_button_function(string))
        button.config(image=self.image_manager.button_images[digit],
                      width=str(self.image_manager.button_images[digit].width()),
                      height=str(self.image_manager.button_images[digit].height()))
        button.place(x=x, y=y)
        return button

    @staticmethod
    def create_button_function(string):
        def func():
            global reference_number_string
            reference_number_string += string
            refresh_ref_label(reference_number_string)

        return func


class ImageManager(object):
    def __init__(self):
        self.button_images = []

        for i in range(10):
            self.button_images.append(ImageTk.PhotoImage(self.resize_image(
                Image.open(MAIN_PATH + "/images/" + str(i) + ".png"))))

        self.image_comma = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/comma.png")))
        self.image_c = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/c.png")))

        self.start_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/start.png")))
        self.start_pressed_img = ImageTk.PhotoImage(self.resize_image(
            Image.open(MAIN_PATH + "/images/start_pressed.png")))
        self.exit_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/exit.png")))
        self.exit_pressed_img = ImageTk.PhotoImage(self.resize_image(
            Image.open(MAIN_PATH + "/images/exit_pressed.png")))
        self.radio_green_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/g.png")))
        self.radio_blue_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/b.png")))
        self.radio_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/radio.png")))
        self.background_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/back.png")))

        self.ref_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/ref.png")))
        self.enter_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/enter.png")))
        self.ref_label_img = ImageTk.PhotoImage(self.resize_image(Image.open(MAIN_PATH + "/images/ref_label.png")))

    @staticmethod
    def resize_image(image):
        new_image = image.resize((int(image.size[0] * PERCENT), int(image.size[1] * PERCENT)), Image.ANTIALIAS)
        return new_image


def start_button_press():
    start_button.config(image=image_manager.start_pressed_img)
    time.sleep(0.1)
    start_button.config(image=image_manager.start_img)

    text_label.config(text="measurement_state IN PROGRESS...")

    if sum(cha == "." for cha in reference_number_string) > 1 or reference_number_string == ".":
        text_label.config(text="REFERENCE VALUE INCORRECT!\n" +
                               "TOO MANY DOTS")
        return

    if measurement_state == "EMPTY":
        data, extinction = doEmptyMeasurement(server_socket, "Leermessung")
        server_socket.sendall(('colors/255/0/0/635/' +
                               str(round(data[0], 3)) + '/0/255/0/525/' +
                               str(round(data[1], 3)) + '/0/0/255/471/' +
                               str(round(data[2], 3)) + '\n').encode())

        text_label.config(text="EMPTY INTENSITIES:\n\n" +
                               "  RED: " + str(round(data[0], 3)) +
                               " Lux  \nGREEN: " + str(round(data[1], 3)) +
                               " Lux  \n BLUE: " + str(round(data[2], 3)) + " Lux  ")

    elif measurement_state == "REFERENCE":
        if reference_number_string != "":
            data_INT, data_EXT, data_COE, success = doReferenceMeasurement(float(str(reference_number_string)),
                                                                           server_socket,
                                                                           "Referenzmessung")
            if success:
                server_socket.sendall(('reference/' +
                                       str(reference_number_string) + '/' +
                                       str(round(data_INT[0], 3)) + '/' +
                                       str(round(data_EXT[0], 3)) + '/' +
                                       str(round(data_COE[0], 3)) + '/' +
                                       str(round(data_INT[1], 3)) + '/' +
                                       str(round(data_EXT[1], 3)) + '/' +
                                       str(round(data_COE[1], 3)) + '/' +
                                       str(round(data_INT[2], 3)) + '/' +
                                       str(round(data_EXT[2], 3)) + '/' +
                                       str(round(data_COE[2], 3)) + '\n').encode())

                text_label.config(text="REFERENCE INTENSITIES:\n\n" +
                                       "  RED: " + str(round(data_INT[0], 3)) +
                                       " Lux  \nGREEN: " + str(round(data_INT[1], 3)) +
                                       " Lux  \n BLUE: " + str(round(data_INT[2], 3)) + " Lux  ")
            else:
                text_label.config(text="measurement_state FAILED!\n\n" +
                                       "DO EMPTY measurement_state AND\n" +
                                       "ENTER REFERENCE CONCENTRATION\n" +
                                       "THEN TRY AGAIN.")
        else:
            text_label.config(text="measurement_state FAILED!\n\n" +
                                   "DO EMPTY measurement_state AND\n" +
                                   "ENTER REFERENCE CONCENTRATION\n" +
                                   "THEN TRY AGAIN.")

    elif measurement_state == "NORMAL":
        data_INT, data_EXT, data_CON, success = doOrdinaryMeasurement(server_socket, "Normalmessung")
        if success:
            server_socket.sendall(('measurements/' +
                                   str(round(data_INT[0], 3)) + '/' +
                                   str(round(data_EXT[0], 3)) + '/' +
                                   str(round(data_CON[0], 3)) + '/' +
                                   str(round(data_INT[1], 3)) + '/' +
                                   str(round(data_EXT[1], 3)) + '/' +
                                   str(round(data_CON[1], 3)) + '/' +
                                   str(round(data_INT[2], 3)) + '/' +
                                   str(round(data_EXT[2], 3)) + '/' +
                                   str(round(data_CON[2], 3)) + '\n').encode())

            text_label.config(text="CONCENTRATIONS:\n" +
                                   "  RED: " + str(round(data_CON[0], 3)) + " mol/L  \n" +
                                   "GREEN: " + str(round(data_CON[1], 3)) + " mol/L  \n" +
                                   " BLUE: " + str(round(data_CON[2], 3)) + " mol/L  \n" +
                                   "AVERAGE:       " + str(
                                       round(((data_CON[0] + data_CON[1] + data_CON[2]) / 3), 3)) + " mol/L")
        else:
            text_label.config(text="measurement_state FAILED!\n\n" +
                                   "ENTER REFERENCE CONCENTRATION\n" +
                                   "AND DO REFERENCE measurement_state.\n" +
                                   "THEN TRY AGAIN.")
    time.sleep(0.1)


def exit_button_press():
    exit_button.config(image=image_manager.exit_pressed_img)
    time.sleep(0.1)
    exit_button.config(image=image_manager.exit_img)
    shutdown = messagebox.askyesnocancel(title="EXIT", message="Do you want to shutdown?")

    if shutdown:
        close_window()
        os.system("sudo shutdown -h now")
    elif not shutdown:
        close_window()


def ref_value_press():
    frame_1.pack_forget()
    frame_2.pack(side="top", fill="both", expand=True)


def comma_press():
    global reference_number_string
    reference_number_string += "."
    refresh_ref_label(reference_number_string)


def c_press():
    global reference_number_string
    reference_number_string = ""
    refresh_ref_label(reference_number_string)


def refresh_ref_label(reference_string):
    ref_label.config(text=reference_string)


def enter_press():
    frame_2.pack_forget()
    frame_1.pack(side="top", fill="both", expand=True)


def radio_button_press_1():
    global measurement_state
    measurement_state = "EMPTY"
    radio_button_1.config(image=image_manager.radio_blue_img)
    radio_button_2.config(image=image_manager.radio_green_img)
    radio_button_3.config(image=image_manager.radio_green_img)


def radio_button_press_2():
    global measurement_state
    measurement_state = "REFERENCE"
    radio_button_1.config(image=image_manager.radio_green_img)
    radio_button_2.config(image=image_manager.radio_blue_img)
    radio_button_3.config(image=image_manager.radio_green_img)


def radio_button_press_3():
    global measurement_state
    measurement_state = "NORMAL"
    radio_button_1.config(image=image_manager.radio_green_img)
    radio_button_2.config(image=image_manager.radio_green_img)
    radio_button_3.config(image=image_manager.radio_blue_img)


def close_window(event=0):
    tk.destroy()


tk.protocol("WM_DELETE_WINDOW", close_window)
tk.bind("<Command-q>", close_window)
tk.bind("<Command-w>", close_window)


# ---------- FRAME 1 -----------

frame_1 = tkinter.Frame(tk, width=WIDTH, height=HEIGHT)
frame_1.pack(side="top", fill="both", expand=True)

frame_2 = tkinter.Frame(tk, width=WIDTH, height=HEIGHT)

# load all images into the image_manager:
image_manager = ImageManager()

start_button = tkinter.Button(master=frame_1,
                              command=start_button_press,
                              image=image_manager.start_img,
                              width=str(image_manager.start_img.width()),
                              height=str(image_manager.start_img.height()))
start_button.place(x=33 * PERCENT, y=36 * PERCENT)

exit_button = tkinter.Button(master=frame_1,
                             command=exit_button_press,
                             image=image_manager.exit_img,
                             width=str(image_manager.exit_img.width()),
                             height=str(image_manager.exit_img.height()))
exit_button.place(x=33 * PERCENT, y=240 * PERCENT)

ref_button = tkinter.Button(master=frame_1,
                            command=ref_value_press,
                            image=image_manager.ref_img,
                            width=str(image_manager.ref_img.width()),
                            height=str(image_manager.ref_img.height()))
ref_button.place(x=288 * PERCENT, y=240 * PERCENT)

radio_label = tkinter.Label(master=frame_1,
                            image=image_manager.radio_img,
                            width=str(image_manager.radio_img.width()),
                            height=str(image_manager.radio_img.height()))
radio_label.place(x=544 * PERCENT, y=37 * PERCENT)

radio_button_1 = tkinter.Button(master=frame_1,
                                command=radio_button_press_1,
                                highlightthickness=0,
                                bg=GRAY_LIGHT,
                                image=image_manager.radio_blue_img,
                                width=str(image_manager.radio_blue_img.width()),
                                height=str(image_manager.radio_blue_img.height()))
radio_button_1.place(x=573 * PERCENT, y=66 * PERCENT)

radio_button_2 = tkinter.Button(master=frame_1,
                                command=radio_button_press_2,
                                highlightthickness=0,
                                bg=GRAY_LIGHT,
                                image=image_manager.radio_green_img,
                                width=str(image_manager.radio_green_img.width()),
                                height=str(image_manager.radio_green_img.height()))
radio_button_2.place(x=573 * PERCENT, y=165 * PERCENT)

radio_button_3 = tkinter.Button(master=frame_1,
                                command=radio_button_press_3,
                                highlightthickness=0,
                                bg=GRAY_LIGHT,
                                image=image_manager.radio_green_img,
                                width=str(image_manager.radio_green_img.width()),
                                height=str(image_manager.radio_green_img.height()))
radio_button_3.place(x=573 * PERCENT, y=266 * PERCENT)

textfield_label = tkinter.Label(master=frame_1,
                                image=image_manager.background_img,
                                width=str(image_manager.background_img.width()),
                                height=str(image_manager.background_img.height()))
textfield_label.place(x=35 * PERCENT, y=408 * PERCENT)

text_label = tkinter.Label(master=frame_1,
                           bg=GRAY_LIGHT,
                           font=("Avenir Next", int(25 * PERCENT)),
                           fg="white",
                           width=40)
text_label.place(x=135 * PERCENT, y=425 * PERCENT)

# ---------- FRAME 2 -----------

# create digit buttons for number input:
digit_button_manager = DigitButtonManager(image_manager, frame_2)

enter_button = tkinter.Button(master=frame_2,
                              command=enter_press,
                              image=image_manager.enter_img,
                              width=str(image_manager.enter_img.width()),
                              height=str(image_manager.enter_img.height()))
enter_button.place(x=640 * PERCENT, y=540 * PERCENT + Y_DIFF)

ref_label_i = tkinter.Label(master=frame_2,
                            image=image_manager.ref_label_img,
                            width=str(image_manager.ref_label_img.width()),
                            height=str(image_manager.ref_label_img.height()))
ref_label_i.place(x=640 * PERCENT, y=40 * PERCENT + Y_DIFF)

ref_label = tkinter.Label(master=frame_2,
                          bg=GRAY_DARK,
                          font=("Courier", int(52 * PERCENT)),
                          fg="white",
                          width=7)
ref_label.place(x=669.5 * PERCENT, y=73 * PERCENT + Y_DIFF)

button_comma = tkinter.Button(master=frame_2,
                              command=comma_press,
                              image=image_manager.image_comma,
                              width=str(image_manager.image_comma.width()),
                              height=str(image_manager.image_comma.height()))
button_comma.place(x=50 * PERCENT, y=540 * PERCENT + Y_DIFF)

button_c = tkinter.Button(master=frame_2,
                          command=c_press,
                          image=image_manager.image_c,
                          width=str(image_manager.image_c.width()),
                          height=str(image_manager.image_c.height()))
button_c.place(x=450 * PERCENT, y=540 * PERCENT + Y_DIFF)

tk.mainloop()
