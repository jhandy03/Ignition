"""
Author: Jordan Handy
Last Updated: 05/24/2025
Contact: jhandy03@vt.edu

Written for MachWorks @ Virgnia Tech's Propulsions Subteam

MIT Liscense or sum shit idk

"""

def aastar(self,M,gamma):
    aas = (1/M)*(2/(gamma+1)*(1+((gamma-1)/2)*M^2))^((gamma+1)/(2*(gamma-1)))
    return aas

def stagtemp(self,M,gamma):
    TT0 = (1+((gamma-1)/2)*M^2)^-1
    return TT0

