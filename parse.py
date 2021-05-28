dict_ex = "Polo['37'] = 'Ryan, Andie'"
list_ex = "Polo = ['Ryan, Andie, 37']"
set_ex = "Polo = {'Ryan, Andie, 37'}"

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

n_dict, k_dict, v_dict = parse_out_dict(dict_ex)
n_list, v_list = parse_out_list(list_ex)
n_set, v_set = parse_out_set(set_ex)

print(f"Dict output example: {dict_ex}")
print(f"name = '{n_dict}'\tkey = '{k_dict}'\tval = '{v_dict}'\n")

print(f"List output example: {list_ex}")
print(f"name = '{n_list}'\tval = '{v_list}'\n")

print(f"Set output example: {set_ex}")
print(f"name = '{n_set}'\tval = '{v_set}'\n")
