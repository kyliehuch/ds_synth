dict_ex = "Polo['37'] = 'Ryan, Andie'"
list_ex = "Polo = ['Ryan, Andie, 37']"
set_ex = "Polo = {'Ryan, Andie, 37'}"

input_ex = ['Polo', '37', 'Andie', 'Ryan']
print(f"Input example: {input_ex}")

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

def translate_indicies(synth_str, input_ex, input_sub):
    sub_idx = []
    for v in input_sub:
        sub_idx.append(input_ex.index(v))
    for i, t in enumerate(sub_idx):
        synth_str = synth_str.replace('@param'+str(i), 'line['+str(t)+']')
    return synth_str

n_dict, k_dict, v_dict = parse_out_dict(dict_ex)
n_list, v_list = parse_out_list(list_ex)
n_set, v_set = parse_out_set(set_ex)

if n_dict not in input_ex:
    input_sub = []
    for i in input_ex:
        if i in n_dict:
            input_sub.append(i)
    print(f"Input subset for name field: {input_sub}")
else:
    print("Name is literal field of input")
if k_dict not in input_ex:
    input_sub = []
    for i in input_ex:
        if i in k_dict:
            input_sub.append(i)
    print(f"Input subset for key field: {input_sub}")
else:
    print("Key is literal field of input")
if v_dict not in input_ex:
    input_sub = []
    for i in input_ex:
        if i in v_dict:
            input_sub.append(i)
    val = "concat(concat(@param1, delim(,)), @param0)"
    print(f"Input subset for value field: {input_sub}")
    print(f"Synthisized code: {val}")
    val = translate_indicies(val, input_ex, input_sub)
    print(f"Formated synthisized code: {val}")
else:
    print("Value is literal field of input")
