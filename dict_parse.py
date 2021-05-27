# test file for parsing dict arguments
from str_parse import parse_delim, parse_concat

# @param0 = ['Andie', 'Ryan', 'Polo', '37']
# Output = Polo[37] = 'Ryan, Andie'
synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"

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

dict_args = synth_output[5:-1]
name, key, val = parse_synth_dict(dict_args)

print(f"Raw Trinity output: {synth_output}\n")
print(f"Raw dict name field: {name}")
print(f"Raw dict key field: {key}")
print(f"Raw dict val field: {val}")

name = parse_concat(parse_delim(name))
key = parse_concat(parse_delim(key))
val = parse_concat(parse_delim(val))

print(f"Parsed dict name field: {name}")
print(f"Parsed dict key field: {key}")
print(f"Parsed dict val field: {val}")
