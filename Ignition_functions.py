"""
Author: Jordan Handy
Last Updated: 05/24/2025
Contact: jhandy03@vt.edu

Written for MachWorks @ Virgnia Tech's Propulsions Subteam

MIT Liscense or sum shit idk

"""
import math
import sympy as sym
import ttkbootstrap as ttk #used to make the app look a little nicer. For use with tkinter but not sure I want to continue with that



class Ignition:
    def aastar(self,M,gamma):
        aas = (1/M)*(2/(gamma+1)*(1+((gamma-1)/2)*M^2))^((gamma+1)/(2*(gamma-1)))
        return aas

    def stagtemp(self,M,gamma):
        TT0 = (1+((gamma-1)/2)*M^2)^-1
        return TT0

    def mainfunc(self,gamma,R,rho_air,T2,u2,BVP,Tc,turbblade,diff_length,straight,theta,
                 D,n_points,d_nozzle,d_turbine,mdot_in,mdot_fuel_engine):
        pi = math.pi
        A1 = (pi*d_turbine**2)/4
        A2 = (pi*d_nozzle**2)/4
        T2 = T2+273.15
        
        return


    def run(self):
        self.root.mainloop()
        