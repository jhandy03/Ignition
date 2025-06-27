
class UnitConversionToolbox:
    def temp_conversion(self, value, input_units, output_units):
        """
        Description: 
            Converts between F, C, and K
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        unit_map = {'Celsius':'C', 'Kelvin': 'K', 'Fahrenheit': 'F'}
        input_units = unit_map.get(input_units, input_units)
        output_units = unit_map.get(output_units, output_units)
        if input_units == 'C':
            K = value+273.15
        elif input_units == 'K':
            K = value
        elif input_units == 'F':
            K = (value-32)*5/9+273.15
        else:
            raise ValueError(f"Internal Error: Unrecognized input unit '{input_units}'")

        if output_units == 'C':
            return K-273.15
        elif output_units == 'F':
            return (K-273.15)*9/5+32
        elif output_units == 'K':
            return K
        else:
            raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def pressure_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between bar, atm, Pa
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if input_units.lower() == 'bar':
            Pa = value*100000
        elif input_units.lower() == 'atm':
            Pa = value *101325
        elif input_units == 'Pa':
            Pa = value
        else:
            raise ValueError(f"Internal Error: Unrecognized input unit '{input_units}'") 
            #TDOD: maybe throw in psi?
        if output_units.lower() == 'bar':    
             return Pa/100000
        elif output_units.lower() == 'atm':
            return Pa/101325
        elif output_units == 'Pa':
            return Pa
        else:
            raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def velocity_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between m/s, km/hr, and mph
        Args: 
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if input_units == 'km/hr':
            mps = value *(3600/1000)
        elif input_units == 'mph':
            mps = value/2.23694
        elif input_units == 'm/s':
            mps = value
        else:
            return None
            #raise ValueError(f"Internal Error: Unrecognized input unit'{input_units}'")
            
        if output_units == 'km/hr':
            return mps*(1000/3600)
        elif output_units == 'mph':
            return mps*2.23694
        elif output_units == 'm/s':
            return mps
        else:
            return None
            #raise ValueError(f"Internal Error: Unrecognized output unit'{output_units}'")
        
    def volume_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between L, m^3, and cm^3
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        #TODO: Check the unit conversions here. Not entirely sure that this is done correctly
        if input_units == 'm^3':
            L = value*1000
        elif input_units == 'cm^3':
            L = value/1000
        elif input_units == 'L':
            L = value
        else:
            return None
        
        if output_units == 'm^3':
            return L/1000
        elif output_units == 'cm^3':
            return L*1000
        elif output_units == 'L':
            return L
        else:
            return None
        
    def massflow_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between kg/s, kg/min, g/min
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        # Convert to kg/s as base unit
        if input_units == 'kg/s':
            kg_per_s = value
        elif input_units == 'kg/min':
            kg_per_s = value / 60
        elif input_units == 'g/min':
            kg_per_s = value / 1000 / 60
        else:
            return None
            #TODO: add in lb/s or something like that?
        # Convert from kg/s to desired output units
        if output_units == 'kg/s':
            return kg_per_s
        elif output_units == 'kg/min':
            return kg_per_s * 60
        elif output_units == 'g/min':
            return kg_per_s * 1000 * 60
        else:
            return None

    def volflow_conversion(self, value, input_units, output_units):
        """
        Description:
            Converts between m^3/s, L/s, m^3/min, L/min
        Args:
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        # Convert to m^3/s as base unit
        if input_units == 'm^3/s':
            m3_per_s = value
        elif input_units == 'L/s':
            m3_per_s = value / 1000
        elif input_units == 'm^3/min':
            m3_per_s = value / 60
        elif input_units == 'L/min':
            m3_per_s = value / 1000 / 60
        else:
            return None
            
        # Convert from m^3/s to desired output units
        if output_units == 'm^3/s':
            return m3_per_s
        elif output_units == 'L/s':
            return m3_per_s * 1000
        elif output_units == 'm^3/min':
            return m3_per_s * 60
        elif output_units == 'L/min':
            return m3_per_s * 1000 * 60
        else:
            return None
    def mass2vol_conversion(self,rho, value, input_units, output_units):
        """
        Description:
            Converts between kg/s, m^3/s
        Args:
            rho (float): density in kg/m^3
            value (float or int): given value
            input_units (str): units of the value given
            output_units (str): units of the value wanted
        Returns:
            float: converted value
            None: invalid computation
        """
        if rho <= 0:
            return None
            
        if input_units == 'kg/s' and output_units == 'm^3/s':
            return value / rho
        elif input_units == 'm^3/s' and output_units == 'kg/s':
            return value * rho
        else:
            return None
    