# Usage: python wrangler.py raw_data_file.txt '1st row output example'
import sys

# Output Example Formating Options:
# Polo[37] = 'Ryan, Andie'        ==> dictionary
# Polo = ['Ryan, Andie, 37']      ==> list
# Polo = {'Ryan, Andie, 37'}      ==> set

# * Initially not allowing nested data structures
# * Code gerated to group target data structures into a dictionary named 'data_structs' with data structures' names as keys and data structure objects as values and written to output file 'format.py'


# –––––––––––––––––– Parse Input & Output Examples –––––––––––––––––
f_name = sys.argv[1]
output_ex = sys.argv[2]

# format raw data file into 2D list (list of row word lists)
with open(f_name) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

input_ex = data[0]


# –––––––––––––––––– Identify Target Data Structure(s) –––––––––––––––––
# NEXT STEPS: ID nested data structures as well
target_ds = ''
for i,c in enumerate(output_ex):
    if c == '[':
        target_ds = 'dict'
        break
    elif c == '=':
        for ch in output_ex[i:]:
            if ch == '[':
                target_ds = 'list'
                break
            elif ch == '{':
                target_ds = 'set'
                break
        break

if target_ds == '':
    print("Invalid output example specified.")
    exit(1)
else:
    print(f"Target data structure detected: {target_ds}")


# –––––––––––––––––– Trinity Output Parse Functions –––––––––––––––––
def parse_synth_dict(arg_str):
    ''' Translates output of Trinity to python for dict data structs.
    Acceps arguments to dict() func, returns dict name, key, and val args '''
    delim_idxs = [0,0]
    open_par_ct = 0
    for i,c in enumerate(arg_str):
        if c == '(':
            open_par_ct += 1
        elif c == ')':
            open_par_ct -= 1
        elif c == ',':
            if open_par_ct == 0:
                if delim_idxs[0] == 0:
                    delim_idxs[0] = i
                else:
                    delim_idxs[1] = i
                    break
    n = arg_str[:delim_idxs[0]].strip()
    k = arg_str[delim_idxs[0]+1:delim_idxs[1]].strip()
    v = arg_str[delim_idxs[1]+1:].strip()
    return n, k, v

def parse_synth_l_s(arg_str):
    ''' Translates output of Trinity to python for dict data structs. Acceps arguments to lsit() or set() funcs, returns struct name, and val args '''
    pass

def parse_concat(arg_str):
    ''' translates output of Trinity to python for dict data structs acceps arguments to lsit() or set() funcs, returns struct name, and val args '''
    pass


# –––––––––––––––––––––––– DSL Definitions –––––––––––––––––––––––––
print(f'Selecting DSL subset for type {target_ds}...')




# –––––––––––––––––– Program Synthesis with Trinity –––––––––––––––––
print('Running Trinity to generate formating code...')

# Hardcoded output for dev & debugging purposes
synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"


# ––––––––––––––––––– Application Logic Synthesis ––––––––––––––––––––
print('Generating data structure-specific application code...')

# Translate Rosette Trinity output to python
synth_output = synth_output.replace('@param0', 'line')

# resolve concat commands
# TODO

# Code to import raw data from .txt file and format it into a 2D list
# Appended to synthesized code for all data structures
synth_prog = """import sys

f_name = sys.argv[1]
with open(f_name) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

data_structs = []\n"""

# Select data structure-specific adaptation logic
if target_ds == 'dict':
    # synthesizer output format: dict(name, key, value)
    dict_args = synth_output[5:-1]
    name, key, val = parse_synth_dict(dict_args)
    try_str = f"{name}[{key}] = {val}"
    exc_str = name + " = {" + key + ":" + val + "}"

    dict_out = f"""for line in data:
        try:
            {try_str}
        except Exception:
            {exc_str}
            data_structs.append({name})"""

    out = univ_out + dict_out

    print(f'Generated formatting code:\n{out}')
elif target_ds == 'list':
    # synthesizer output format: list(name, entry)
    list_args = synth_output[5:-1]
    name, entry = parse_synth_l_s(list_args)

elif target_ds == 'set':
    # synthesizer output format: set(name, entry)
    set_args = synth_output[4:-1]
    name, entry = parse_synth_l_s(set_args)

else:
    print(f"Unsuported target data structure {target_ds}")
    exit(1)
