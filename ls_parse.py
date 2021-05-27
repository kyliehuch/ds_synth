# test file for parsing list and set arguments
from str_parse import parse_delim, parse_concat

# @param0 = ['Andie', 'Ryan', 'Polo', '37']
# List Output = Polo = ['Ryan, Andie, 37']
synth_output_list = "list(@param0[2], concat(concat(concat(@param0[1], get_delimiter(,)), concat(@param0[0], get_delimiter(,))), @param0[3]))"

# Set Output = Polo = {'Ryan, Andie, 37'}
synth_output_set = "set(@param0[2], concat(concat(concat(@param0[1], get_delimiter(,)), concat(@param0[0], get_delimiter(,))), @param0[3]))"


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


print(f"List synth output raw: {synth_output_list}")
list_args = synth_output_list[5:-1]
l_name, l_val = parse_synth_l_s(list_args)

print(f"Raw list name field: {l_name}")
print(f"Raw list val field: {l_val}")

l_name = parse_concat(parse_delim(l_name))
l_val = parse_concat(parse_delim(l_val))

print(f"Parsed list name field: {l_name}")
print(f"Parsed list val field: {l_val}\n")


print(f"Set synth output raw: {synth_output_set}")
set_args = synth_output_set[4:-1]
s_name, s_val = parse_synth_l_s(set_args)

print(f"Raw list name field: {s_name}")
print(f"Raw list val field: {s_val}")

s_name = parse_concat(parse_delim(s_name))
s_val = parse_concat(parse_delim(s_val))

print(f"Parsed list name field: {s_name}")
print(f"Parsed list val field: {s_val}\n")
