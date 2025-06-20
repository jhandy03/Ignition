
class Ignition:
    def __init__(self,master):
        self.master = master
        master.title('Ignition V 0.0.1')
        self.master.state('zoomed')

        #Configure main window
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1,weight=1)
        #self.master.grid_rowconfigure(2,weight=1)
        
        #configure plot frame. sets sizes of the rows and columns
        self.plot_container_frame = ttk.Frame(self.master)
        self.plot_container_frame.grid(row=0,column=1, sticky='NSEW',padx=1,pady=1)
        self.plot_container_frame.grid_columnconfigure(0,weight=1)
        self.plot_container_frame.grid_rowconfigure(0, weight=1)
        self.plot_container_frame.grid_rowconfigure(1, weight=10)
        self.plot_container_frame.grid_rowconfigure(2, weight=10)
        
        #starts the 3 plots??
        self.plots = {}
        self.plot_setup('geometry', 'Engine Geometry', self.plot_container_frame, row=0)
        self.plot_setup('pt_data', 'Pressure and Temperature Profile', self.plot_container_frame, row=1)
        self.plot_setup('mach_data', 'Mach Number Profile', self.plot_container_frame, row=2)
        
        #General inputs frame
        self.general_inputs_frame = ttk.Frame(self.master)
        self.general_inputs_frame.grid(row=0,column=0, sticky='NSEW',padx=1,pady=1)
        
        #Configures the rows and col for the gen inputs. 18 total inputs split into 3 col and 6 rows
        for i in range(7):
            self.general_inputs_frame.grid_rowconfigure(i,weight=1)
        
        #configures col 0,3,6  1,4,7  2,5,8
        for i in range(3):
            self.general_inputs_frame.grid_columnconfigure(i*3,weight=1)
            self.general_inputs_frame.grid_columnconfigure(i*3+1,weight=2)
            self.general_inputs_frame.grid_columnconfigure(i*3+2,weight=1)
            
        ttk.Label(self.general_inputs_frame,text='General Inputs').grid(row=0,column=0,columnspan=9,pady=1,sticky='EW')
        
        # Set up validation methods first
        self._setup_validation_methods()
        
        #TODO: revisit the parameters since the names/ values are not entirely correct
        #Will need to be updated with additional user inputs (ie all the stoich stuff/ combustion, or other?? Maybe the unit conversion stuff?)
        self.input_vars = {'gamma':tk.DoubleVar(value=1.4),'R':tk.DoubleVar(value=287),'rho_air':tk.DoubleVar(value=1.225),
                   'EGT':tk.DoubleVar(value=800),'u_exit':tk.DoubleVar(value=1200),'BVP':tk.DoubleVar(value=1),
                   'ITP':tk.DoubleVar(value=0.9515),'mdot_in':tk.DoubleVar(value=1),'length_turbine':tk.DoubleVar(value=1),
                   'length_diff':tk.DoubleVar(value=1),'straight':tk.DoubleVar(value=1),'half_angle':tk.DoubleVar(value=15),
                   'flame_height':tk.DoubleVar(value=1),'noz_diameter':tk.DoubleVar(value=1),'turb_diameter':tk.DoubleVar(value=1),
                   'mdot_fuel':tk.DoubleVar(value=1),'plot_points':tk.IntVar(value=1000),'M_diff':tk.DoubleVar(value=1)}
        self.input_params = [('Gamma:',self.input_vars['gamma']," "),('R:',self.input_vars['R'],'J/(kg*K)'),
                    ('Air Density:',self.input_vars['rho_air'],'kg/m³'),('EGT:',self.input_vars['EGT'],'°C'),
                    ('Exit Velocity:',self.input_vars['u_exit'],'km/hr'),('Blowout Velocity Parameter:',self.input_vars['BVP'],''),
                    ('Ignition Time Parameter:',self.input_vars['ITP'],' '),('Mass Flow In:',self.input_vars['mdot_in'],'L/s'),
                    ('Turbine Length:',self.input_vars['length_turbine'],'m'),('Diffuser Length:',self.input_vars['length_diff'],'m'),
                    ('Straight Length:',self.input_vars['straight'],'m'),('Half Angle:',self.input_vars['half_angle'],'°'),
                    ('Flame Height:',self.input_vars['flame_height'],'m'),('Nozzle Diameter:',self.input_vars['noz_diameter'],'m'),
                    ('Turbine Diameter:',self.input_vars['turb_diameter'],'m'),('Fuel Mass Flow:',self.input_vars['mdot_fuel'],'g/min'),
                    ('Plot Points:',self.input_vars['plot_points'],' '),('Mach Number Post Diffuser:',self.input_vars['M_diff'],' ')]

        current_grid_row_for_inputs=1
        for i,(label_text,var_obj,unit_text) in enumerate(self.input_params):
# Calculate the row number within input_frame.
            # (i // 3) increments the row every 3 items.
            row_in_frame = current_grid_row_for_inputs + (i // 3)
            
            # Calculate the starting physical column for this group of (Label, Entry, Unit).
            # (i % 3) cycles through 0, 1, 2 for the logical groups.
            # * 3 converts this to the actual starting physical column (0, 3, or 6).
            start_physical_col = (i % 3) * 3 

            # Configure this specific row to expand proportionally
            #self.general_inputs_frame.grid_rowconfigure(row_in_frame, weight=1)

            # Place the Label (e.g., "Gamma:", "R:")
            ttk.Label(self.general_inputs_frame, text=label_text).grid(
                row=row_in_frame, column=start_physical_col,
                pady=2, padx=5, sticky='w' # 'w' for west (left) alignment
            )
            
            # Place the Entry widget
            # Use type checking to ensure correct validation function is called
            if isinstance(var_obj, tk.IntVar):
                ttk.Entry(self.general_inputs_frame, textvariable=var_obj, validate="key",
                          validatecommand=(self.master.register(self._validate_int_input), '%P')).grid(
                    row=row_in_frame, column=start_physical_col + 1,
                    pady=2, padx=5, sticky='ew' # 'ew' for expand horizontally
                )
            else: # Assume DoubleVar
                ttk.Entry(self.general_inputs_frame, textvariable=var_obj, validate="key",
                          validatecommand=(self.master.register(self._validate_float_input), '%P')).grid(
                    row=row_in_frame, column=start_physical_col + 1,
                    pady=2, padx=5, sticky='ew'
                )

            # Place the Unit/Description Label
            # Only show if there's actual text (not just empty space or None)
            if unit_text.strip():
                ttk.Label(self.general_inputs_frame, text=unit_text).grid(
                    row=row_in_frame, column=start_physical_col + 2,
                    pady=2, padx=5, sticky='w'
                )
        # --- END OF WIDGET PLACING LOOP ---

        # --- The rest of your __init__ code goes here ---


        # --- The rest of your __init__ code goes here ---
        # Frame 3: Output Information (Bottom Left)
        self.output_frame = ttk.Frame(self.master)
        self.output_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.output_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.output_frame, text="Output Information").pack(pady=10)

        self.output_text = ttk.Text(self.output_frame, height=10, state='disabled', wrap='word')
        self.output_text.pack(expand=True, fill='both', padx=5, pady=5)


        # Frame 4: Control Buttons (Bottom Right)
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)
        self.button_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(self.button_frame, text="Start Calculation", command=self.StartButton).pack(pady=5)
        ttk.Button(self.button_frame, text="Stop", command=self.StopButton).pack(pady=5)
        ttk.Button(self.button_frame, text="Reset", command=self.ResetButton).pack(pady=5)


    
        
    def _setup_validation_methods(self):
        # Validation for float inputs
        def validate_float_input(P):
            if P == "": return True
            try:
                float(P)
                return True
            except ValueError:
                return False
        self._validate_float_input = validate_float_input

        # Validation for int inputs
        def validate_int_input(P):
            if P == "": return True
            try:
                int(P)
                return True
            except ValueError:
                return False
        self._validate_int_input = validate_int_input
    
    def aastar(self,M,gamma):
        aas = (1/M)*(2/(gamma+1)*(1+((gamma-1)/2)*M**2))**((gamma+1)/(2*(gamma-1)))
        return aas

    def stagtemp(self,M,gamma):
        TT0 = (1+((gamma-1)/2)*M**2)**-1
        return TT0

    def mainfunc(self,gamma,R,rho_air,T2,u2,BVP,Tc,turbblade,diff_length,straight,theta,
                 D,n_points,d_nozzle,d_turbine,mdot_in,mdot_fuel_engine):
        # pi = math.pi
        # A1 = (pi*d_turbine**2)/4
        # A2 = (pi*d_nozzle**2)/4
        # T2 = T2+273.15
        # u2 = u2*1000*(1/3600)
        # M2 = u2/math.sqrt(gamma*R*T2)
        # a2astar = self.aastar(M2,gamma)
        # Astar = A2/a2astar
        
        # M1 = sym.symbols('M1')
        # a1astar = self.aastar(M1, gamma)
        # M1eqn = sym.Eq(A1/Astar,a1astar)
        # M1 = sym.solve(M1eqn,M1)
        # M1 = M1[0]
        
        # T2T0 = self.stagtemp(M2,gamma)
        # T0 = T2/T2T0
        # T1T0 = self.stagtemp(M1,gamma)
        # T1 = T1T0*T0
        # u1 = M1*math.sqrt(gamma*R*T1)
        
        # radius_ab = d_turbine/2+0.01
        # length_diff = 0.025
        # Vlmax = BVP*(radius_ab/Tc)
        # Cp = (gamma*R)/(gamma-1)
        # T3 = T1+(u1**2/(2*Cp))-(Vlmax**2/(2*Cp))
        # M3 = Vlmax/(math.sqrt(gamma*R*T3))
        # # if M3 <= 0.4:
        # #     pass      #Not implemented correctly. Will do later once GUI is built
        # # else:
        # #     ValueError("Mach number past the flame holder exceeds M = 0.4. This is not recomended. Proceed? (y/n)")
        # #     return
        # Tpost = 2100 #CHANGE THIS LATER ONCE STANJAN IS LOOPED IN
        # Ppost = 220000 #SAME THING CHANGE THIS LATER
        # Mpost = Vlmax/(math.sqrt(gamma*R*Tpost))
        # A_combchamber = pi*(radius_ab**2)

        # Mexit = 1 #Ideal case for a converging nozzle. Need to add various nozzles later
        # Aexit = ((Mpost*A_combchamber)/Mexit)*math.sqrt(((1+((gamma-1)/2)*Mexit**2)/(1+((gamma-1)/2)*Mpost**2))**((gamma+1)/(gamma-1)))
        # rexit = math.sqrt(Aexit/pi)
        
        #TODO: Will be finished later once functions/ data handling is sorted
        # self.update_geometryplt(x,y)
        # self.update_Mplt(x,M)
        # self.update_PTplt(x,p,t)
         #Dummy data for plots so they show something when Start is pressed
        x_data = [i * 0.1 for i in range(n_points)] if n_points > 0 else [0]
        y_data_geom = [0.1 + 0.05 * math.sin(val) for val in x_data]
        p_data = [101325 + 50000 * math.cos(val) for val in x_data]
        t_data = [288 + 50 * math.sin(val) for val in x_data]
        mach_data = [0.5 + 0.2 * math.sin(val) for val in x_data]

        self.update_geometryplt(x_data,y_data_geom)
        self.update_Mplt(x_data, mach_data) # Ensure x_data and mach_data are passed
        self.update_PTplt(x_data,p_data,t_data)

        # Update output information
        output_str = (
            f"Calculation placeholder complete!\n"
            f"Gamma: {gamma}\n"
            f"R: {R}\n"
            f"Plot Points: {n_points}\n"
            f"This is dummy data. Implement actual calculations later.\n"
        )
        self.update_output(output_str)
        return

    def plot_setup(self, name, title, parent_grid_frame, row):
        plot_sub_frame = ttk.Frame(parent_grid_frame, borderwidth=2)
        plot_sub_frame.grid(row=row, column=0, sticky='NSEW', padx=5, pady=5)
        plot_sub_frame.grid_columnconfigure(0, weight=1)
        plot_sub_frame.grid_rowconfigure(0, weight=1)
        plot_sub_frame.grid_rowconfigure(1, weight=0)

        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        figure.subplots_adjust(bottom=0.2,left=0.1)
        ax.set_title(title)
        ax.set_xlabel('Axial Distance (m)')
        ax.set_ylabel('Parameter Value')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(figure, master=plot_sub_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky='NSEW')


        canvas.draw()

        self.plots[name] = {
            'frame': plot_sub_frame,
            'figure': figure,
            'ax': ax,
            'canvas': canvas
        }
        
    
    def update_geometryplt(self,x_data,y_data):
        ax = self.plots['geometry']['ax']
        canvas = self.plots['geometry']['canvas']
        ax.clear()
        ax.plot(x_data, y_data, label='Upper Radius', color='blue')
        ax.plot(x_data, [-r for r in y_data], label='Lower Radius', color='blue', linestyle='--') # Added lower radius for visual completeness
        ax.fill_between(x_data, y_data, [-r for r in y_data], alpha=0.1, color='blue')
        ax.set_title('Engine Geometry')
        ax.set_xlabel('Axial Distance (m)')
        ax.set_ylabel('Radius (m)')
        ax.legend()
        ax.grid(True)
        canvas.draw() 
        return
    
    def update_PTplt(self,x_data,p_data,t_data):
        ax = self.plots['pt_data']['ax']
        canvas = self.plots['pt_data']['canvas']
        ax.clear()
        ax.plot(x_data, p_data, label='Pressure (Pa)', color='red')
        ax.set_ylabel('Pressure (Pa)', color='red')
        ax.tick_params(axis='y', labelcolor='red')

        ax2 = ax.twinx()
        ax2.plot(x_data, t_data, label='Temperature (K)', color='blue')
        ax2.set_ylabel('Temperature (K)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        ax.set_title('Pressure and Temperature Profile')
        ax.set_xlabel('Axial Distance (m)')
        ax.grid(True)
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='best')

        canvas.draw()
        return
    
    def update_Mplt(self,x_data,m_data):
        #TODO
        return  
    
    def update_output(self,text):
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0,tk.END)
        self.output_text.insert(tk.END,text)
        self.output_text.config(state='disabled')
    
    def Combustion(self,mdot_in,mdot_fuel,rho_air):
        # mdot_in = mdot_in*10**-3
        # mdot_fuel = mdot_fuel*(1/1000)*(1/60)
        # mdot_total = rho_air*mdot_in
        # mdot_air = mdot_total-mdot_fuel
        # f_act = mdot_fuel/mdot_air
        
        # MW_carbon = 12.011
        # MW_oxygen = 15.999
        # MW_nitrogen = 14.007
        # MW_hydrogen = 1.0078
        # #Using Jet A as a fuel. Assume it's composition is C12H24
        # MW_fuel = 12*MW_carbon+24*MW_hydrogen
        # #Assuming air is O2+3.74N2
        # MW_oxidizer = 2*MW_oxygen+3.74*2*MW_nitrogen
        # f_stoich = MW_fuel/(18*MW_oxidizer)
        
        # phi = f_act/f_stoich
        
        # #Need to figure out how to get STANJAN working in here. Might have some issues if I 
        # #figure out how to get JetA into StanJan
        # P3 = 2.179 #atm. NEED TO UPDATE WITH ENGINE DATA
        
        self.update_output(self.output_text.get(1.0,tk.END)+'\nCombustion Placeholder Finished\n')
        return
    
    def StartButton(self):
        """
        Executes the main calculation workflow when the Start button is pressed.
        Uses default/hardcoded values for now since GUI input elements are not implemented.
        """
        gamma = float(self.input_vars['gamma'].get())
        R = float(self.input_vars['R'].get())
        rho_air = float(self.input_vars['rho_air'].get())
        T2 = float(self.input_vars['EGT'].get())
        u2 = float(self.input_vars['u_exit'].get())
        BVP = float(self.input_vars['BVP'].get())
        Tc = float(self.input_vars['flame_height'].get())
        turbblade = float(self.input_vars['ITP'].get())
        diff_length = float(self.input_vars['length_diff'].get())
        straight = float(self.input_vars['straight'].get())
        theta = float(self.input_vars['half_angle'].get())
        D = float(self.input_vars['turb_diameter'].get())
        n_points = int(self.input_vars['plot_points'].get())
        d_nozzle = float(self.input_vars['noz_diameter'].get())
        d_turbine = float(self.input_vars['turb_diameter'].get())
        mdot_in = float(self.input_vars['mdot_in'].get())
        mdot_fuel_engine = float(self.input_vars['mdot_fuel'].get())
        
        # Execute main calculation
        self.mainfunc(gamma, R, rho_air, T2, u2, BVP, Tc, turbblade, 
                 diff_length, straight, theta, D, n_points, d_nozzle, 
                 d_turbine, mdot_in, mdot_fuel_engine)
        
        # Execute combustion analysis
        self.Combustion(mdot_in, mdot_fuel_engine, rho_air)
        
        # try:
        #     # Execute main calculation
        #     self.mainfunc(gamma, R, rho_air, T2, u2, BVP, Tc, turbblade, 
        #                  diff_length, straight, theta, D, n_points, d_nozzle, 
        #                  d_turbine, mdot_in, mdot_fuel_engine)
            
        #     # Execute combustion analysis
        #     self.Combustion(mdot_in, mdot_fuel_engine, rho_air)
            
            
        # except Exception as e:
        #     print(f"Error during calculation: {e}")
        
        return
    
    def ResetButton(self):
         # Reset all input fields to their default values
        self.input_vars['gamma'].set(1.4)
        self.input_vars['R'].set(287)
        self.input_vars['rho_air'].set(1.225)
        self.input_vars['EGT'].set(800)
        self.input_vars['u_exit'].set(1200)
        self.input_vars['BVP'].set(1)
        self.input_vars['ITP'].set(0.9515)
        self.input_vars['mdot_in'].set(1)
        self.input_vars['length_turbine'].set(1)
        self.input_vars['length_diff'].set(1)
        self.input_vars['straight'].set(1)
        self.input_vars['half_angle'].set(15)
        self.input_vars['flame_height'].set(1)
        self.input_vars['noz_diameter'].set(1)
        self.input_vars['turb_diameter'].set(1)
        self.input_vars['mdot_fuel'].set(1)
        self.input_vars['plot_points'].set(100)
        self.input_vars['M_diff'].set(1)

        # Clear plots
        for plot_name in self.plots:
            ax = self.plots[plot_name]['ax']
            canvas = self.plots[plot_name]['canvas']
            ax.clear()
            ax.set_title(self.plots[plot_name]['figure'].axes[0].get_title()) # Re-set title
            ax.set_xlabel('Axial Distance (m)')
            ax.set_ylabel('Parameter Value')
            ax.grid(True)
            canvas.draw()

        # Clear output
        self.update_output("Inputs reset. Output cleared.\n")
        return
    
    def StopButton(self):
        #TODO Implement later
        self.update_output("Stop button pressed. (No active calculation to stop)\n")
        print("Stop button pressed.")
        return

    def run(self):
        self.master.mainloop()
        return
