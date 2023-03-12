import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

class MyGUI:
    #Main Method (Calls itself)
    def __init__(self):
        #Xbee Portion of Program (Receives the data and sets it to variables, change com port and baud rate as needed in XCTU)
        #Helpful links: https://xbplib.readthedocs.io/en/latest/user_doc/communicating_with_xbee_devices.html
        #https://github.com/digidotcom/xbee-python/tree/master/examples/communication/ReceiveDataSample
        #Instantiate xbee radio node
        '''xbee = XBeeDevice("COM1", 9600)
        xbee.open()
        #Xbee Callback method that listens for xbee devices and when data is received, save the data as variables
        def data_receive_callback(xbee_message):
            address = xbee_message.remote_device.get_64bit_addr()
            data = xbee_message.data.decode("utf8")
            sensnum, pressure, temp, humidity, solvolt, gpstime, gpslat, gpslong, gpsspeed, gpsalt, gpsangle, gpsfix, gpssat = data
            print("Received data from %s: %s" % (address, data))
        #Adds the callback
        xbee.add_data_received_callback(data_receive_callback)'''

        #Tkinter Portion of Program
        self.root = tk.Tk()

        #Default visual variables that can be changed
        self.root.geometry("500x500")
        self.root.title("UVA BOTR Ground Station V0.1")
        defaultfont = ('Arial', 18)

        #Main label for top of program, change for every flight test
        self.label = tk.Label(self.root, text = "BOTR Flight Test 1", font = defaultfont)
        self.label.pack(padx=10, pady=10)

        #graph frame for the four matplotlib graphs
        graphframe = tk.Frame(self.root)
        graphframe.columnconfigure(0, weight = 1)
        graphframe.columnconfigure(1, weight = 1)
        graphframe.columnconfigure(2, weight = 1)
        graphframe.columnconfigure(3, weight = 1)
        graphframe.columnconfigure(4, weight = 1)
        graphframe.columnconfigure(5, weight = 1)
        graphframe.columnconfigure(6, weight = 1)
        graphframe.columnconfigure(7, weight = 1)

        btn1 = tk.Label(graphframe, text = "Altitude:", font = defaultfont)
        btn1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        btn2 = tk.Frame(graphframe, background="#99fb99", height=60)
        btn2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        btn3 = tk.Label(graphframe, text = "Apogee:", font = defaultfont)
        btn3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        btn4 = tk.Frame(graphframe, background="#99fb99", height=60)
        btn4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        btn5 = tk.Label(graphframe, text = "Status:", font = defaultfont)
        btn5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        btn6 = tk.Frame(graphframe, background="#99fb99", height=60)
        btn6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        btn7 = tk.Label(graphframe, text = "Velocity:", font = defaultfont)
        btn7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        btn8 = tk.Frame(graphframe, background="#99fb99", height=60)
        btn8.grid(row = 0, column = 7, sticky = tk.W+tk.E)

        btn9 = tk.Button(graphframe, text = "1", font = defaultfont)
        btn9.grid(row = 1, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn10 = tk.Button(graphframe, text = "2", font = defaultfont)
        btn10.grid(row = 1, column = 2, sticky = tk.W+tk.E)

        btn11 = tk.Button(graphframe, text = "3", font = defaultfont)
        btn11.grid(row = 2, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn12 = tk.Button(graphframe, text = "4", font = defaultfont)
        btn12.grid(row = 2, column = 2, sticky = tk.W+tk.E)

        btn13 = tk.Button(graphframe, text = "5", font = defaultfont)
        btn13.grid(row = 3, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn14 = tk.Button(graphframe, text = "6", font = defaultfont)
        btn14.grid(row = 3, column = 2, sticky = tk.W+tk.E)

        graphframe.pack(fill = 'x')

        #main loop and exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    #Closing Method (Asks user if they really want to close the window)
    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit?")):
            self.root.destroy()
   
MyGUI()     
    

    