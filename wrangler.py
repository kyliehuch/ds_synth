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
    ''' Translates output of Trinity to python for list and set data structs. Acceps arguments to lsit() or set() funcs, returns struct name, and val args '''

    # TODO: implement

    pass

def parse_delim(synth_str):
    ''' Translates output of Trinity to python for string get_delim() method. Acceps string, splices get_delim() and re-formats string accordingly '''
    while 'get_delimiter' in synth_str:
        si = synth_str.index('get_delimiter')
        ei = si + + len('get_delimiter(')
        synth_str = synth_str[0:si] + "'" +  synth_str[ei] + "'" + synth_str[ei+2:]
    return synth_str

def parse_concat(synth_str):
    ''' Translates output of Trinity to python for string concat() method. Acceps string, splices concat() and re-formats string accordingly '''
    while 'concat' in synth_str:
        si = synth_str.index('concat')
        ei = si + + len('concat(')
        start_str = synth_str[:si]
        end_str = synth_str[ei:]
        delim_idx = 0
        close_idx = 0
        open_par_ct = 0
        for i,c in enumerate(end_str):
            if c == '(':
                open_par_ct += 1
            elif c == ')':
                if open_par_ct != 0:
                    open_par_ct -= 1
                else:
                    close_idx = i
                    break
            elif c == ',':
                if (open_par_ct == 0) & (delim_idx == 0):
                    delim_idx = i
        c_arg0 = end_str[:delim_idx].strip()
        c_arg1 = end_str[delim_idx+1:close_idx].strip()
        rest = end_str[close_idx+1:]
        end_str = c_arg0 + " + " + c_arg1 + rest
        synth_str = start_str + end_str
    return synth_str


# –––––––––––––––––––––––– DSL Definitions –––––––––––––––––––––––––
print(f'Selecting DSL subset for type {target_ds}...')

# TODO: define enum_funcs for DSL methods (separate class for each ds)


# –––––––––––––––––– Program Synthesis with Trinity –––––––––––––––––
print('Running Trinity to generate formating code...')

# TODO: write main trinity synthesizer

# Hardcoded output for dev & debugging purposes
synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"


# ––––––––––––––––––– Application Logic Synthesis ––––––––––––––––––––
print('Generating data structure-specific application code...')

# Translate Rosette Trinity output to python
synth_output = synth_output.replace('@param0', 'line')

# resolve get_delim commands
synth_output = parse_delim(synth_output)

# resolve concat commands with parse_concat(concat_args)
synth_output = parse_concat(synth_output)

# Code to import raw data from .txt file and format it into a 2D list
# Appended to synthesized code for all data structures
synth_prog = f"""import sys

with open('{f_name}') as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

data_structs = {{}}\n"""

# Select data structure-specific adaptation logic
if target_ds == 'dict':
    # synthesizer output format: dict(name, key, value)
    dict_args = synth_output[5:-1]
    name, key, val = parse_synth_dict(dict_args)
    if_str = f"data_structs[{name}][{key}] = {val}"
    else_str = f"data_structs[{name}] = {{ {key}:{val} }}"

    # Partial program for application of logic to dictionaries
    dict_out = f"""
for line in data:
    if line[2] in data_structs.keys():
        {if_str}
    else:
        {else_str}

for i in data_structs.keys():
    print(i, "=", data_structs[i])\n"""

    # Append application logic to synthesized code
    synth_prog += dict_out

elif target_ds == 'list':
    # synthesizer output format: list(name, entry)
    list_args = synth_output[5:-1]
    name, entry = parse_synth_l_s(list_args)

    # TODO: write adaptation logic

elif target_ds == 'set':
    # synthesizer output format: set(name, entry)
    set_args = synth_output[4:-1]
    name, entry = parse_synth_l_s(set_args)

    # TODO: write adaptation logic

else:
    print(f"Unsuported target data structure {target_ds}")
    exit(1)


# ––––––––––––––––––– Output Python File Creation ––––––––––––––––––––

with open('format.py','w') as out_file:
    out_file.write(synth_prog)

print("Done!\nData formatting code written to format.py")
