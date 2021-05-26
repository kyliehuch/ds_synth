#!/usr/bin/env python

import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator, RelaxedRandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider, ExampleConstraintPruningDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')

class DictInterpreter(PostOrderInterpreter):

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
