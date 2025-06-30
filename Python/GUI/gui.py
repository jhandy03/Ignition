import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from PIL import Image, ImageTk #might throw in the MW logo later somewhere along with some easter eggs ;)
from MainInputsWidget.main_inputs_widget import MainInputsWidget
from MainCalculations.main_calculations import MainCalculations
from UnitConversionToolbox.unit_conversion_toolbox import UnitConversionToolbox
import random as rand
from Settings.settings import Settings
import time
# import datetime
# import threading


class GUI:
    def __init__(self):
        self.ignition = MainCalculations()  # make an instance of the MainCalculations class
        self.uct = UnitConversionToolbox()  # Create instance of unit conversion class
        self.settings = Settings(self)
        self.main_window()
        
        self.stop_run = False
        self.start_time_main = time.time()
        
       
        
    def main_window(self):
        self.start_time_main = time.time()
        self.root = ctk.CTk()   #create main window
        self.root.title("Ignition v0.5")     #name of the window
        ctk.set_appearance_mode("dark") #set default theme to dark. Will add ability to change later
        self.root._state_before_windows_set_titlebar_color = 'zoomed' #fullscreen the window
        
        rand_num = rand.randint(0, 100)
        if rand_num >=  95:
            self.root.configure(cursor='right_ptr')
        else:
            pass
        
        #Creates the mains tabs of Ignition and then assigns them to variables. Makes things easier to type later
        tabs = ctk.CTkTabview(self.root, width=300, height=300, anchor="w",border_width=2, border_color="#4a4a4a", fg_color="#2b2b2b") #anchor='w' make them left aligned
        tabs.pack(padx=20, pady=20, anchor="w",expand=True,fill='both')
        tabs.add("Main")
        tabs.add("Unit Conversion Toolbox")
        tabs.add("Settings")
        maintab = tabs.tab("Main")
        self.settingstab = tabs.tab("Settings")  #may add more later
        self.ucttab = tabs.tab("Unit Conversion Toolbox")
        self.settings_window()
        self.uct_window()
        

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
        leftframe.grid_rowconfigure(6,weight=0)
        leftframe.grid_rowconfigure(4,weight=1) #label for output
        
        #rows for the input frames. Want them to be a bit larger than the labels
        leftframe.grid_rowconfigure(1,weight=2)
        leftframe.grid_rowconfigure(3,weight=2)
        leftframe.grid_rowconfigure(5,weight=2) #row for outputs
        leftframe.grid_columnconfigure(0,weight=1)
        inputsframe = ctk.CTkFrame(leftframe)
        inputsframe.grid(row=1,column=0, padx=10, pady=(0,10), sticky="new")
        
        
        #made a separate frame for the start, stop and reset buttons
        leftframe_bottom = ctk.CTkFrame(leftframe,fg_color="transparent")
        leftframe_bottom.grid(row=4,column=0, padx=10, pady=(0,10), sticky="ns") 
        leftframe_bottom.grid_rowconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(0,weight=1)
        leftframe_bottom.grid_columnconfigure(1,weight=1)
        leftframe_bottom.grid_columnconfigure(2,weight=1)
        
        geninputslabel_frame = ctk.CTkFrame(leftframe,fg_color="transparent")
        geninputslabel_frame.grid(row=0,column=0,padx=10,pady=0)
        geninputslabel = ctk.CTkLabel(geninputslabel_frame,text="General Inputs",font=("Courier New Bold", 20))
        geninputslabel.grid(row=0,column=0,padx=10,pady=10,sticky="ns")
        
        #Right frame will contain the plots for the geometry, temp, pressure, and mach number vs axial distance
        self.rightframe.grid_columnconfigure(0,weight=1)
        self.rightframe.grid_rowconfigure(0,weight=2)
        self.rightframe.grid_rowconfigure(1,weight=1)
        self.rightframe.grid_rowconfigure(2,weight=1)
        
        
        #all values with 1 are incomplete. Recheck units as I want to make them base SI instead of weird numbers like in matlab
        input_widgets = [
            {'label': "\u03B3", "value":1.4, "units": ""},
            {'label': "R", "value":287, "units": "J/(kg*K)"},
            {'label': "\u03C1 air ", "value":1.225, "units": "kg/m^3"},
            {'label': "Blowout Velocity Parameter", "value":1, "units": ""},
            {'label': "Ignition Time Parameter", "value":1, "units": ""},
            {'label': "\u1E41 in", "value":1, "units": "L/s"},
            {'label': "\u1E41 fuel", "value":1, "units": "g/min"},
            {'label': "Exit Velocity", "value":1200, "units": "km/hr"},
            {'label': "Turbine Blade Length", "value":1, "units": "mm"},
            {'label': "Diffuser Length", "value":1, "units": "mm"},
            {'label': "Straight Section Length", "value":1, "units": "mm"},
            {'label': "Flame Holder Half Angle", "value":15, "units": "degrees"},
            {'label': "Nozzle Diameter", "value":1, "units": "mm"},
            {'label': "Turbine Diameter", "value":1, "units": "mm"},
            
            # {'label': "Blank", "value":1, "units": "Blank"},    #3 placeholders for now, might not need?
            # {'label': "Blank", "value":1, "units": "Blank"},
            # {'label': "Blank", "value":1, "units": "Blank"},
        ]
        inputs_per_column = 7
        self.widget_instances = []
        for i, inp in  enumerate(input_widgets):
            col = i // inputs_per_column
            row = i % inputs_per_column
            grid_col = col*3
            widget = MainInputsWidget(inputsframe, value=str(inp["value"]),label_front=inp["label"], label_rear=inp["units"])
            widget.grid(row = row,column=grid_col)
            self.widget_instances.append(widget)
        
        num_input_col = ((len(input_widgets) + inputs_per_column - 1) // inputs_per_column) * 3
        for c in range(num_input_col):
            if c%2 ==1:
                inputsframe.grid_columnconfigure(c, weight=1)
            else:
                inputsframe.grid_columnconfigure(c, weight=0)

        self.startbutton = ctk.CTkButton(leftframe_bottom,text="Start",command=self.run_ignition) #implement start function later
        self.startbutton.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.startbutton.bind('<Return>', lambda event: self.run_ignition())
        self.stopbutton = ctk.CTkButton(leftframe_bottom,text="Stop",command=None) #implement stop function later
        self.stopbutton.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
        self.resetbutton = ctk.CTkButton(leftframe_bottom,text="Reset",command=None) #implement reset function later
        self.resetbutton.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")
        
        #combustion inputs frame. Not sure how I want to organize this entirely yet
        combframe = ctk.CTkFrame(leftframe)
        combframe.grid(row=3,column=0, padx=10, pady=10, sticky="new")
        combframe.grid_columnconfigure(0, weight=1)
        combustionlabel = ctk.CTkLabel(combframe, text="Combustion Inputs", font=("Courier New Bold", 20))
        combustionlabel.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        combframetop = ctk.CTkFrame(combframe,fg_color="transparent")
        combframetop.grid(row=1, column=0, padx=10, pady=(0,10))
        combframemiddle = ctk.CTkFrame(combframe,fg_color="transparent")
        combframemiddle.grid(row=2, column=0, padx=10, pady=(0,10))
        
        fuel_label = ctk.CTkLabel(combframetop,text='Fuel Type',font=("Computer Modern", 15))
        fuel_label.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.fueldropdown = ctk.CTkOptionMenu(combframetop, values=["Jet-A","Propane","Butane","Methane"],command=self.update_combustion_equation,font=('Computer Modern',15)) #TODO: Finish later (want to change the colors later too)
        self.fueldropdown.grid(row=0,column=1,padx=10,pady=10)
        self.dissociation_checkbox = ctk.CTkCheckBox(combframetop,text="Dissociation",command=self.update_equation_values,font=('Computer Modern',15)) #TODO: Finish later
        self.dissociation_checkbox.grid(row=0,column=2,padx=10,pady=10,sticky="e")
        
        combframeinputs = ctk.CTkFrame(combframemiddle,fg_color="transparent")
        combframeinputs.grid(row=0,column=0,padx=10,pady=(0,10),sticky="nsew")
        combframeinputs.grid_rowconfigure(0,weight=1)
        
        self.create_combustion_inputs(combframeinputs)
        
        combframebottom = ctk.CTkFrame(combframe,fg_color="transparent")
        combframebottom.grid(row=3,column=0,padx=10,pady=(0,10))
        
        combustion_bottom_widgets = [
            {'label': "EGT", "value": 1073.15, "units": "K"},
            {'label': "Combustion Pressure", "value": 101325, "units": "Pa"},
        ]
        
        self.widget_instances_bottom = []
        for i, inp in enumerate(combustion_bottom_widgets):
            col = i * 3
            widget = MainInputsWidget(combframebottom, value=str(inp["value"]), label_front=inp["label"], label_rear=inp["units"])
            widget.grid(row=0, column=col)
            self.widget_instances_bottom.append(widget)
        
        #Plot stuff
        self.setup_plots(self.rightframe)
        
        self.output_frame = ctk.CTkFrame(leftframe,fg_color="transparent")
        self.output_frame.grid(row=5,column=0,padx=10,pady=(0,10),sticky="nsew")
        self.output_frame.grid_rowconfigure(0,weight=1)
        
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Outputs", font=("Courier New Bold",25))
        self.output_label.grid(row=0,column=0,columnspan=6,padx=10,pady=10,sticky="ew")
        
        
        output_widgets = [
            {'label': "Thrust Increase", "value": 1, "units": "N"},
            {'label': "Combustion Temperature", "value": 1, "units": "K"},
            {'label': "Combustion Pressure", "value": 1, "units": "Pa"},
            {'label': "Exit Mach Number", "value": 1, "units": ""},
            {'label': "\u03A6", "value": 1, "units": ""},
            {'label': "𝑓 act", "value": 1, "units": ""},
            {'label': "𝑓 stoich", "value": 1, "units": ""},
        ]
        self.widget_instances_output = []
        inputs_per_column_output = 4
        for i, out in enumerate(output_widgets):
            col = i // inputs_per_column_output
            row = (i % inputs_per_column_output) + 1  # +1 to start below the label
            grid_col = col * 3  # Each widget takes 3 columns (label, space, input)
            widget_output = MainInputsWidget(self.output_frame, value=str(out["value"]), label_front=out["label"], label_rear=out["units"])
            widget_output.grid(row=row, column=grid_col)
            self.widget_instances_output.append(widget_output)
        
        num_output_col = ((len(output_widgets) + inputs_per_column_output - 1) // inputs_per_column_output) * 3
        for c in range(num_output_col):
            if c % 3 == 1:  # Middle columns (spacing)
                self.output_frame.grid_columnconfigure(c, weight=1)
            else:  # Label and input columns
                self.output_frame.grid_columnconfigure(c, weight=0)

        
        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) #handles closing the window properly
        self.root.mainloop() #runs the main loop
    
    def setup_plots(self, frame):
        frame.grid_rowconfigure(0,weight=1) #was going to make the geometry plot larger but looks bad
        frame.grid_rowconfigure(1,weight=1)
        frame.grid_rowconfigure(2,weight=1)
        self.setup_geometry_plot()
        self.setup_temp_pressure_plot()
        self.setup_mach_plot()
        self.test_plot()
        
        self.figures = [self.geometry_fig, self.temp_fig, self.mach_fig, self.test_fig] #used for theme change
        
    def setup_geometry_plot(self):
         
        self.geometry_fig, self.geometry_ax = plt.subplots(figsize=(6,6.5),facecolor='#2b2b2b') #might need to pass in figsize if things are a bit off
        self.geometry_ax.set_title("Afterburner Geometry",color='w')
        self.geometry_ax.set_xlabel("Axial Distance (m)",color='w')
        self.geometry_ax.set_ylabel("Radial Distance (m)",color='w')
        self.geometry_canvas = FigureCanvasTkAgg(self.geometry_fig, master=self.rightframe)
        self.geometry_canvas.get_tk_widget().grid(row=0, column=0,padx=10,pady=10, sticky="nsew")
        self.geometry_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
        self.geometry_ax.plot([0, 2], [0, 2])  # Example plot data
        self.geometry_ax.set_facecolor("#4b4b4b")
        self.geometry_ax.tick_params(labelcolor='w')
         
    def setup_temp_pressure_plot(self):
        
        self.temp_fig, self.temp_ax = plt.subplots(facecolor='#2b2b2b')
        self.temp_ax.set_title("Temperature and Pressure vs Axial Distance",color='w')
        # self.temp_ax.set_xlabel("Axial Distance (m)") #gets cut off and I can't figure out a way to fit the label on every plot
        self.temp_ax.set_ylabel("Temperature (K)",color='w')
        self.temp_ax.set_facecolor("#4b4b4b")
        
        self.pressure_ax = self.temp_ax.twinx()
        self.pressure_ax.set_ylabel("Pressure (Pa)",color='w')
        self.pressure_ax.tick_params(labelcolor='w')
        
        self.tp_canvas = FigureCanvasTkAgg(self.temp_fig, master =self.rightframe)
        self.tp_canvas.get_tk_widget().configure(highlightthickness=0,bd=0,bg='#2b2b2b')
        self.tp_canvas.get_tk_widget().grid(row=1, column=0,padx=10,pady=10, sticky="nsew")
        self.temp_ax.grid(True, linestyle='-', alpha=0.5) #enables grid w/ 50% opacity
        self.temp_ax.tick_params(labelcolor='w')
           
    def setup_mach_plot(self):
        
        self.mach_fig, self.mach_ax = plt.subplots(facecolor='#2b2b2b')
        self.mach_ax.set_title("Mach Number vs Axial Distance",color='w')
        # self.mach_ax.set_xlabel("Axial Distance (m)")     #gets cut off and I can't figure out a way to fit the label on every plot
        self.mach_ax.set_ylabel("Mach Number",color='w')
        self.mach_canvas = FigureCanvasTkAgg(self.mach_fig, master=self.rightframe)
        self.mach_canvas.get_tk_widget().configure(highlightthickness=0,bd=0,bg='#2b2b2b')
        self.mach_canvas.get_tk_widget().grid(row=2, column=0,padx=10,pady=10, sticky="nsew")
        self.mach_ax.grid(True, linestyle='--', alpha=0.5) #enables grid w/ 50% opacity
        self.mach_ax.set_facecolor("#4b4b4b")
        self.mach_ax.tick_params(labelcolor='w')

    def test_plot(self):
        self.test_fig, self.test_ax = plt.subplots(facecolor='#2b2b2b')
        self.test_ax.set_title('Test Plot',color='w')
        self.test_ax.set_xlabel('x-axis',color='w')
        self.test_ax.set_ylabel('y-axis',color='w')
        self.test_canvas = FigureCanvasTkAgg(self.test_fig, master=self.example_frame)
        self.test_canvas.get_tk_widget().configure(highlightthickness=0, bd=0, bg='#2b2b2b')
        self.test_canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.test_ax.grid(True, linestyle='-', alpha=0.5)
        self.test_ax.set_facecolor("#4b4b4b")
        self.test_ax.tick_params(labelcolor='w')

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

    def run_ignition(self):
        self.startbutton.configure(state='disabled',text='Processing...')
        # self.stop_run = False
        self.start_time_ignition = time.time()
        self.settings.log_event("Ignition Calculations Started", 0,0)
        self.root.update() 
        try:
            gamma = float(self.widget_instances[0].get_value())
            R_val = float(self.widget_instances[1].get_value())
            rho_air = float(self.widget_instances[2].get_value())
            bv_param = float(self.widget_instances[3].get_value())
            it_param = float(self.widget_instances[4].get_value())
            mdot_in = float(self.widget_instances[5].get_value())
            mdot_fuel = float(self.widget_instances[6].get_value())
            exit_velocity = float(self.widget_instances[7].get_value())
            turb_blade_len = float(self.widget_instances[8].get_value())
            diff_length = float(self.widget_instances[9].get_value())
            straight_length = float(self.widget_instances[10].get_value())
            theta = float(self.widget_instances[11].get_value())
            noz_d = float(self.widget_instances[12].get_value())
            turb_d = float(self.widget_instances[13].get_value())
            
            egt = float(self.widget_instances_bottom[0].get_value())
            input_pressure = float(self.widget_instances_bottom[1].get_value())
            
            fuel_type = str(self.fueldropdown.get())
            dissociation_checkbox_value = self.dissociation_checkbox.get()
            #add in the combustion equation stuff later. Not sure how to handle yet
            comb_temp = float(self.widget_instances_bottom[0].get_value())
            comb_pressure = float(self.widget_instances_bottom[1].get_value())
            D_len = 2 #flame holder height (optimize to find this??)

            input_names = [ ('gamma',gamma), ('R',R_val), ('rho_air',rho_air), ('bv_param',bv_param), ('it_param',it_param), 
                           ('mdot_in',mdot_in), ('mdot_fuel',mdot_fuel), ('exit_velocity',exit_velocity), ('turb_blade_len',turb_blade_len), 
                           ('diff_length',diff_length), ('straight_length',straight_length), ('theta',theta), ('noz_d',noz_d), ('turb_d',turb_d), 
                           ('egt',egt), ('input_pressure',input_pressure), ('comb_temp',comb_temp), ('comb_pressure',comb_pressure), ('D_len',D_len)]

            #TODO: add input validation
            for name, value in input_names:
                self.ignition.validate_input(value)
                if self.ignition.validate_input(value) is False:
                    self.settings.log_event(f"Invalid input for {name}",0,0)
                    self.startbutton.configure(state='normal',text='Start')
                    return
                else:
                    self.settings.log_event(f"Input {name} validated successfully",0,0)
                    
                
                
            runignition = self.ignition.main_calculations(gamma, R_val, rho_air, egt, exit_velocity, bv_param, it_param, turb_blade_len,
                                                        diff_length, straight_length, theta, D_len, noz_d, turb_d, mdot_in, mdot_fuel)
            end_time_ignition = time.time()
            time_check = end_time_ignition - self.start_time_ignition
            
            def update_outputs():
                self.widget_instances_output[0].set_value(str(runignition['thrust']))
                self.widget_instances_output[1].set_value(str(runignition['Tpost']))
                self.widget_instances_output[2].set_value(str(runignition['Ppost']))
                self.widget_instances_output[3].set_value(str(runignition['Mexit']))
                self.widget_instances_output[4].set_value(str(runignition['phi']))
                self.widget_instances_output[5].set_value(str(runignition['f_act']))
                self.widget_instances_output[6].set_value(str(runignition['f_stoich']))
                self.startbutton.configure(state='normal',text='Start')
                self.settings.log_event("Ignition calculations completed", self.start_time_ignition, end_time_ignition)
            
            #wanted to throw in a small delay since if it runs too fast it feels weird to the user. Might
            #want to adjust/ remove later as the calcs become more intensive/ take longer
            if time_check <= 0.1: #TODO revisit
                # rand_time = rand.randint(0,1)
                # self.root.after(rand_time, update_outputs)
                update_outputs()
            else:
                update_outputs()
            
        except Exception as e:
            self.settings.log_event(f"Error during Ignition calculations: {e}", 0,0)
            self.startbutton.configure(state='normal',text='Start')
            return
            

    def settings_window(self):
        for i in range(2):
            self.settingstab.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.settingstab.grid_columnconfigure(i, weight=1)
        
        set_main_frame = ctk.CTkFrame(self.settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        set_main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        set_main_frame.grid_columnconfigure(0, weight=1)
        set_main_frame.grid_rowconfigure(0, weight=0)
        set_main_frame.grid_rowconfigure(1, weight=0)
        set_main_frame.grid_rowconfigure(2, weight=0)
        set_main_frame.grid_rowconfigure(3, weight=0)

        theme_label = ctk.CTkLabel(set_main_frame, text="Theme", font=("Courier New Bold", 20))
        theme_label.grid(row=0, column=0, padx=10, pady=10,sticky='nw')
        theme_dropdown = ctk.CTkOptionMenu(set_main_frame, values=['Dark','Light','System'], command=self.settings.set_theme, font=("Computer Modern", 15))
        theme_dropdown.grid(row=1,column=0, padx=10, pady=10,sticky='w')
        
        plot_color_label = ctk.CTkLabel(set_main_frame, text='Plot Theme',font=('Courier New Bold', 20))
        plot_color_label.grid(row=2,column=0,padx=10,pady=10,sticky='nw')
 
        plot_color_options = ['Dark','Light',"Don't"]
        plot_theme_selection = ctk.CTkOptionMenu(set_main_frame, values=plot_color_options, command=self.settings.plotcolors, font=("Computer Modern", 15))
        plot_theme_selection.grid(row=3,column=0, padx=10, pady=10,sticky='w')
        
        self.example_frame = ctk.CTkFrame(self.settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        self.example_frame.grid(row=0, column=1, padx=10, pady=10, sticky="new")

        self.example_frame.grid_columnconfigure(0,weight=1)
        self.example_frame.grid_rowconfigure(0,weight=1)
        self.example_frame.grid_rowconfigure(1,weight=1)
        self.example_frame.grid_rowconfigure(2,weight=1)

        example_title_label = ctk.CTkLabel(self.example_frame, text="Example Title", font=("Courier New Bold", 20))
        example_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        example_text_label = ctk.CTkLabel(self.example_frame, text="This is example text", font=('Computer Modern', 15))
        example_text_label.grid(row=1, column=0, padx=10, pady=10, sticky="new")


        internal_log_frame = ctk.CTkFrame(self.settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        internal_log_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        internal_log_frame.grid_columnconfigure(0, weight=1)
        internal_log_frame.grid_rowconfigure(0, weight=1)
        internal_log_label = ctk.CTkLabel(internal_log_frame, text="Debug Log", font=("Computer Modern",20))
        internal_log_label.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        
        self.end_time_main = time.time()
        self.settings.logging_setup(internal_log_frame)
        self.settings.log_event("App Initialized",self.start_time_main, self.end_time_main)
        
        self.about_frame = ctk.CTkFrame(self.settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        self.about_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.about_frame.grid_columnconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(1, weight=1)
        
        about_label = ctk.CTkLabel(self.about_frame, text='About', font=("Computer Modern", 20))
        about_label.grid(row=0,column=0,padx=10,pady=10,sticky="ns")

        about_text = ctk.CTkTextbox(self.about_frame, width=500, height=225, font=("Computer Modern",15))
        about_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        about_text.insert("end",
            "Ignition was originally written by Jordan Handy during March 2025 in MATLAB. Its original use was to simplify repeated calculations when designing an afterburner for a small turbojet engine for MachWorks.\n\n"
            "MachWorks is an undergraduate design team based out of Virginia Tech, focusing on high-speed jet-powered aircraft. Ignition was then expanded \nto include more functionality (thanks to JD Fiore), performing combustion calculations, unit conversions, and other engineering calculations.\n\n"
            "As ambitions grew, the need for converting the code into a more robust and easy to collaborate on language arose. Formal talks about converting \nthe codebase to Python started in April 2025, with initial conversions starting in May the same year.\n\n"
            "Since then, the code has been expanded to work with external programs for use in simulation and optimization. The end goal for Ignition is to be a \nfully-featured afterburner design tool that students can use to design and optimize afterburners for small, hobbyist turbojet engines."
        )





        # font_frame = ctk.CTkFrame(self.settingstab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
        # font_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
    def uct_window(self):
        for i in range(9):
            self.ucttab.grid_rowconfigure(i, weight=1)
            
        self.ucttab.grid_columnconfigure(0, weight=1)
        self.ucttab.grid_columnconfigure(1, weight=2)
        self.ucttab.grid_columnconfigure(2, weight=2)
        self.ucttab.grid_columnconfigure(3, weight=2)
        self.ucttab.grid_columnconfigure(4, weight=2)
        self.ucttab.grid_columnconfigure(5, weight=2)

            
        
        title_label = ctk.CTkLabel(self.ucttab, text="Unit Conversion Toolbox", font=("Courier New Bold", 50))
        title_label.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="ns")
        
        inputs_label = ctk.CTkLabel(self.ucttab, text="Input Units", font=("Computer Modern", 25))
        inputs_label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        outputs_label = ctk.CTkLabel(self.ucttab, text="Output Units", font=("Computer Modern", 25))
        outputs_label.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")
        
        unit_labels = ['Temperature','Pressure','Velocity','Volume','Mass Flow Rate','Volume Flow Rate','Mass to Volume Flow Rate']
            
        for i, input in enumerate(unit_labels):
            conversion_label = ctk.CTkLabel(self.ucttab, text=input, font=("Computer Modern", 20))
            conversion_label.grid(row=i+2, column=0, padx=10, pady=10, sticky="ns")
            
        self.input_entries=[]
        for i in range(7):
            entry = ctk.CTkEntry(self.ucttab, width=20)
            entry.grid(row=i+2, column=1, padx=10, pady=10, sticky="ew")
            entry.bind('<KeyRelease>', self.conversion_callback(i))  # Bind key release to conversion
            self.input_entries.append(entry)

        self.input_temp_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["Celsius", "Fahrenheit", "Kelvin"], command=lambda x: self.convert_units(0), font=("Computer Modern", 15))
        self.input_temp_dropdown.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

        self.input_pressure_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["bar", "atm", "Pa"], command=lambda x: self.convert_units(1), font=("Computer Modern", 15))
        self.input_pressure_dropdown.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        self.input_velocity_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m/s", "km/hr", "mph"], command=lambda x: self.convert_units(2), font=("Computer Modern", 15))
        self.input_velocity_dropdown.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

        self.input_volume_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m^3", "cm^3", "L"], command=lambda x: self.convert_units(3), font=("Computer Modern", 15))
        self.input_volume_dropdown.grid(row=5, column=2, padx=10, pady=10, sticky="ew")

        self.input_mfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["kg/s", "g/min", "kg/min"], command=lambda x: self.convert_units(4), font=("Computer Modern", 15))
        self.input_mfr_dropdown.grid(row=6, column=2, padx=10, pady=10, sticky="ew")

        self.input_vfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m^3/s", "L/s", "m^3/min","L/min"], command=lambda x: self.convert_units(5), font=("Computer Modern", 15))
        self.input_vfr_dropdown.grid(row=7, column=2, padx=10, pady=10, sticky="ew")

        self.input_mtvfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["kg/s", "m^3/s"], command=lambda x: self.convert_units(6), font=("Computer Modern", 15))
        self.input_mtvfr_dropdown.grid(row=8, column=2, padx=10, pady=10, sticky="ew")

        for i in range(7):
            arrows_label = ctk.CTkLabel(self.ucttab, text="→", font=("Computer Modern", 50))
            arrows_label.grid(row=i+2, column=3, padx=10, pady=10, sticky="nsew")

        self.output_temp_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["Celsius", "Fahrenheit", "Kelvin"], command=lambda x: self.convert_units(0), font=("Computer Modern", 15))
        self.output_temp_dropdown.grid(row=2, column=4, padx=10, pady=10, sticky='ew')

        self.output_pressure_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["bar", "atm", "Pa"], command=lambda x: self.convert_units(1), font=("Computer Modern", 15))
        self.output_pressure_dropdown.grid(row=3, column=4, padx=10, pady=10, sticky='ew')

        self.output_velocity_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m/s", "km/hr", "mph"], command=lambda x: self.convert_units(2), font=("Computer Modern", 15))
        self.output_velocity_dropdown.grid(row=4, column=4, padx=10, pady=10, sticky='ew')

        self.output_volume_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m^3", "cm^3", "L"], command=lambda x: self.convert_units(3), font=("Computer Modern", 15))
        self.output_volume_dropdown.grid(row=5, column=4, padx=10, pady=10, sticky='ew')

        self.output_mfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["kg/s", "g/min", "kg/min"], command=lambda x: self.convert_units(4), font=("Computer Modern", 15))
        self.output_mfr_dropdown.grid(row=6, column=4, padx=10, pady=10, sticky='ew')

        self.output_vfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["m^3/s", "L/s", "m^3/min",'L/min'], command=lambda x: self.convert_units(5), font=("Computer Modern", 15))
        self.output_vfr_dropdown.grid(row=7, column=4, padx=10, pady=10, sticky='ew')

        self.output_mtvfr_dropdown = ctk.CTkOptionMenu(self.ucttab, values=["kg/s", "m^3/s"], command=lambda x: self.convert_units(6), font=("Computer Modern", 15))
        self.output_mtvfr_dropdown.grid(row=8, column=4, padx=10, pady=10, sticky='ew')

        self.output_entries = []
        for i in range(7):
            entry = ctk.CTkEntry(self.ucttab, width=20)
            entry.grid(row=i+2, column=5, padx=10, pady=10, sticky="ew")
            self.output_entries.append(entry)
   
    def convert_units(self, type):
        self.start_unit_convert_time = time.time()
        try:
            input_value = self.input_entries[type].get()
            if not input_value:
                self.output_entries[type].delete(0, 'end')  
                return  
            input_value = float(input_value)
            dropdowns = [
                (self.input_temp_dropdown, self.output_temp_dropdown),
                (self.input_pressure_dropdown, self.output_pressure_dropdown),
                (self.input_velocity_dropdown, self.output_velocity_dropdown),
                (self.input_volume_dropdown, self.output_volume_dropdown),
                (self.input_mfr_dropdown, self.output_mfr_dropdown),
                (self.input_vfr_dropdown, self.output_vfr_dropdown),
                (self.input_mtvfr_dropdown, self.output_mtvfr_dropdown),
            ]
            input_unit = dropdowns[type][0].get()
            output_unit = dropdowns[type][1].get()
            
            if input_unit == output_unit:
                output_value = input_value
            else:
                if type == 0:
                    output_value = self.uct.temp_conversion(input_value, input_unit, output_unit)
                elif type == 1:
                    output_value = self.uct.pressure_conversion(input_value, input_unit, output_unit)
                elif type == 2:
                    output_value = self.uct.velocity_conversion(input_value, input_unit, output_unit)
                elif type == 3:
                    output_value = self.uct.volume_conversion(input_value, input_unit, output_unit)
                elif type == 4:
                    output_value = self.uct.massflow_conversion(input_value, input_unit, output_unit)
                elif type == 5:
                    output_value = self.uct.volflow_conversion(input_value, input_unit, output_unit)
                elif type == 6:
                    output_value = self.uct.mass2vol_conversion(input_value, 1.225, input_unit, output_unit) #TODO: Fix the density
                else:
                    output_value = input_value
            
            self.output_entries[type].delete(0, 'end')
            self.output_entries[type].insert(0, f"{output_value:.4f}")
            self.end_unit_convert_time = time.time()
            self.settings.log_event("Unit Conversion Completed", self.start_unit_convert_time, self.end_unit_convert_time)
        
        except ValueError:
            self.output_entries[type].delete(0, 'end')
            print("value error")
        
        except Exception as e:
            self.output_entries[type].delete(0, 'end')
            print('exception')
            
    def conversion_callback(self,index):
        def callback(event):
            self.convert_units(index)
        return callback
    
    