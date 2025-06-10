#!/bin/python

# This script was thrown together by FoofooTheGuy
# https://github.com/FoofooTheGuy
# All sources have been linked in a comment

import tkinter as tk
import socketserver
import urllib.parse
import http.server
import pathlib
import atexit
import qrcode
import shutil
import time
import os

from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

from tkinterdnd2 import DND_FILES, TkinterDnD

from http.server import HTTPServer, SimpleHTTPRequestHandler

IP_ADDRESS=''
PORT='8000'
CHOSEN_FILE=''
DIRECTORY='QRLS_temp'
RUNNING=0

#dir where we will put the files and start the server
try:
    shutil.rmtree(DIRECTORY)
except:
    pass
os.mkdir(DIRECTORY)

#https://stackoverflow.com/a/3850271
def exit_handler():
    try:
        shutil.rmtree(DIRECTORY)
    except:
        print('no directory')

atexit.register(exit_handler)

root = TkinterDnD.Tk()# Now working with drag and drop
root.geometry('500x300')
root.title('QR LAN share')


#save placeholder image
img = Image.new('RGB', (1, 1), (255, 255, 255))
img.save(DIRECTORY + '/ServerFileQRCode.png')


#https://www.w3resource.com/python-exercises/python-basic-exercise-55.php
def getIP():
    # Import the 'socket' module to work with network-related functions.
    import socket

    # The following code retrieves the local IP address of the current machine:
    # 1. Use 'socket.gethostname()' to get the local hostname.
    # 2. Use 'socket.gethostbyname_ex()' to get a list of IP addresses associated with the hostname.
    # 3. Filter the list to exclude any IP addresses starting with "127." (loopback addresses).
    # 4. Extract the first IP address (if available) from the filtered list.
    # 5. Print the obtained IP address to the console.

    # Step 1: Get the local hostname.
    local_hostname = socket.gethostname()

    # Step 2: Get a list of IP addresses associated with the hostname.
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]

    # Step 3: Filter out loopback addresses (IPs starting with "127.").
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]

    # Step 4: Extract the first IP address (if available) from the filtered list.
    first_ip = filtered_ips[:1]

    # Step 5: Print the obtained IP address to the console.
    global IP_ADDRESS
    IP_ADDRESS=first_ip[0]

#update the QR code image
def updateImage():
    global DIRECTORY
    
    global image
    global copy_of_image
    global photo
    
    image = Image.open(DIRECTORY + '/ServerFileQRCode.png')
    copy_of_image = image.copy()
    photo = ImageTk.PhotoImage(image)
    QRcode.config(image = photo)
    QRcode.image = photo

#https://stackoverflow.com/a/74162322
def tksleep(t):
    'emulating time.sleep(seconds)'
    ms = int(t)
    root = tk._get_default_root('sleep')
    var = tk.IntVar(root)
    root.after(ms, var.set, 1)
    root.wait_variable(var)

def handleServer():    
    global IP_ADDRESS
    global PORT
    global DIRECTORY
    global RUNNNING

    startButton.config(text = 'Server started')
    
    tksleep(300)# wait for the gui to update ;-;
    
    #https://stackoverflow.com/a/42763796
    try:
        RUNNING = 1
        #https://stackoverflow.com/a/52531444
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)
            
        with socketserver.TCPServer((IP_ADDRESS, int(PORT)), Handler) as httpd:
            print('Do a Keyboard Interrupt (CTRL + C) to close the server')
            print('Server started at ' + IP_ADDRESS + ':' + PORT)
            httpd.serve_forever()
    except KeyboardInterrupt:# CTRL + C
        print()
        print('Closing server')
        httpd.shutdown()
        
        img = Image.new('RGB', (1, 1), (255, 255, 255))
        img.save(DIRECTORY + '/ServerFileQRCode.png')
        
        updateImage()
        
        RUNNING = 0
        
        startButton.config(text = 'Start server')



def startServer():
    global IP_ADDRESS
    global PORT
    global RUNNING
    
    if(RUNNING == 0):
        startButton.config(text = 'Server starting...')
    elif(RUNNING == 1):
        return
    
    getIP()
    print(IP_ADDRESS)
    PORT = portEntry.get()
    print(PORT)
    
    #https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1, box_size = 1, border = 2, error_correction=qrcode.constants.ERROR_CORRECT_M)

    # Adding data to the instance 'qr'
    qr.add_data('http://' + IP_ADDRESS + ':' + PORT + '/tmp.cia')

    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black', back_color = 'white')

    img.save(DIRECTORY + '/ServerFileQRCode.png')
    
    updateImage()
    
    print('Starting server in 5 seconds...')
    tksleep(1000)
    print('Starting server in 4 seconds...')
    tksleep(1000)
    print('Starting server in 3 seconds...')
    tksleep(1000)
    print('Starting server in 2 seconds...')
    tksleep(1000)
    print('Starting server in 1 seconds...')
    tksleep(1000)
    handleServer()
    
    

def setChosenFile(filename):
    global CHOSEN_FILE
    
    #delete old temp file
    try:
        pathlib.Path.unlink(DIRECTORY + '/tmp.cia')
    except:
        pass
    
    CHOSEN_FILE = filename.strip('{}')
    print(CHOSEN_FILE)
    #make a temporary copy of the file to our directory
    shutil.copyfile(CHOSEN_FILE, DIRECTORY + '/tmp.cia')
    #https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-text/
    fileLabel.config(text = 'File: ' + CHOSEN_FILE)



def browseFiles():
    filename = filedialog.askopenfilename()
    setChosenFile(filename)



#https://stackoverflow.com/a/36333014
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width if new_width < new_height else new_height, new_width if new_width < new_height else new_height))
    photo = ImageTk.PhotoImage(image)
    QRcode.config(image = photo)
    QRcode.image = photo #avoid garbage collection



#https://www.geeksforgeeks.org/python-gui-tkinter/

menu = Menu(root)
root.config(menu=menu)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')
helpmenu.add_separator()
helpmenu.add_command(label='Exit', command=root.quit)

fileLabel = Label(root, text='File:')
fileLabel.pack()

browseButton = tk.Button(root, text='Browse', command=browseFiles)
#Stuff for drag and drop
browseButton.drop_target_register(DND_FILES)
browseButton.dnd_bind('<<Drop>>', lambda e: setChosenFile(e.data))
browseButton.pack()

Label(root, text='Port:').pack()

#https://www.reddit.com/r/learnpython/comments/985umy/comment/i9qd024/
# function to validate mark entry
def only_numbers(char):
    return char.isdigit()

validation = root.register(only_numbers)

#text box to enter marks
portEntry=Entry(root, validate="key", validatecommand=(validation, '%S'), justify='center')
portEntry.insert(END, PORT) # https://stackoverflow.com/a/20126024
portEntry.pack()

startButton = Button(root, text='Start Server', command=startServer)
startButton.pack()

#https://stackoverflow.com/a/36333014
image = Image.open(DIRECTORY + '/ServerFileQRCode.png')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
QRcode = ttk.Label(root, image = photo)
QRcode.bind('<Configure>', resize_image)
QRcode.pack()

mainloop()
