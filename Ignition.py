"""
Author: Jordan Handy
Last Updated: 05/24/2025
Contact: jhandy03@vt.edu

Repo: https://github.com/jhandy03/Ignition

Written for MachWorks @ Virgnia Tech's Propulsion Subteam

MIT Liscense or sum shit idk

"""
import math
import sympy as sym
import tkinter as tk
#import PIL
import ttkbootstrap as ttk #used to make the app look a little nicer. For use with tkinter but not sure I want to continue with that
from ttkbootstrap.constants import LEFT, RIGHT, TOP, BOTTOM, CENTER #specific constants instead of wildcard import
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import Window
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

class Ignition:
    def __init__(self,master):
        self.master = master
        master.title('Ignition V 0.0.1')
        self.master.state('zoomed')

        #Configure main window
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1,weight=1)
        self.master.grid_rowconfigure(2,weight=1)
        
        #configure plot frame. sets sizes of the rows and columns
        self.plot_container_frame = ttk.Frame(self.master,bootstyle='darkly')
        self.plot_container_frame.grid(row=0,column=1, sticky='NSEW',padx=1,pady=1)
        self.plot_container_frame.grid_columnconfigure(0,weight=1)
        self.plot_container_frame.grid_rowconfigure(0, weight=2)
        self.plot_container_frame.grid_rowconfigure(1, weight=1)
        self.plot_container_frame.grid_rowconfigure(2, weight=1)
        
        #starts the 3 plots??
        self.plots = {}
        self.plot_setup('geometry', 'Engine Geometry', self.plot_container_frame, row=0)
        self.plot_setup('pt_data', 'Pressure and Temperature Profile', self.plot_container_frame, row=1)
        self.plot_setup('mach_data', 'Mach Number Profile', self.plot_container_frame, row=2)
        
        #General inputs frame
        self.general_inputs_frame = ttk.Frame(self.master,bootstyle='darkly')
        self.general_inputs_frame.grid(row=0,column=0, sticky='NSEW',padx=1,pady=1)
        
        #Configures the rows and col for the gen inputs. 18 total inputs split into 3 col and 6 rows
        for i in range(7):
            self.general_inputs_frame.grid_rowconfigure(i,weight=1)
        
        #configures col 0,3,6  1,4,7  2,5,8
        for i in range(3):
            self.general_inputs_frame.grid_columnconfigure(i*3,weight=1)
            self.general_inputs_frame.grid_columnconfigure(i*3+1,weight=2)
            self.general_inputs_frame.grid_columnconfigure(i*3+3,weight=1)
            
        ttk.Label(self.general_inputs_frame,text='General Inputs',bootstyle='darkly').grid(row=0,column=0,columnspan=9,ypad=1,sticky='EW')
        #TODO: revisit the parameters since the names/ values are not entirely correct
        #Will need to be updated with additional user inputs (ie all the stoich stuff/ combustion, or other?? Maybe the unit conversion stuff?)
        self.input_vars = {'gamma':tk.DoubleVar(value=1.4),'R':tk.DoubleVar(value=287),'rho_air':tk.DoubleVar(value=1.225),
                   'EGT':tk.DoubleVar(value=800),'u_exit':tk.DoubleVar(value=1200),'BVP':tk.DoubleVar(value=1),
                   'ITP':tk.DoubleVar(value=0.9515),'mdot_in':tk.DoubleVar(value=1),'length_turbine':tk.DoubleVar(value=1),
                   'length_diff':tk.DoubleVar(value=1),'straight':tk.DoubleVar(value=1),'half_angle':tk.DoubleVar(value=15),
                   'flame_height':tk.DoubleVar(value=1),'noz_diameter':tk.DoubleVar(value=1),'turb_diameter':tk.DoubleVar(value=1),
                   'mdot_fuel':tk.DoubleVar(value=1),'plot_points':tk.DoubleVar(value=1),'M_diff':tk.DoubleVar(value=1)}
        self.input_params = [('Gamma:',self.input_vars['gamma']," "),('R:',self.input_vars['R'],'J/(kg*K)'),
                    ('Air Density:',self.input_vars['rho_air'],'kg/m³'),('EGT:',self.input_vars['EGT'],'°C'),
                    ('Exit Velocity:',self.input_vars['u_exit'],'km/hr'),('BVP:',self.input_vars['BVP'],''),
                    ('ITP:',self.input_vars['ITP'],' '),('Mass Flow In:',self.input_vars['mdot_in'],'L/s'),
                    ('Turbine Length:',self.input_vars['length_turbine'],'m'),('Diffuser Length:',self.input_vars['length_diff'],'m'),
                    ('Straight Length:',self.input_vars['straight'],'m'),('Half Angle:',self.input_vars['half_angle'],'°'),
                    ('Flame Height:',self.input_vars['flame_height'],'m'),('Nozzle Diameter:',self.input_vars['noz_diameter'],'m'),
                    ('Turbine Diameter:',self.input_vars['turb_diameter'],'m'),('Fuel Mass Flow:',self.input_vars['mdot_fuel'],'g/min'),
                    ('Plot Points:',self.input_vars['plot_points'],' '),('Mach Number Post Diffuser:',self.input_vars['M_diff'],' ')]

        current_grid_row_for_inputs=1
        for i,(label_text,var_obj,unit_text) in enumerate(self.input_params):
# Calculate the row number within input_frame.
            # (i // 3) increments the row every 3 items.
            row_in_frame = current_grid_row_for_inputs + (i // 3)
            
            # Calculate the starting physical column for this group of (Label, Entry, Unit).
            # (i % 3) cycles through 0, 1, 2 for the logical groups.
            # * 3 converts this to the actual starting physical column (0, 3, or 6).
            start_physical_col = (i % 3) * 3 

            # Configure this specific row to expand proportionally
            self.general_inputs_frame.grid_rowconfigure(row_in_frame, weight=1)

            # Place the Label (e.g., "Gamma:", "R:")
            ttk.Label(self.general_inputs_frame, text=label_text, bootstyle="inverse-primary").grid(
                row=row_in_frame, column=start_physical_col,
                pady=2, padx=5, sticky='w' # 'w' for west (left) alignment
            )
            
            # Place the Entry widget
            # Use type checking to ensure correct validation function is called
            if isinstance(var_obj, tk.IntVar):
                ttk.Entry(self.general_inputs_frame, textvariable=var_obj, validate="key",
                          validatecommand=(self.master.register(self._validate_int_input), '%P')).grid(
                    row=row_in_frame, column=start_physical_col + 1,
                    pady=2, padx=5, sticky='ew' # 'ew' for expand horizontally
                )
            else: # Assume DoubleVar
                ttk.Entry(self.general_inputs_frame, textvariable=var_obj, validate="key",
                          validatecommand=(self.master.register(self._validate_float_input), '%P')).grid(
                    row=row_in_frame, column=start_physical_col + 1,
                    pady=2, padx=5, sticky='ew'
                )

            # Place the Unit/Description Label
            # Only show if there's actual text (not just empty space or None)
            if unit_text.strip():
                ttk.Label(self.general_inputs_frame, text=unit_text, bootstyle="inverse-secondary").grid(
                    row=row_in_frame, column=start_physical_col + 2,
                    pady=2, padx=5, sticky='w' # 'w' for west (left) alignment
                )
        # --- END OF WIDGET PLACING LOOP ---

        # You also need to define the validation methods, typically at the end of __init__ or as separate methods
        self._setup_validation_methods()


        # --- The rest of your __init__ code goes here ---
        # Frame 3: Output Information (Bottom Left)
        self.output_frame = ttk.Frame(self.master, bootstyle="info")
        self.output_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.output_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.output_frame, text="Output Information", bootstyle="inverse-info").pack(pady=10)

        self.output_text = ttk.Text(self.output_frame, height=10, state='disabled', wrap='word', bootstyle="info")
        self.output_text.pack(expand=True, fill='both', padx=5, pady=5)

        # Frame 1: Plots (Right side)
        self.plot_container_frame = ttk.Frame(self.master, bootstyle="secondary")
        self.plot_container_frame.grid(row=0, column=1, sticky='NSEW', padx=5, pady=5)
        self.plot_container_frame.grid_columnconfigure(0, weight=1)

        self.plot_container_frame.grid_rowconfigure(0, weight=2)
        self.plot_container_frame.grid_rowconfigure(1, weight=1)
        self.plot_container_frame.grid_rowconfigure(2, weight=1)

        self.plots = {}
        self.plot_setup('geometry', 'Engine Geometry', self.plot_container_frame, row=0)
        self.plot_setup('pt_data', 'Pressure and Temperature Profile', self.plot_container_frame, row=1)
        self.plot_setup('mach_data', 'Mach Number Profile', self.plot_container_frame, row=2)

        # Frame 4: Control Buttons (Bottom Right)
        self.button_frame = ttk.Frame(self.master, bootstyle="darkly")
        self.button_frame.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(self.button_frame, text="Start Calculation", command=self.StartButton, bootstyle="success").pack(pady=5)
        ttk.Button(self.button_frame, text="Stop", command=self.StopButton, bootstyle="danger").pack(pady=5)
        ttk.Button(self.button_frame, text="Reset", command=self.ResetButton, bootstyle="warning").pack(pady=5)


        return
        
    def _setup_validation_methods(self):
        # Validation for float inputs
        def validate_float_input(P):
            if P == "": return True
            try:
                float(P)
                return True
            except ValueError:
                return False
        self._validate_float_input = validate_float_input

        # Validation for int inputs
        def validate_int_input(P):
            if P == "": return True
            try:
                int(P)
                return True
            except ValueError:
                return False
        self._validate_int_input = validate_int_input
    
    def aastar(self,M,gamma):
        aas = (1/M)*(2/(gamma+1)*(1+((gamma-1)/2)*M**2))**((gamma+1)/(2*(gamma-1)))
        return aas

    def stagtemp(self,M,gamma):
        TT0 = (1+((gamma-1)/2)*M**2)**-1
        return TT0

    def mainfunc(self,gamma,R,rho_air,T2,u2,BVP,Tc,turbblade,diff_length,straight,theta,
                 D,n_points,d_nozzle,d_turbine,mdot_in,mdot_fuel_engine):
        pi = math.pi
        A1 = (pi*d_turbine**2)/4
        A2 = (pi*d_nozzle**2)/4
        T2 = T2+273.15
        u2 = u2*1000*(1/3600)
        M2 = u2/math.sqrt(gamma*R*T2)
        a2astar = self.aastar(M2,gamma)
        Astar = A2/a2astar
        
        M1 = sym.symbols('M1')
        a1astar = self.aastar(M1, gamma)
        M1eqn = sym.Eq(A1/Astar,a1astar)
        M1 = sym.solve(M1eqn,M1)
        M1 = M1[0]
        
        T2T0 = self.stagtemp(M2,gamma)
        T0 = T2/T2T0
        T1T0 = self.stagtemp(M1,gamma)
        T1 = T1T0*T0
        u1 = M1*math.sqrt(gamma*R*T1)
        
        radius_ab = d_turbine/2+0.01
        length_diff = 0.025
        Vlmax = BVP*(radius_ab/Tc)
        Cp = (gamma*R)/(gamma-1)
        T3 = T1+(u1**2/(2*Cp))-(Vlmax**2/(2*Cp))
        M3 = Vlmax/(math.sqrt(gamma*R*T3))
        # if M3 <= 0.4:
        #     pass      #Not implemented correctly. Will do later once GUI is built
        # else:
        #     ValueError("Mach number past the flame holder exceeds M = 0.4. This is not recomended. Proceed? (y/n)")
        #     return
        Tpost = 2100 #CHANGE THIS LATER ONCE STANJAN IS LOOPED IN
        Ppost = 220000 #SAME THING CHANGE THIS LATER
        Mpost = Vlmax/(math.sqrt(gamma*R*Tpost))
        A_combchamber = pi*(radius_ab**2)

        Mexit = 1 #Ideal case for a converging nozzle. Need to add various nozzles later
        Aexit = ((Mpost*A_combchamber)/Mexit)*math.sqrt(((1+((gamma-1)/2)*Mexit**2)/(1+((gamma-1)/2)*Mpost**2))**((gamma+1)/(gamma-1)))
        rexit = math.sqrt(Aexit/pi)
        
        #TODO: Will be finished later once functions/ data handling is sorted
        # self.update_geometryplt(x,y)
        # self.update_Mplt(x,M)
        # self.update_PTplt(x,p,t)
        
        return

    def plot_setup(self, name, title, parent_grid_frame, row):
        plot_sub_frame = ttk.Frame(parent_grid_frame, relief=ttk.RIDGE, borderwidth=2)
        plot_sub_frame.grid(row=row, column=0, sticky='NSEW', padx=5, pady=5)
        plot_sub_frame.grid_columnconfigure(0, weight=1)
        plot_sub_frame.grid_rowconfigure(0, weight=1)
        plot_sub_frame.grid_rowconfigure(1, weight=0)

        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.set_title(title)
        ax.set_xlabel('Axial Distance (m)')
        ax.set_ylabel('Parameter Value')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(figure, master=plot_sub_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky='NSEW')


        canvas.draw()

        self.plots[name] = {
            'frame': plot_sub_frame,
            'figure': figure,
            'ax': ax,
            'canvas': canvas
        }
        
    
    def update_geometryplt(self,x_data,y_data):
        ax = self.plots['geometry']['ax']
        canvas = self.plots['geometry']['canvas']
        ax.clear()
        ax.plot(x_data, y_data, label='Upper Radius', color='blue')
        ax.plot(x_data, [-r for r in y_data], label='Lower Radius', color='blue', linestyle='--') # Added lower radius for visual completeness
        ax.fill_between(x_data, y_data, [-r for r in y_data], alpha=0.1, color='blue')
        ax.set_title('Engine Geometry')
        ax.set_xlabel('Axial Distance (m)')
        ax.set_ylabel('Radius (m)')
        ax.legend()
        ax.grid(True)
        canvas.draw() 
        return
    
    def update_PTplt(self,x_data,p_data,t_data):
        ax = self.plots['pt_data']['ax']
        canvas = self.plots['pt_data']['canvas']
        ax.clear()
        ax.plot(x_data, p_data, label='Pressure (Pa)', color='red')
        ax.set_ylabel('Pressure (Pa)', color='red')
        ax.tick_params(axis='y', labelcolor='red')

        ax2 = ax.twinx()
        ax2.plot(x_data, t_data, label='Temperature (K)', color='blue')
        ax2.set_ylabel('Temperature (K)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        ax.set_title('Pressure and Temperature Profile')
        ax.set_xlabel('Axial Distance (m)')
        ax.grid(True)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='best')

        canvas.draw()
        return
    
    def update_Mplt(self):
        #TODO
        return  
    
    def Combustion(self,mdot_in,mdot_fuel,rho_air):
        mdot_in = mdot_in*10**-3
        mdot_fuel = mdot_fuel*(1/1000)*(1/60)
        mdot_total = rho_air*mdot_in
        mdot_air = mdot_total-mdot_fuel
        f_act = mdot_fuel/mdot_air
        
        MW_carbon = 12.011
        MW_oxygen = 15.999
        MW_nitrogen = 14.007
        MW_hydrogen = 1.0078
        #Using Jet A as a fuel. Assume it's composition is C12H24
        MW_fuel = 12*MW_carbon+24*MW_hydrogen
        #Assuming air is O2+3.74N2
        MW_oxidizer = 2*MW_oxygen+3.74*2*MW_nitrogen
        f_stoich = MW_fuel/(18*MW_oxidizer)
        
        phi = f_act/f_stoich
        
        #Need to figure out how to get STANJAN working in here. Might have some issues if I 
        #figure out how to get JetA into StanJan
        P3 = 2.179 #atm. NEED TO UPDATE WITH ENGINE DATA
        
        
        return
    
    def StartButton(self):
        """
        Executes the main calculation workflow when the Start button is pressed.
        Uses default/hardcoded values for now since GUI input elements are not implemented.
        """
        # gamma = float(self.gamma.get())
        # R = float(self.R.get())
        # rho_air = float(self.rho_air.get())
        # T2 = float(self.T2.get())
        # u2 = float(self.u2.get())
        # BVP = float(self.BVP.get())
        # Tc = float(self.Tc.get())
        # turbblade = float(self.turbblade.get())
        # diff_length = float(self.diff_length.get())
        # straight = float(self.straight.get())
        # theta = float(self.theta.get())
        # D = float(self.D.get())
        # n_points = int(self.n_points.get())
        # d_nozzle = float(self.d_nozzle.get())
        # d_turbine = float(self.d_turbine.get())
        # mdot_in = float(self.mdot_in.get())
        # mdot_fuel_engine = float(self.mdot_fuel.get())
        
        # try:
        #     # Execute main calculation
        #     self.mainfunc(gamma, R, rho_air, T2, u2, BVP, Tc, turbblade, 
        #                  diff_length, straight, theta, D, n_points, d_nozzle, 
        #                  d_turbine, mdot_in, mdot_fuel_engine)
            
        #     # Execute combustion analysis
        #     self.Combustion(mdot_in, mdot_fuel_engine, rho_air)
            
            
        # except Exception as e:
        #     print(f"Error during calculation: {e}")
        
        return
    
    def ResetButton(self):
        #TODO Implement later
        return
    
    def StopButton(self):
        #TODO Implement later
        return

    def run(self):
        return


class UnitConversionToolbox:
    def temp_conversion(self, value, input_units, output_units):
        """
        Description: 
            Converts between F, C, and K
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if input_units.upper() == 'C':
            K = value+273.15
        elif input_units.upper() == 'K':
            K = value
        elif input_units.upper() == 'F':
            K = (value-32)*5/9+273.15
        else:
            raise ValueError(f"Internal Error: Unrecognized input unit '{input_units}'")

        if output_units.upper() == 'C':
            return K-273.15
        elif output_units.upper() == 'F':
            return (K-273.15)*9/5+32
        elif output_units.upper() == 'K':
            return K
        else:
            raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def pressure_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between bar, atm, Pa
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if input_units.lower() == 'bar':
            Pa = value*100000
        elif input_units.lower() == 'atm':
            Pa = value *101325
        elif input_units == 'Pa':
            Pa = value
        else:
            raise ValueError(f"Internal Error: Unrecognized input unit '{input_units}'") 
            
        if output_units.lower() == 'bar':    
             return Pa/100000
        elif output_units.lower() == 'atm':
            return Pa/101325
        elif output_units == 'Pa':
            return Pa
        else:
            raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def velocity_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between m/s, km/hr, and mph
        Args: 
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if input_units == 'km/hr':
            mps = value *(3600/1000)
        elif input_units == 'mph':
            mps = value/2.23694
        elif input_units == 'm/s':
            mps = value
        else:
            return None
            #raise ValueError(f"Internal Error: Unrecognized input unit'{input_units}'")
            
        if output_units == 'km/hr':
            return mps*(1000/3600)
        elif output_units == 'mph':
            return mps*2.23694
        elif output_units == 'm/s':
            return mps
        else:
            return None
            #raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def volume_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between L, m^3, and cm^3
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        #TODO: Check the unit conversions here. Not entirely sure that this is done correctly
        if input_units == 'm^3':
            L = value*1000
        elif input_units == 'cm^3':
            L = value/1000
        elif input_units == 'L':
            L = value
        else:
            return None
        
        if output_units == 'm^3':
            return L/1000
        elif output_units == 'cm^3':
            return L*1000
        elif output_units == 'L':
            return L
        else:
            return None
        
    def massflow_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between kg/s, kg/min, g/min
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        # Convert to kg/s as base unit
        if input_units == 'kg/s':
            kg_per_s = value
        elif input_units == 'kg/min':
            kg_per_s = value / 60
        elif input_units == 'g/min':
            kg_per_s = value / 1000 / 60
        else:
            return None
            
        # Convert from kg/s to desired output units
        if output_units == 'kg/s':
            return kg_per_s
        elif output_units == 'kg/min':
            return kg_per_s * 60
        elif output_units == 'g/min':
            return kg_per_s * 1000 * 60
        else:
            return None

    def volflow_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between m^3/s, L/s, m^3/min, L/min
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        # Convert to m^3/s as base unit
        if input_units == 'm^3/s':
            m3_per_s = value
        elif input_units == 'L/s':
            m3_per_s = value / 1000
        elif input_units == 'm^3/min':
            m3_per_s = value / 60
        elif input_units == 'L/min':
            m3_per_s = value / 1000 / 60
        else:
            return None
            
        # Convert from m^3/s to desired output units
        if output_units == 'm^3/s':
            return m3_per_s
        elif output_units == 'L/s':
            return m3_per_s * 1000
        elif output_units == 'm^3/min':
            return m3_per_s * 60
        elif output_units == 'L/min':
            return m3_per_s * 1000 * 60
        else:
            return None
    def mass2vol_conversion(self,rho, value, input_units, output_units):
        """
        Description:
            Converts between kg/s, m^3/s
        Args:
            rho (float): density in kg/m^3
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if rho <= 0:
            return None
            
        if input_units == 'kg/s' and output_units == 'm^3/s':
            return value / rho
        elif input_units == 'm^3/s' and output_units == 'kg/s':
            return value * rho
        else:
            return None
    
    
class Settings:
    def plotcolors(self):
        #TODO: implement once GUI is setup
        return
    def theme(self):

        
        
        return
    def fontstyle(self):
        #TODO: implement once GUI is setup
        return
    def fontsize(self):
        #TODO: implement once GUI is setup
        return
    
    
if __name__ == "__main__":
    root = Window(themename='darkly')
    app = Ignition(root)
    root.mainloop()