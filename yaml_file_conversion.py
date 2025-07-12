# import os
# import cantera

# print(os.path.dirname(cantera.__file__))

import os
import sys
from cantera.ck2yaml import main as ck2yaml_main

def convert(input_file, thermo_file, output_file, permissive=True):
    print(f"converting {input_file}, {thermo_file} to {output_file}")
    
    args=['--input=' + input_file, '--thermo=' + thermo_file, '--output=' + output_file]
    if permissive:
        args.append('--permissive')
        
    original_argv = sys.argv
    sys.argv = ['ck2yaml_script'] + args
    try:
        ck2yaml_main()
    except Exception as e:
        print(f"Error during conversion: {e}")
    finally:
        sys.argv = original_argv
        

inp_file = 'jet_a_chem.inp'
dat_file = 'jet_a_thermo.dat'
out_file = 'Jet_A.yaml'

if __name__ == "__main__":
    
    if not os.path.exists(inp_file):
        print(f"Input file {inp_file} does not exist.")
        sys.exit(1)
    if not os.path.exists(dat_file):
        print(f"Thermo file {dat_file} does not exist.")
        sys.exit(1)
    try:
        convert(inp_file, dat_file, out_file, permissive=True)
        print(f"Conversion completed. Output file: {out_file}")
    except Exception as e:
        print(f"Conversion failed: {e}")