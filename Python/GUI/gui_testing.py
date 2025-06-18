import customtkinter as ctk

root = ctk.CTk()   #create main window
root.title("Ignition")     #name of the window
ctk.set_appearance_mode("dark") #set default theme to dark. Will add ability to change later
root._state_before_windows_set_titlebar_color = 'zoomed' #fullscreen the window

#Creates the mains tabs of Ignition and then assigns them to variables. Makes things easier to type later
tabs = ctk.CTkTabview(root, width=300, height=300, anchor="w") #anchor='w' make them left aligned
tabs.pack(padx=20, pady=20, fill="both", expand=True, anchor="w")
tabs.add("Main")
tabs.add("Settings")
maintab = tabs.tab("Main")
settingstab = tabs.tab("Settings")  #may add more later

maintab.grid_rowconfigure(0, weight=1)
maintab.grid_columnconfigure(0, weight=2)
maintab.grid_columnconfigure(1, weight=1)

leftframe = ctk.CTkFrame(maintab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
leftframe.grid(row=0,column=0, padx=15, pady=15, sticky="nsew") 
rightframe = ctk.CTkFrame(maintab, fg_color="#2b2b2b", border_width=2, border_color="#4a4a4a")
rightframe.grid(row=0,column=1, padx=15, pady=15, sticky="nsew")

leftframe.grid_rowconfigure(0,weight=1)
leftframe.grid_rowconfigure(2,weight=1)
leftframe.grid_rowconfigure(4,weight=1)
leftframe.grid_rowconfigure(1,weight=2)
leftframe.grid_rowconfigure(3,weight=2)

leftframe_bottom = ctk.CTkFrame(leftframe, fg_color="#3a3a3a", border_width=2, border_color="#5a5a5a")
leftframe_bottom.grid(row=4,column=0, padx=15, pady=15, sticky="nsew") 

geninputslabel = ctk.CTkLabel(leftframe, text="General Inputs", font=("Courier New Bold", 18), text_color="#ffffff")
geninputslabel.grid(row=1, column=0, padx=20, pady=10, sticky="w")


# --- 20 Inputs in 2 columns of 10, each as label-entry-label ---
input_entries = []
num_columns = 2
inputs_per_column = 10

for i in range(20):
    col = i // inputs_per_column  # 0 or 1
    row = i % inputs_per_column   # 0 to 9

    label1 = ctk.CTkLabel(leftframe, text=f"Input {i+1}", text_color="#ffffff")
    entry = ctk.CTkEntry(leftframe)
    label2 = ctk.CTkLabel(leftframe, text="units", text_color="#aaaaaa")

    grid_col = col * 3  # Each group takes 3 columns

    label1.grid(row=row+2, column=grid_col, padx=5, pady=2, sticky="e")
    entry.grid(row=row+2, column=grid_col + 1, padx=5, pady=2, sticky="ew")
    label2.grid(row=row+2, column=grid_col + 2, padx=5, pady=2, sticky="w")

    input_entries.append(entry)

# Make entry columns expand
for c in range(1, num_columns * 3, 3):
    leftframe.grid_columnconfigure(c, weight=1)

if __name__ == "__main__":
    root.mainloop()