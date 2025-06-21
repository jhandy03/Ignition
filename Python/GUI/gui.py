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
        tabs = ctk.CTkTabview(self.root, width=300, height=300, anchor="w",border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b") #anchor='w' make them left aligned
        tabs.pack(padx=20, pady=20, anchor="w",expand=True,fill='both')
        tabs.add("Main")
        tabs.add("Unit Conversion Toolbox")
        tabs.add("Settings")
        maintab = tabs.tab("Main")
        settingstab = tabs.tab("Settings")  #may add more later
        
        settings_frame1 = ctk.CTkFrame(settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        set_plotlabel = ctk.CTkLabel(settings_frame1,text='Plot Color',font=("Courier New Bold", 25))
        set_plotlabel.pack(padx=10, pady=10, anchor="w")

        #Breaks the main window into frames and sets their weights
        leftframe = ctk.CTkFrame(maintab,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        leftframe.grid(row=0,column=0, padx=10, pady=10, sticky="nsew") 
        self.rightframe = ctk.CTkFrame(maintab,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        self.rightframe.grid(row=0,column=1, padx=10, pady=10, sticky="nsew")
        maintab.grid_columnconfigure(0,weight=1)
        maintab.grid_columnconfigure(1,weight=1)    #TODO: check the weights, things aren't working right atm
        maintab.grid_rowconfigure(0,weight=1)
        
        #rows for the labels and the bottom buttons. want them to be smaller than the inputs
        leftframe.grid_rowconfigure(0,weight=1)
        leftframe.grid_rowconfigure(2,weight=1)
        leftframe.grid_rowconfigure(4,weight=0)
        
        #rows for the input frames. Want them to be a bit larger than the labels
        leftframe.grid_rowconfigure(1,weight=2)
        leftframe.grid_rowconfigure(3,weight=2)
        leftframe.grid_columnconfigure(0,weight=1)
        inputsframe = ctk.CTkFrame(leftframe,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        inputsframe.grid(row=1,column=0, padx=10, pady=10, sticky="new")
        
        
        #made a separate frame for the start, stop and reset buttons
        leftframe_bottom = ctk.CTkFrame(leftframe,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        leftframe_bottom.grid(row=4,column=0, padx=10, pady=10, sticky="ns") 
        leftframe_bottom.grid_rowconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(1,weight=1)
        leftframe_bottom.grid_columnconfigure(2,weight=1)
        
    
        geninputslabel = ctk.CTkLabel(leftframe,text="General Inputs",font=("Courier New Bold", 20))
        geninputslabel.grid(row=0,column=0,padx=10,pady=10,sticky="new")
        combustionlabel = ctk.CTkLabel(leftframe,text="Combustion Inputs",font=("Courier New Bold", 20))
        combustionlabel.grid(row=2,column=0,padx=10,pady=0,sticky="new")
        
        #Right frame will contain the plots for the geometry, temp, pressure, and mach number vs axial distance
        self.rightframe.grid_columnconfigure(0,weight=1)
        self.rightframe.grid_rowconfigure(0,weight=2)
        self.rightframe.grid_rowconfigure(1,weight=1)
        self.rightframe.grid_rowconfigure(2,weight=1)
        
        
        #all values with 1 are incomplete. Recheck units as I want to make them base SI instead of weird numbers like in matlab
        input_widgets = [
            {'label': "Gamma", "value":1.4, "units": ""},
            {'label': "R", "value":287, "units": "J/(kg*K)"},
            {'label': "Air Density", "value":1.225, "units": "kg/m^3"},
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
        inputs_per_column = 7
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
            if c%2 ==1:
                inputsframe.grid_columnconfigure(c, weight=1)
            else:
                inputsframe.grid_columnconfigure(c, weight=0)

        startbutton = ctk.CTkButton(leftframe_bottom,text="Start",command=None) #implement start function later
        startbutton.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        stopbutton = ctk.CTkButton(leftframe_bottom,text="Stop",command=None) #implement stop function later
        stopbutton.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
        resetbutton = ctk.CTkButton(leftframe_bottom,text="Reset",command=None) #implement reset function later
        resetbutton.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")
        
        #combustion inputs frame. Not sure how I want to organize this entirely yet
        combframe = ctk.CTkFrame(leftframe,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        combframe.grid(row=3,column=0, padx=10, pady=10, sticky="new")
        combframe.grid_columnconfigure(0,weight=1)
        combframetop = ctk.CTkFrame(combframe)
        combframetop.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
        combframemiddle = ctk.CTkFrame(combframe)
        combframemiddle.grid(row=1,column=0,padx=10,pady=10,sticky="ew")
        combframemiddle.grid_columnconfigure(0,weight=1)
        
        fuel_label = ctk.CTkLabel(combframetop,text='Fuel Type',font=("Computer Modern", 15))
        fuel_label.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.fueldropdown = ctk.CTkOptionMenu(combframetop, values=["Jet-A","Propane","Butane","Methane"],command=self.update_combustion_equation,font=('Computer Modern',15)) #TODO: Finish later
        self.fueldropdown.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
        self.dissociation_checkbox = ctk.CTkCheckBox(combframetop,text="Dissociation",command=self.update_equation_values,font=('Computer Modern',15)) #TODO: Finish later
        self.dissociation_checkbox.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")
        
        combframeinputs = ctk.CTkFrame(combframemiddle,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        combframeinputs.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        combframeinputs.grid_rowconfigure(0,weight=1)
        for i in range(19):
            if i%2 == 1:
                combframeinputs.grid_columnconfigure(i, weight=2)
            else:
                combframeinputs.grid_columnconfigure(i,weight=1)
        self.create_combustion_inputs(combframeinputs)
        
        combframebottom = ctk.CTkFrame(combframe,border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b")
        combframebottom.grid(row=2,column=0,padx=10,pady=10,sticky="nsew")
        for i in range(6):
            if i%2==1:
                combframebottom.grid_columnconfigure(i, weight=1)
            else:
                combframebottom.grid_columnconfigure(i, weight=1)
        
        combustion_bottom_widgets = [
            {'label': "Exhaust Gas Temperature", "value": 1073.15, "units": "K"},
            {'label': "Exit Pressure", "value": 101325, "units": "Pa"},
        ]
        
        widget_instances_bottom = []
        for i, inp in enumerate(combustion_bottom_widgets):
            col = i * 3
            widget = MainInputsWidget(combframebottom, value=str(inp["value"]), label_front=inp["label"], label_rear=inp["units"])
            widget.grid(row=0, column=col)
            widget_instances_bottom.append(widget)
        
        # {'label': "EGT", "value":800, "units": "C"},
            

        #Plot stuff
        self.setup_plots(self.rightframe)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close) #handles closing the window properly
        self.root.mainloop() #runs the main loop
    
    
    def setup_plots(self, frame):
        frame.grid_rowconfigure(0,weight=1) #was going to make the geometry plot larger but looks bad
        frame.grid_rowconfigure(1,weight=1)
        frame.grid_rowconfigure(2,weight=1)
        self.setup_geometry_plot()
        self.setup_temp_pressure_plot()
        self.setup_mach_plot()
        
    def setup_geometry_plot(self):
        self.geometry_fig, self.geometry_ax = plt.subplots(figsize=(6,6.5)) #might need to pass in figsize if things are a big off
        self.geometry_ax.set_title("Afterburner Geometry")
        self.geometry_ax.set_xlabel("Axial Distance (m)")
        self.geometry_ax.set_ylabel("Radial Distance (m)")
        self.geometry_canvas = FigureCanvasTkAgg(self.geometry_fig, master=self.rightframe)
        self.geometry_canvas.get_tk_widget().grid(row=0, column=0,padx=10,pady=10, sticky="nsew")
        self.geometry_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
         
    def setup_temp_pressure_plot(self):
        self.temp_fig, self.temp_ax = plt.subplots()
        self.temp_ax.set_title("Temperature and Pressure vs Axial Distance")
        # self.temp_ax.set_xlabel("Axial Distance (m)") #gets cut off and I can't figure out a way to fit the label on every plot
        self.temp_ax.set_ylabel("Temperature (K)")
        
        self.pressure_ax = self.temp_ax.twinx()
        self.pressure_ax.set_ylabel("Pressure (Pa)")
        
        self.tp_canvas = FigureCanvasTkAgg(self.temp_fig, master =self.rightframe)
        self.tp_canvas.get_tk_widget().grid(row=1, column=0,padx=10,pady=10, sticky="nsew")
        self.temp_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
        
    def setup_mach_plot(self):
        self.mach_fig, self.mach_ax = plt.subplots()
        self.mach_ax.set_title("Mach Number vs Axial Distance")
        # self.mach_ax.set_xlabel("Axial Distance (m)")     #gets cut off and I can't figure out a way to fit the label on every plot
        self.mach_ax.set_ylabel("Mach Number")
        self.mach_canvas = FigureCanvasTkAgg(self.mach_fig, master=self.rightframe)
        self.mach_canvas.get_tk_widget().grid(row=2, column=0,padx=10,pady=10, sticky="nsew")
        self.mach_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
        
    def update_plots(self, geox, geoy, tempx, tempy, pressurex, pressurey, machx, machy):
        self.geometry_ax.clear()
        self.temp_ax.clear()
        self.pressure_ax.clear()
        self.mach_ax.clear()
        
        #comma tells python to only unpack the first element so it can be used in the legend
        #otherwise would return a massive list of all data
        #Not needed for geometry since it'll be the only thing on it's plot
        temp_data, = self.temp_ax.plot(tempx,tempy, color='red')
        pressure_data, = self.pressure_ax.plot(pressurex, pressurey, color='blue')
        mach_data, = self.mach_ax.plot(machx, machy, color='green')
        self.geometry_ax.plot(geox, geoy, color='black')
        
        self.temp_ax.legend([temp_data, pressure_data], ["Temperature (K)", "Pressure (Pa)"])
        self.mach_ax.legend([mach_data], ["Mach Number"])
        self.temp_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
        # self.pressure_ax.grid(True, linestyle='--', alpha=0.5) #needed?
        self.mach_ax.grid(True, linestyle='--', alpha=0.5)
        
        self.tp_canvas.draw()
        self.geometry_canvas.draw()
        self.mach_canvas.draw()
        
    def on_close(self):
        """
        Handles weird window closing behavior. Matplotlib doesn't
        like when you just close the window so this closes it properly.
        """
        self.root.quit()
        
    def update_equation_values(self):
        fuel_selection = self.fueldropdown.get()
        C, H = self.get_fuel_atoms(fuel_selection)
        
        if self.dissociation_checkbox.get():
            #TODO: Revise later
            mol_co2 = 1
            mol_h2o = 1
            mol_co = 1
            
            self.co2.delete(0, 'end')
            self.co2.insert(0, f"{mol_co2:.1f}")
            
            self.mol_water.delete(0, 'end')
            self.mol_water.insert(0, f"{mol_h2o:.1f}")
            
            # Show all CO components by putting them back in the grid
            self.plus_co_label.grid(row=0, column=20, padx=5, pady=5)
            self.co.grid(row=0, column=21, padx=5, pady=5)  # Show the CO entry field
            self.co_label.grid(row=0, column=22, padx=5, pady=5)
            
            # Update the CO value
            self.co.delete(0, 'end')
            self.co.insert(0, f"{mol_co:.1f}")
            
            # Restore normal appearance
            self.plus_co_label.configure(text_color=('white', 'white'))
        else:
            # Hide dissociation products
            mol_co2 = C
            mol_h2o = H
            
            self.co2.delete(0, 'end')
            self.co2.insert(0, f"{mol_co2:.1f}")
            
            self.mol_water.delete(0, 'end')
            self.mol_water.insert(0, f"{mol_h2o:.1f}")
            
            # Remove all CO components from the grid
            self.plus_co_label.grid_remove()
            self.co.grid_remove()  # Hide the CO entry field
            self.co_label.grid_remove()
            
    def get_fuel_atoms(self, fuel_selection):
        if fuel_selection == "Jet-A":
            return 12, 24
        elif fuel_selection == "Propane":
            return 3, 8
        elif fuel_selection == "Butane":
            return 4, 10
        elif fuel_selection == "Methane":
            return 1, 4
        else:
            return 0, 0

    def create_combustion_inputs(self, frame):
        self.mol_fuel = ctk.CTkEntry(frame, width=30)
        self.mol_fuel.insert(0, '1')
        self.mol_fuel.grid(row=0,column=0,padx=5,pady=5)
        
        self.fuel_formula = ctk.CTkLabel(frame, text='C12H24', font=('Computer Modern', 15))
        self.fuel_formula.grid(row=0,column=1,padx=5,pady=5)
        
        plus_label = ctk.CTkLabel(frame, text='+', font=('Computer Modern', 15))
        plus_label.grid(row=0,column=2,padx=5,pady=5)
        
        self.mol_oxygen = ctk.CTkEntry(frame, width=30)
        self.mol_oxygen.insert(0, '18')
        self.mol_oxygen.grid(row=0,column=3,padx=5,pady=5)
        self.o2_label = ctk.CTkLabel(frame, text='O2', font=('Computer Modern', 15))
        self.o2_label.grid(row=0,column=4,padx=5,pady=5)

        plus_label2 = ctk.CTkLabel(frame, text='+', font=('Computer Modern', 15))
        plus_label2.grid(row=0,column=5,padx=5,pady=5)
        
        self.mol_nitrogen = ctk.CTkEntry(frame, width=30)
        self.mol_nitrogen.insert(0, '3.77*18')
        self.mol_nitrogen.grid(row=0,column=6,padx=5,pady=5)
        self.n2_label = ctk.CTkLabel(frame, text='N2', font=('Computer Modern', 15))
        self.n2_label.grid(row=0,column=7,padx=5,pady=5)

        arrow_label = ctk.CTkLabel(frame, text='→', font=('Computer Modern', 15))
        arrow_label.grid(row=0,column=8,padx=5,pady=5)
        
        self.mol_water = ctk.CTkEntry(frame, width=30)
        self.mol_water.insert(0, '12')
        self.mol_water.grid(row=0,column=9,padx=5,pady=5)
        self.water_label = ctk.CTkLabel(frame, text='H2O', font=('Computer Modern', 15))
        self.water_label.grid(row=0,column=10,padx=5,pady=5)

        self.plus_label3 = ctk.CTkLabel(frame, text='+', font=('Computer Modern', 15))
        self.plus_label3.grid(row=0,column=11,padx=5,pady=5)
        
        self.co2 = ctk.CTkEntry(frame, width=30)
        self.co2.insert(0, '12')
        self.co2.grid(row=0,column=12,padx=5,pady=5)
        self.co2_label = ctk.CTkLabel(frame, text='CO2', font=('Computer Modern', 15))
        self.co2_label.grid(row=0,column=13,padx=5,pady=5)

        self.plus_label4 = ctk.CTkLabel(frame, text='+', font=('Computer Modern', 15))
        self.plus_label4.grid(row=0,column=14,padx=5,pady=5)
        
        self.o2 = ctk.CTkEntry(frame, width=30)
        self.o2.insert(0, '1')
        self.o2.grid(row=0,column=15,padx=5,pady=5)
        self.o2_label = ctk.CTkLabel(frame, text='O2', font=('Computer Modern', 15))
        self.o2_label.grid(row=0,column=16,padx=5,pady=5)
        
        self.plus5_label = ctk.CTkLabel(frame, text='+', font=('Computer Modern', 15))
        self.plus5_label.grid(row=0,column=17,padx=5,pady=5)

        self.n2 = ctk.CTkEntry(frame, width=30)
        self.n2.insert(0, '3.77*18')
        self.n2.grid(row=0,column=18,padx=5,pady=5)
        self.n2_label = ctk.CTkLabel(frame, text='N2', font=('Computer Modern', 15))
        self.n2_label.grid(row=0,column=19,padx=5,pady=5)

        self.plus_co_label = ctk.CTkLabel(frame, text='+',font=('Computer Modern', 15))
        self.plus_co_label.grid(row=0,column=20,padx=5,pady=5)
        self.plus_co_label.configure(fg_color="#2b2b2b")
        self.co = ctk.CTkEntry(frame, width=30)
        self.co.insert(0, '0')
        self.co.grid(row=0,column=21,padx=5,pady=5)
        self.co_label = ctk.CTkLabel(frame, text='CO', font=('Computer Modern', 15))
        self.co_label.grid(row=0,column=22,padx=5,pady=5)

        self.update_combustion_equation(self.fueldropdown.get())
    
    def get_combustion_equation(self):
        fuel_selection = self.fueldropdown.get()
        C, H = self.get_fuel_atoms(fuel_selection)
        try:
            mol_o2 = float(self.mol_oxygen.get())
            mol_n2 = float(self.mol_nitrogen.get())
        except ValueError:
            mol_o2 = 0
            mol_n2 = 0
            
        equation = {'fuel_type': fuel_selection,'carbon_atoms': C, 'hydrogen_atoms': H,
                    'oxygen_moles': mol_o2, 'nitrogen_moles': mol_n2}
        
        if self.dissociation_checkbox.get():
            equation["mol_co2"] = C
            equation["mol_h2o"] = H
            equation["mol_co"] = 1
            equation["dissociation"] = True
        else:
            equation["mol_co2"] = C
            equation["mol_h2o"] = H
            equation["mol_co"] = 0
            equation["dissociation"] = False
        return equation
        
    def update_combustion_equation(self, fuel_selection):
        if fuel_selection == "Jet-A":
            self.fuel_formula.configure(text='C12H24')
        elif fuel_selection == "Propane":
            self.fuel_formula.configure(text='C3H8')
        elif fuel_selection == "Butane":
            self.fuel_formula.configure(text='C4H10')
        elif fuel_selection == "Methane":
            self.fuel_formula.configure(text='CH4')
            
        if hasattr(self, 'dissociation_checkbox'):
            self.update_equation_values()
        
