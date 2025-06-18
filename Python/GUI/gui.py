import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from MainInputsWidget.main_inputs_widget import MainInputsWidget


class GUI:
    def __init__(self):
        self.main_window()
        # self.running = True #want to implement a start and stop button
        
    def main_window(self):
        self.root = ctk.CTk()   #create main window
        self.root.title("Ignition")     #name of the window
        ctk.set_appearance_mode("dark") #set default theme to dark. Will add ability to change later
        self.root._state_before_windows_set_titlebar_color = 'zoomed' #fullscreen the window
        
        #Creates the mains tabs of Ignition and then assigns them to variables. Makes things easier to type later
        tabs = ctk.CTkTabview(self.root, width=300, height=300, anchor="w") #anchor='w' make them left aligned
        tabs.pack(padx=20, pady=20, anchor="w",expand=True,fill='both')
        tabs.add("Main")
        tabs.add("Settings")
        maintab = tabs.tab("Main")
        settingstab = tabs.tab("Settings")  #may add more later
        
        settings_frame1 = ctk.CTkFrame(settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        set_plotlabel = ctk.CTkLabel(settings_frame1,text='Plot Color',font=("Courier New Bold", 25))
        set_plotlabel.pack(padx=10, pady=10, anchor="w")

        leftframe = ctk.CTkFrame(maintab,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        leftframe.grid(row=0,column=0, padx=10, pady=10, sticky="nsew") 
        rightframe = ctk.CTkFrame(maintab,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        rightframe.grid(row=0,column=1, padx=10, pady=10, sticky="nsew")
        maintab.grid_columnconfigure(0,weight=3)
        maintab.grid_columnconfigure(1,weight=2)
        maintab.grid_rowconfigure(0,weight=1)
        
        #rows for the labels and the bottom buttons. want them to be smaller than the inputs
        leftframe.grid_rowconfigure(0,weight=1)
        leftframe.grid_rowconfigure(2,weight=1)
        leftframe.grid_rowconfigure(4,weight=0)
        
        #rows for the input frames. Want them to be a bit larger than the labels
        leftframe.grid_rowconfigure(1,weight=2)
        leftframe.grid_rowconfigure(3,weight=2)
        leftframe.grid_columnconfigure(0,weight=1)
        inputsframe = ctk.CTkFrame(leftframe)
        inputsframe.grid(row=1,column=0, padx=10, pady=10, sticky="nsew")
        
        
        #made a separate frame for the start, stop and reset buttons
        leftframe_bottom = ctk.CTkFrame(leftframe,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        leftframe_bottom.grid(row=4,column=0, padx=10, pady=10, sticky="nsew") 
        leftframe_bottom.grid_rowconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(1,weight=1)
        leftframe_bottom.grid_columnconfigure(2,weight=1)
        
        geninputslabel = ctk.CTkLabel(leftframe,text="General Inputs",font=("Courier New Bold", 25))
        geninputslabel.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
        combustionlabel = ctk.CTkLabel(leftframe,text="Combustion Inputs",font=("Courier New Bold", 25))
        combustionlabel.grid(row=2,column=0,padx=10,pady=10,sticky="ew")
        
        #Right frame will contain the plots for the geometry, temp, pressure, and mach number vs axial distance
        rightframe.grid_columnconfigure(0,weight=1)
        rightframe.grid_rowconfigure(0,weight=2)
        rightframe.grid_rowconfigure(1,weight=1)
        rightframe.grid_rowconfigure(2,weight=1)
        
        
        #all values with 1 are incomplete. Recheck units as I want to make them base SI instead of weird numbers like in matlab
        input_widgets = [
            {'label': "Gamma", "value":1.4, "units": ""},
            {'label': "R", "value":287, "units": "J/(kg*K)"},
            {'label': "Air Density", "value":1.225, "units": "kg/m^3"},
            {'label': "EGT", "value":800, "units": "C"},
            {'label': "Exit Velocity", "value":1200, "units": "km/hr"},
            {'label': "Blowout Velocity Parameter", "value":1, "units": ""},
            {'label': "Ignition Time Parameter", "value":1, "units": ""},
            {'label': "Mass Flow In", "value":1, "units": "L/s"},
            {'label': "Turbine Blade Length", "value":1, "units": "m"},
            {'label': "Diffuser Length", "value":1, "units": "m"},
            {'label': "Straight Section Length", "value":1, "units": "m"},
            {'label': "Flame Holder Half Angle", "value":15, "units": "degrees"},
            {'label': "Nozzle Diameter", "value":1, "units": "mm"},
            {'label': "Turbine Diameter", "value":1, "units": "mm"},
            {'label': "Mass Flow Fuel", "value":1, "units": "g/min"},
            # {'label': "Blank", "value":1, "units": "Blank"},    #3 placeholders for now, might not need?
            # {'label': "Blank", "value":1, "units": "Blank"},
            # {'label': "Blank", "value":1, "units": "Blank"},
        ]
        inputs_per_column = 6
        widget_instances = []
        for i, inp in  enumerate(input_widgets):
            col = i // inputs_per_column
            row = i % inputs_per_column
            grid_col = col*3
            widget = MainInputsWidget(inputsframe, value=str(inp["value"]),label_front=inp["label"], label_rear=inp["units"])
            widget.grid(row = row,column=grid_col)
            widget_instances.append(widget)
        
        num_input_col = ((len(input_widgets) + inputs_per_column - 1) // inputs_per_column) * 3
        for c in range(num_input_col):
            if c%3 ==1:
                inputsframe.grid_columnconfigure(c, weight=1)
            else:
                inputsframe.grid_columnconfigure(c, weight=0)

        startbutton = ctk.CTkButton(leftframe_bottom,text="Start",command=None) #implement start function later
        startbutton.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        stopbutton = ctk.CTkButton(leftframe_bottom,text="Stop",command=None) #implement stop function later
        stopbutton.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
        resetbutton = ctk.CTkButton(leftframe_bottom,text="Reset",command=None) #implement reset function later
        resetbutton.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")
        
        
        # Add debug visualization to show frame boundaries
        def add_debug_borders():
            # Make all frames visible with colored borders for debugging
            for widget in self.root.winfo_children():
                if isinstance(widget, ctk.CTkTabview):
                    for tab_name in widget._tab_dict:
                        tab = widget.tab(tab_name)
                        for child in tab.winfo_children():
                            if isinstance(child, ctk.CTkFrame):
                                child.configure(border_width=3, border_color="red")
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, ctk.CTkFrame):
                                        grandchild.configure(border_width=2, border_color="blue")
                                        for ggchild in grandchild.winfo_children():
                                            if isinstance(ggchild, ctk.CTkFrame):
                                                ggchild.configure(border_width=1, border_color="green")

        add_debug_borders()
        self.root.mainloop() #runs the main loop
        
        