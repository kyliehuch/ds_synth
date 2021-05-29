def det_depth_loc(cat_str, input_ex):
    ''' Accepts target string and calcuates synthesizer depth and loc '''
    pos_delim_strs = [",", " "]
    lit_count = len(input_ex)
    delim_count = 0
    for i in pos_delim_strs:
        delim_count += cat_str.count(i)
    loc = (lit_count + 2*delim_count - 1)
    depth = ((lit_count + delim_count + 1) // 2) + 1
    if delim_count > 0:
        depth += 1
    return depth, loc

in_ex = ['Andie', 'Ryan', '37']
o_ex = 'Ryan,Andie,37'

depth, loc = det_depth_loc(o_ex, in_ex)
print(f"Input: {in_ex}\tOutput: '{o_ex}'")
print(f"depth = {depth}\tloc = {loc}")

# 'Ryan' + ',' + 'Andie'
# concat(concat(@param1, delim(,)), @param0)
# depth = 4, loc = 3

# 'Ryan,Andie,37' --> 'Ryan' + ',' + 'Andie' + ',' '37'
# concat( concat( concat('Ryan', ','), concat('Andie', ',') ), '37')
