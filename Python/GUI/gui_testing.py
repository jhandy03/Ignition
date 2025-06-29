import customtkinter as ctk
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


current_style_index = 0

def theme():
    global current_style_index
    current_style_index = (current_style_index + 1) % len(plt.style.available)
    plt.style.use(plt.style.available[current_style_index])
    
    # Redraw the plot with new style
    ax.clear()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Sample Plot')
    canvas.draw()
    
    # Update button text to current theme name
    themebutton.configure(text=plt.style.available[current_style_index])

root = ctk.CTk()
root.title("Ignition")
ctk.set_appearance_mode("dark")
root.geometry("800x600")

# Configure grid weights for proper resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_title('Sample Plot')

canvas = FigureCanvasTkAgg(fig, root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

themebutton = ctk.CTkButton(root, text=plt.style.available[current_style_index], command=theme)
themebutton.grid(row=1, column=0, pady=10)

root.protocol("WM_DELETE_WINDOW", root.quit)


if __name__ == "__main__":
    root.mainloop()