"""
Author: Jordan Handy
Last Updated: 05/24/2025
Contact: jhandy03@vt.edu

Repo: https://github.com/jhandy03/Ignition

Written for MachWorks @ Virgnia Tech's Propulsion Subteam


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


   
    
if __name__ == "__main__":
    root = Window(themename='darkly')
    app = Ignition(root)
    app.run()