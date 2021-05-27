#!/usr/bin/env python

import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator, RelaxedRandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider, ExampleConstraintPruningDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')

class SetInterpreter(PostOrderInterpreter):

    def eval_get_delimiter(self, node, args):
        return args[0]

    def eval_concat(self, node, args):
        return args[0] + args[1]

    # return name, struct tuples for container data types
    def eval_set(self, node, args):
        s_name = args[0]
        s_vals = set(args[1])
        return s_name, s_vals
