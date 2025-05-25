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
import tkinter
import pillow as pw
import ttkbootstrap as ttk #used to make the app look a little nicer. For use with tkinter but not sure I want to continue with that



class Ignition:
    def __init__(self):
        self.gamma = 2 #not sure if I need to init every single variable used. Revist later
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

    def plotstuff(self):
        #Implement later
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
    
    
    def ResetButton(self):
        #Implement later
        return
    
    def StopButton(self):
        #Implement later
        return

    def run(self):
        self.root.mainloop()


class UnitConversionToolbox:
    def temp_conversion(self):
        
        return
    def pressure_conversion(self):
        
        return
    def velocity_conversion(self):
        
        return
    def volume_conversion(self):
        
        return
    def massflow_conversion(self):
        
        return
    def volflow_conversion(self):
        
        return
    def mass2vol_conversion(self,rho):
        
        return
    
    
class Settings:
    def plotcolors(self):
        return
    def theme(self):
        return
    def fontstyle(self):
        return
    def fontsize(self):
        return
    