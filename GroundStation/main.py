import tkinter as tk
import sv_ttk
from tkinter import ttk
from tkinter import messagebox
#from tkinter import filedialog
#from tkinter.filedialog import asksaveasfile

class MyGUI:
    #Main Method (Calls itself)
    def __init__(self):
        #Tkinter Portion of Program
        self.root = tk.Tk()

        #Default visual variables that can be changed
        self.root.geometry("500x500")
        self.root.title("UVA BOTR Ground Station V0.1")
        defaultfont = ('Arial', 18)

        #Main label for top of program, change for every flight test
        self.label = tk.Label(self.root, text = "BOTR Flight Test", font = defaultfont)
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
        graphframe.columnconfigure(8, weight = 1)
        graphframe.columnconfigure(9, weight = 1)
        graphframe.columnconfigure(10, weight = 1)
        graphframe.columnconfigure(11, weight = 1)

        space1 = tk.Label(graphframe, text = "State:", font = defaultfont)
        space1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        space2 = tk.Frame(graphframe, background="#99fb99", height=60)
        space2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        space3 = tk.Label(graphframe, text = "Altitude:", font = defaultfont)
        space3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        space4 = tk.Frame(graphframe, background="#99fb99", height=60)
        space4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        space5 = tk.Label(graphframe, text = "Apogee", font = defaultfont)
        space5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        space6 = tk.Frame(graphframe, background="#99fb99", height=60)
        space6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        space7 = tk.Label(graphframe, text = "Velocity:", font = defaultfont)
        space7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        space8 = tk.Frame(graphframe, background="#99fb99", height=60)
        space8.grid(row = 0, column = 7, sticky = tk.W+tk.E)
        space9 = tk.Label(graphframe, text = "Angle:", font = defaultfont)
        space9.grid(row = 0, column = 8, sticky = tk.W+tk.E)
        space10 = tk.Frame(graphframe, background="#99fb99", height=60)
        space10.grid(row = 0, column = 9, sticky = tk.W+tk.E)
        space11 = tk.Label(graphframe, text = "Satellites:", font = defaultfont)
        space11.grid(row = 0, column = 10, sticky = tk.W+tk.E)
        space12 = tk.Frame(graphframe, background="#99fb99", height=60)
        space12.grid(row = 0, column = 11, sticky = tk.W+tk.E)

        graphframe.pack(fill = 'x')

        anotherFrame = tk.Frame(self.root)
        anotherFrame.columnconfigure(0, weight = 1)
        anotherFrame.columnconfigure(1, weight = 1)


        btn9 = tk.Button(anotherFrame, text = "1", font = defaultfont)
        btn9.grid(row = 1, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn10 = tk.Button(anotherFrame, text = "2", font = defaultfont)
        btn10.grid(row = 1, column = 1, sticky = tk.W+tk.E)

        btn11 = tk.Button(anotherFrame, text = "3", font = defaultfont)
        btn11.grid(row = 2, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn12 = tk.Button(anotherFrame, text = "4", font = defaultfont)
        btn12.grid(row = 2, column = 1, sticky = tk.W+tk.E)

        anotherFrame.pack(fill = 'x')

        button = ttk.Button(self.root, text = "CLICK ME!")
        button.pack(fill = 'x')
        
        #light/dark mode
        sv_ttk.set_theme("light")

        #main loop and exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    #Closing Method (Asks user if they really want to close the window)
    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit?")):
            self.root.destroy()
            #ser.close();
   
MyGUI()     
    

    