#!/usr/bin/env python

import sys
import random
"""import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator
from tyrell.decider import Example, ExampleConstraintDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')
logger.setLevel('DEBUG')"""

# Usage: python wrangler.py raw_data_file.txt '1st row output example'

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

print(f"Input example: {input_ex}")
print(f'Output example: "{output_ex}"')



# –––––––––––––––––– Identify Target Data Structure(s) –––––––––––––––––
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


# –––––––––––––––––– Output Field Parse Functions –––––––––––––––––
def parse_out_dict(out_ex):
    bo = out_ex.index('[')
    bc = out_ex.index(']')
    e = out_ex.index('=')
    n = out_ex[:bo].strip().strip("'").strip('"')
    k = out_ex[bo+1:bc].strip().strip("'").strip('"')
    v = out_ex[e+1:].strip().strip("'").strip('"')
    return n, k, v

def parse_out_list(out_ex):
    e = out_ex.index('=')
    bo = out_ex.index('[')
    bc = out_ex.index(']')
    n = out_ex[:e].strip().strip("'").strip('"')
    v = out_ex[bo+1:bc].strip().strip("'").strip('"')
    return n, v

def parse_out_set(out_ex):
    e = out_ex.index('=')
    bo = out_ex.index('{')
    bc = out_ex.index('}')
    n = out_ex[:e].strip().strip("'").strip('"')
    v = out_ex[bo+1:bc].strip().strip("'").strip('"')
    return n, v


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
    delim_idx = 0
    open_par_ct = 0
    for i,c in enumerate(arg_str):
        if c == '(':
            open_par_ct += 1
        elif c == ')':
            open_par_ct -= 1
        elif c == ',':
            if open_par_ct == 0:
                delim_idx = i
                break
    n = arg_str[:delim_idx].strip()
    v = arg_str[delim_idx+1:].strip()
    return n, v

def parse_delim(synth_str, num_params):
    ''' Translates output of Trinity to python for string get_delim() method. Acceps string, splices get_delim() and re-formats string accordingly '''
    for i in range(num_params):
        synth_str = synth_str.replace('@param'+str(i), 'line['+str(i)+']')
    while 'delim' in synth_str:
        si = synth_str.index('delim')
        ei = si + + len('delim(')
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


# ––––––––––––––––– Synthesizer Helper Functions ––––––––––––––––
def parse_file_generator(input_ex):
    ''' Creates correctly formated .tyrell file for a given input example '''
    in_f = "Str, "*(len(input_ex)-1) + "Str"
    file_conts = f"""enum ConstStr {{
  ",", " "
}}
value Empty;
value Str;

program gen_str({in_f}) -> Str;
func empty: Empty -> Empty;

func delim: Str -> ConstStr;
func concat: Str -> Str, Str;
"""
    with open('string.tyrell','w') as out_file:
        out_file.write(file_conts)

def det_depth_loc(cat_str, input_ex):
    ''' Accepts target string and calcuates synthesizer depth and loc '''
    depth = None
    loc = None
    return depth, loc


# ––––––––––––––––– DSL Enumerator Class Definitions ––––––––––––––––
"""class StrInterpreter(PostOrderInterpreter):

    def eval_delim(self, node, args):
        return args[0]

    def eval_concat(self, node, args):
        return args[0] + args[1]
"""


# ––––––––––––––– Trinity Program Synthesis Functions  –––––––––––––––––
"""
def synth_str(in_ex, out_ex, search_depth, search_loc):
    ''' Trinity synth prog for strings '''
    logger.info('Parsing Spec...')
    spec = S.parse_file('string.tyrell')
    logger.info('Parsing succeeded')

    logger.info('Building synthesizer...')
    synthesizer = Synthesizer(
        enumerator=SmtEnumerator(spec, depth=search_depth, loc=search_loc),
        decider=ExampleConstraintDecider(
            spec=spec,
            interpreter=StrInterpreter(),
            examples=[
                Example(input=in_ex, output=out_ex),
            ],
        )
    )
    logger.info('Synthesizing programs...')

    prog = synthesizer.synthesize()
    if prog is not None:
        logger.info('Solution found: {}'.format(prog))
    else:
        logger.info('Solution not found!')
    return prog
"""


# ––––––––––––––––––– Application Logic Synthesis ––––––––––––––––––––
print('Generating data structure-specific application code...')

# Create .tyrell file for this example
parse_file_generator(input_ex)

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
    name, key, val = parse_out_dict(output_ex)
    if name not in input_ex:
        print("Synthesizing code to generate dictionary name field...")
        depth, loc = det_depth_loc(name, input_ex)
        name = synth_str(input_ex, name, depth, loc)
        name = parse_concat(parse_delim(name, len(input_ex)))
    else:
        name = 'line[' + str(input_ex.index(name)) + ']'
    if key not in input_ex:
        print("Synthesizing code to generate dictionary key field...")
        depth, loc = det_depth_loc(key, input_ex)
        key = synth_str(input_ex, key, depth, loc)
        key = parse_concat(parse_delim(key, len(input_ex)))
    else:
        key = 'line[' + str(input_ex.index(key)) + ']'
    if val not in input_ex:
        print("Synthesizing code to generate dictionary value field...")
        #depth, loc = det_depth_loc(val, input_ex)
        #val = synth_str(input_ex, val, depth, loc)
        val = "concat(concat(@param1, delim(,)), @param0)"
        val = parse_concat(parse_delim(val, len(input_ex)))
    else:
        val = 'line[' + str(input_ex.index(val)) + ']'

    if_str = f"data_structs[{name}][{key}] = {val}"
    else_str = f"data_structs[{name}] = {{ {key}:{val} }}"

    # Partial program for application of logic to dictionaries
    dict_out = f"""
for line in data:
    if {name} in data_structs.keys():
        {if_str}
    else:
        {else_str}

for i in data_structs.keys():
    print(i, "=", data_structs[i])\n"""

    # Append application logic to synthesized code
    synth_prog += dict_out

elif target_ds == 'list':
    name, val = parse_out_list(output_ex)
    if name not in input_ex:
        print("Synthesizing code to generate list name field...")
        depth, loc = det_depth_loc(name, input_ex)
        name = synth_str(input_ex, name, depth, loc)
        name = parse_concat(parse_delim(name, len(input_ex)))
    else:
        name = 'line[' + str(input_ex.index(name)) + ']'
    if val not in input_ex:
        print("Synthesizing code to generate list value field...")
        depth, loc = det_depth_loc(val, input_ex)
        val = synth_str(input_ex, val, depth, loc)
        val = parse_concat(parse_delim(val, len(input_ex)))
    else:
        val = 'line[' + str(input_ex.index(val)) + ']'

    if_str = f"data_structs[{name}].append({val})"
    else_str = f"data_structs[{name}] = [{val}]"

    # Partial program for application of logic to lists
    list_out = f"""
for line in data:
    if {name} in data_structs.keys():
        {if_str}
    else:
        {else_str}

for i in data_structs.keys():
    print(i, "=", data_structs[i])\n"""

    # Append application logic to synthesized code
    synth_prog += list_out

elif target_ds == 'set':
    name, val = parse_out_set(output_ex)
    if name not in input_ex:
        print("Synthesizing code to generate set name field...")
        depth, loc = det_depth_loc(name, input_ex)
        name = synth_str(input_ex, name, depth, loc)
        name = parse_concat(parse_delim(name, len(input_ex)))
    else:
        name = 'line[' + str(input_ex.index(name)) + ']'
    if val not in input_ex:
        print("Synthesizing code to generate set value field...")
        depth, loc = det_depth_loc(val, input_ex)
        val = synth_str(input_ex, val, depth, loc)
        val = parse_concat(parse_delim(val, len(input_ex)))
    else:
        val = 'line[' + str(input_ex.index(val)) + ']'

    if_str = f"data_structs[{name}].add({val})"
    else_str = f"data_structs[{name}] = {{ {val} }}"

    # Partial program for application of logic to lists
    set_out = f"""
for line in data:
    if {name} in data_structs.keys():
        {if_str}
    else:
        {else_str}

for i in data_structs.keys():
    print(i, "=", data_structs[i])\n"""

    # Append application logic to synthesized code
    synth_prog += set_out

else:
    print(f"Unsuported target data structure {target_ds}")
    exit(1)


# ––––––––––––––––––– Output Python File Creation ––––––––––––––––––––

with open('format.py','w') as out_file:
    out_file.write(synth_prog)

print("Done!\nData formatting code written to format.py")
