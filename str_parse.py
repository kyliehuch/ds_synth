# test file for developing string parsing methods

# @param0 = ['Andie', 'Ryan', 'Polo', '37']
# Output = Polo[37] = 'Ryan, Andie'
synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"

in_ex = ['Andie', 'Ryan', 'Polo', '37']
in_sub = ['Andie', 'Ryan']
val = "concat(@param1, concat(delim(,), @param0))"

def translate_indicies(synth_str, input_ex, input_sub):
    sub_idx = []
    for v in input_sub:
        sub_idx.append(input_ex.index(v))
    for i, t in enumerate(sub_idx):
        synth_str = synth_str.replace('@param'+str(i), 'line['+str(t)+']')
    return synth_str

def parse_delim(synth_str):
    ''' Translates output of Trinity to python for string get_delim() method. Acceps string, splices get_delim() and re-formats string accordingly '''
    while 'delim' in synth_str:
        si = synth_str.index('delim')
        ei = si + + len('delim(')
        synth_str = synth_str[0:si] + "'" +  synth_str[ei] + "'" + synth_str[ei+2:]
    return synth_str

def parse_concat(synth_str):
    ''' Translates output of Trinity to python for string concat() method. Acceps arguments to lsit() or set() funcs, returns struct name, and val args '''
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
                if not ((end_str[i-1] == "'") & (end_str[i+1] == "'")):
                    if (open_par_ct == 0) & (delim_idx == 0):
                        delim_idx = i
        c_arg0 = end_str[:delim_idx].strip()
        c_arg1 = end_str[delim_idx+1:close_idx].strip()
        rest = end_str[close_idx+1:]
        end_str = c_arg0 + " + " + c_arg1 + rest
        synth_str = start_str + end_str
    return synth_str


print(f"Raw output: {val}")
val = translate_indicies(val, in_ex, in_sub)
print(f"Line output: {val}")
val = parse_delim(val)
print(f"Delim parsed output: {val}")
val = parse_concat(val)
print(f"Parsed output: {val}")
