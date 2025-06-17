"""
Author: Jordan Handy
Last Updated: 05/24/2025
Contact: jhandy03@vt.edu

Repo: https://github.com/jhandy03/Ignition

Written for MachWorks @ Virgnia Tech's Propulsion Subteam


"""
import customtkinter as ctk
from GUI.gui import GUI
from Optimization.optimization_testing import Ignition_Optimization
from Settings.settings import Settings
from UnitConversionToolbox.unitconversiontoolbox import UnitConversionToolbox
from MainCalculations.main_calculations import Ignition
    
if __name__ == "__main__":
    self.root = ctk.CTk()
    ignition = Ignition(master)
    settings = Settings()
    gui = GUI(root)
    uctb = UnitConversionToolbox()
    optim = Ignition_Optimization()
    