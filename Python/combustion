import cantera as ct
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

T_initial = 1073.15 
P_initial = 2.1 * ct.one_atm 

fuel_comp = 'NC10H22:0.74, PHC3H7:0.15, CYC9H18:0.11'
ox_comp = 'O2:1,N2:3.76'
gas_mech = 'Luche.yaml'
phi = 1.0

delta_h = 0.36e6 #J/kg

gas = ct.Solution(gas_mech)
gas.TP = T_initial, P_initial
gas.set_equivalence_ratio(phi, fuel=fuel_comp, oxidizer=ox_comp)


temp_guesses = []
residuals = []


indicies = [17,18,23]
MW_fuel = sum(gas.molecular_weights[i] for i in indicies)
print(MW_fuel)

# for i in range(len(gas.molecular_weights)):
#     print(gas.molecular_weights[i])
# print(len(gas.molecular_weights))
    
def balance(Temp_guess):
    Temp_guess = float(Temp_guess)
    gas.TP = T_initial, P_initial # important cantara
    gas.set_equivalence_ratio(phi, fuel=fuel_comp, oxidizer=ox_comp)

    h_vapor = delta_h / gas.molecular_weights[0]
    h_init = gas.enthalpy_mass + h_vapor  # important cantara
    
    gas.TP = Temp_guess, P_initial
    gas.equilibrate('HP') # important cantara
    h_comb = gas.enthalpy_mass # important cantara
    
    residual = h_init - h_comb
    
    temp_guesses.append(Temp_guess)
    residuals.append(residual)
    
    print(f"Temp_guess: {Temp_guess:.2f} K")
    return residual

final_temp = fsolve(balance, T_initial, xtol=1e-6)[0]
print(f"Adiabatic Flame Temperature: {final_temp:.2f} K")

plt.figure(figsize=(8, 6))
plt.plot(range(len(temp_guesses)), temp_guesses, marker='o', linestyle='-', color='b')
plt.xlabel('iteration number')
plt.ylabel('Temperature Guess (K)')
plt.title('Iteration vs Temp Guess')
plt.grid()
plt.xticks(range(0,len(temp_guesses)+1,1))
plt.show()
