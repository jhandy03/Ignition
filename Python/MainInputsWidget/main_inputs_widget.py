import customtkinter as ctk
class MainInputsWidget:
    def __init__(self, parent, value='', label_front='Input', label_rear='Units'):
        self.label_front = ctk.CTkLabel(parent, text=label_front,font=("Computer Modern", 15))
        self.entry = ctk.CTkEntry(parent)
        self.entry.insert(0, value)
        self.label_rear = ctk.CTkLabel(parent, text=label_rear,font=("Computer Modern", 15))

    def grid(self, row, column, padx=10, pady=5, sticky='ew'):
        self.label_front.grid(row=row,column=column, padx=padx,pady=pady, sticky='e')
        self.entry.grid(row=row,column=column+1, padx=padx,pady=pady, sticky=sticky)
        self.label_rear.grid(row=row,column=column+2, padx=padx,pady=pady, sticky='w')
        
    def get(self):
       return self.entry.get() 