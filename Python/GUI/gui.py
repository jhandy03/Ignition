import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class GUI:
    def __init__(self,root):
        self.root = root
        self.main_window(root)
        # self.running = True #want to implement a start and stop button
        
    def main_window(self,root):
        
        self.root.title("Ignition")
        ctk.set_appearance_mode("dark")
        self.root._state_before_windows_set_titlebar_color = 'zoomed'
        