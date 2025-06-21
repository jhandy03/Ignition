import customtkinter as ctk
import numpy as np
import cantera as ct


root = ctk.CTk()   #create main window
root.title("Ignition")     #name of the window
ctk.set_appearance_mode("dark") #set default theme to dark. Will add ability to change later
root.geometry("800x600")  #set default window size



if __name__ == "__main__":
    root.mainloop()