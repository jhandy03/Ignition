import math
import sympy as sym
class MainCalculations:
    def __init__(self):
        pass
       
 
    
    def aastar(self,M,gamma):
        aas = (1/M)*(2/(gamma+1)*(1+((gamma-1)/2)*M**2))**((gamma+1)/(2*(gamma-1)))
        return aas

    def stagtemp(self,M,gamma):
        TT0 = (1+((gamma-1)/2)*M**2)**-1
        return TT0

    def main_calculations(self,gamma,R,rho_air,T2,u2,BVP,Tc,turbblade,diff_length,straight,theta,
                 D,d_nozzle,d_turbine,mdot_in,mdot_fuel_engine):
        pi = math.pi
        A1 = (pi*d_turbine**2)/4
        A2 = (pi*d_nozzle**2)/4
        T2 = T2+273.15 #TODO: might just want to take K instead of C
        u2 = u2*1000*(1/3600) #TODOL: might just want to take m/s instead of km/h
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
        Tpost = 2100 #TODO: Update
        Ppost = 220000 #TODO: Update
        Mpost = Vlmax/(math.sqrt(gamma*R*Tpost))
        A_combchamber = pi*(radius_ab**2)

        Mexit = 1 #Ideal case for a converging nozzle. Need to add various nozzles later
        Aexit = ((Mpost*A_combchamber)/Mexit)*math.sqrt(((1+((gamma-1)/2)*Mexit**2)/(1+((gamma-1)/2)*Mpost**2))**((gamma+1)/(gamma-1)))
        rexit = math.sqrt(Aexit/pi)
        
        #TODO: Placeholder values for some things that will be implemented later (combustion et al)
        phi = 0.5
        f_act = 0.95
        f_stoich = 0.06
        thrust = 5000
        
        return {'thrust': thrust, 'Tpost': Tpost, 'Ppost': Ppost, 'Mexit': Mexit, 'phi': phi,
                'f_act': f_act, 'f_stoich': f_stoich}
        
        