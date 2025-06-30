import customtkinter as ctk
import matplotlib.pyplot as plt
import time
import datetime

class Settings:
    def __init__(self, gui_instance):
        self.gui = gui_instance
    
    def set_theme(self,theme):
        self.theme = theme
        if theme == 'Dark':
            ctk.set_appearance_mode("dark")
        elif theme == 'Light':
            ctk.set_appearance_mode("light")
        elif theme == 'System':
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode("dark")
    
    def plotcolors(self,color):
        self.color = color
        
        if color == 'Dark':
            self.rcParams = {'axes.facecolor': '#4b4b4b',
                             'axes.edgecolor': '#2b2b2b',
                             'axes.labelcolor': 'white',
                             'xtick.color': 'white',
                             'ytick.color': 'white',
                             'text.color': 'white',
                             'axes.titlecolor': 'white'}
        elif color == 'Light':
            self.rcParams = {'axes.facecolor': "#ffffff",
                             'axes.edgecolor': "#b8b8b8",
                             'axes.labelcolor': 'black',
                             'xtick.color': 'black',
                             'ytick.color': 'black',
                             'text.color': 'black',
                             'axes.titlecolor': 'black'}
            
        elif color == "Don't":
            self.rcParams = {'axes.facecolor': "#FF00FF",
                             'axes.edgecolor': "#FF00FF",
                             'axes.labelcolor': 'r',
                             'xtick.color': 'r',
                             'ytick.color': 'r',
                             'text.color': 'r',
                             'axes.titlecolor': 'r'}
        
        else:
            raise ValueError("Invalid option")
            
        
        plt.rcParams.update(self.rcParams)
        if hasattr(self.gui, 'figures'):
            for fig in self.gui.figures:
                fig.set_facecolor(self.rcParams['axes.facecolor'])
                for ax in fig.axes:
                    ax.set_facecolor(self.rcParams['axes.facecolor'])
                    ax.set_title(ax.get_title(), color=self.rcParams['axes.titlecolor'])
                    ax.set_xlabel(ax.get_xlabel(), color=self.rcParams['axes.labelcolor'])
                    ax.set_ylabel(ax.get_ylabel(), color=self.rcParams['axes.labelcolor'])
                    ax.tick_params(axis='x', colors=self.rcParams['xtick.color'])
                    ax.tick_params(axis='y', colors=self.rcParams['ytick.color'])
                fig.canvas.draw()
            
    def fontstyle(self):
        #TODO: implement once GUI is setup
        return
   
    def fontsize(self):
        #TODO: implement once GUI is setup
        return
    
    def logging_setup(self,frame):
        self.logbox = ctk.CTkTextbox(frame, width=500, height=225, font=("Computer Modern", 15), text_color = '#34a6c2') #TODO: revise color
        self.logbox.grid(row=1,column=0, padx=10, pady=10, sticky="nsew")
        
    def log_event(self,event_message, start_time, end_time):
        current_time = datetime.datetime.now().strftime('%I:%M:%S %p').lower()
        elapsed = end_time - start_time
        if elapsed > 0:
            log_message = f"{current_time} | {event_message} | Processing Time: {elapsed:.6f} sec \n"
        elif elapsed <=0:
            log_message = f"{current_time} | {event_message} \n"
        else:
            log_message = f"{current_time} | Error\n"
        
        self.logbox.configure(state='normal')
        self.logbox.insert("end", log_message)
        self.logbox.configure(state='disabled')
    
    #TODO: add progress bar
    