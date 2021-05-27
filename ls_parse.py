# test file for parsing list and set arguments

# @param0 = ['Andie', 'Ryan', 'Polo', '37']
# List Output = Polo = ['Ryan, Andie, 37']
synth_output_list = "list(@param0[2], concat(concat(concat(@param0[1], get_delimiter(,)), concat(@param0[0], get_delimiter(,))), @param0[3]))"

# Set Output = Polo = {'Ryan, Andie, 37'}
synth_output_set = "set(@param0[2], concat(concat(concat(@param0[1], get_delimiter(,)), concat(@param0[0], get_delimiter(,))), @param0[3]))"
