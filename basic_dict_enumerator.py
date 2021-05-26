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

    # return name, struct tuples for container data types
    def eval_dict(self, node, args):
        d_name = args[0]
        d_key = args[1]
        d_val = args[2]
        return d_name, {d_key:d_val}

    def eval_list(self, node, args):
        l_name = args[0]
        l_vals = args[1]
        return l_name, l_vals

    def eval_set(self, node, args):
        s_name = args[0]
        s_vals = set(args[1])
        return s_name, s_vals
