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
import PIL
import ttkbootstrap as ttk #used to make the app look a little nicer. For use with tkinter but not sure I want to continue with that
from ttkbootstrap.constants import LEFT, RIGHT, TOP, BOTTOM, CENTER #specific constants instead of wildcard import
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

class Ignition:
    def __init__(self,master):
        self.master = master
        master.title('Ignition V 0.0.1')
        
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(0,weight=1)
        
        self.plot_frame = ttk.Frame(self.master)
        self.plot_frame.grid(row=0,column=0,sticky=ttk.NSEW)
        self.plot_frame.grid_columnconfigure(0,weight=1)
        self.plot_frame.grid_rowconfigure(0,weight=0)
        
        self.fig, self.ax, self.canvas, self.toolbar = self.plotstuff(self.plot_frame)
        return
    
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
        
        return

    def plotstuff(self,parent_frame, title):
        figure = Figure(figsize=(6,4),dpi=100)
        ax = figure.add_subplot(111)
        ax.set_title(title)
        ax.set_xlabel('Axial Distance (m)')
        ax.set_ylabel('Flow Parameters')
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(figure,master=parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=ttk.TOP,fill=ttk.BOTH,expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas,parent_frame)
        toolbar.update()
        toolbar.pack(side=ttk.BOTTOM,fill=ttk.X)
        
        canvas.draw()
        return figure,ax, canvas, toolbar
    
    def update_machplt(self):
        self.ax1.clear()
        
    
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
        return
    
    def ResetButton(self):
        #Implement later
        return
    
    def StopButton(self):
        #Implement later
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
    root = tk.Tk()
    app = Ignition(root)
    root.mainloop()