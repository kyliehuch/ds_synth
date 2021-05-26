# test file for developing string parsing methods


def parse_delim(synth_str):
    while 'get_delimiter' in synth_str:
        si = synth_str.index('get_delimiter')
        ei = si + + len('get_delimiter(')
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
                if (open_par_ct == 0) & (delim_idx == 0):
                    delim_idx = i
        c_arg0 = end_str[:delim_idx].strip()
        c_arg1 = end_str[delim_idx+1:close_idx].strip()
        rest = end_str[close_idx+1:]
        end_str = c_arg0 + " + " + c_arg1 + rest
        synth_str = start_str + end_str
    return synth_str


synth_output = "dict(@param0[2], @param0[3], concat(concat(@param0[1], get_delimiter(,)), @param0[0]))"

# Translate Rosette Trinity output to python
synth_output = synth_output.replace('@param0', 'line')

print(synth_output)

synth_output = parse_delim(synth_output)

print(synth_output)

synth_output = parse_concat(synth_output)

print(synth_output)
