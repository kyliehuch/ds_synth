import sys


def parse_synth_dict(arg_str):
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

univ_out = """import sys

f_name = sys.argv[1]
with open(f_name) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

data_structs = []\n"""


f_name = sys.argv[1]
output_ex = sys.argv[2]

# format raw data file into 2D list (list of row word lists)
with open(f_name) as f:
    data = f.readlines()
    for i, line in enumerate(data):
        data[i] = [x.strip() for x in line.split()]

# Identify target data structure(s) --> ID nesting structure as well (?)
''' Formating Options:
Polo[37] = 'Ryan, Andie'        ==> dictionary
Polo = ['Ryan, Andie, 37']      ==> list
Polo = {'Ryan, Andie, 37'}      ==> set

* Initially not allowing nested data structures
* Code gerated to group target data structures into a dictionary named 'data_structs' with data structures' names as keys and data structure objects as values
'''

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


# Select subset of DSL
print(f'Selecting DSL subset for type {target_ds}...')


# Select pre-defined application logic
print('Running Trinity to generate formating code...')

synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"


# Dictionary data structure example (from proposal):
print('Formating generated generated code for application...')

synth_output = synth_output.replace('@param0', 'line')

if target_ds == 'dict':
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
