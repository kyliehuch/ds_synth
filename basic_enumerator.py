#!/usr/bin/env python

import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator, RelaxedRandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider, ExampleConstraintPruningDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')

class StructInterpreter(PostOrderInterpreter):

    def eval_get_delimiter(self, node, args):
        return args[0]

    def eval_concat(self, node, args):
        return args[0] + args[1]

    # Include substring method?
    """def eval_substr(self, node, args):
        arg_str = args[0]
        arg_pos0 = args[1]
        arg_pos1 = args[2]
        return arg_str[arg_pos0:arg_pos1]"""

    # return name, struct tuples for container data types
    def eval_dict(self, node, args):
        d_name = args[0]
        d_key = args[1]
        d_val = args[2]
        return d_name, {d_key:d_val}

    # include update? --> is this needed?
    """def eval_dict_update(self, node, args):
        dict1 = args[0]
        dict2 = args[1]
        return dict1.update(dict2)"""

    def eval_list(self, node, args):
        l_name = args[0]
        l_vals = args[1]
        return l_name, l_vals

    def eval_set(self, node, args):
        s_name = args[0]
        s_vals = set(args[1])
        return s_name, s_vals
