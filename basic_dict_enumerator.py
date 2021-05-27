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

    # return name, struct tuples for container data types
    def eval_dict(self, node, args):
        d_name = args[0]
        d_key = args[1]
        d_val = args[2]
        return (d_name, {d_key:d_val})


def main():
	logger.info('Parsing Spec...')
	spec = S.parse_file('basic_dict.tyrell')
	logger.info('Parsing succeeded')

	logger.info('Building synthesizer...')
	synthesizer = Synthesizer(
		enumerator=SmtEnumerator(spec, depth=3, loc=5),
		decider=ExampleConstraintDecider(
			spec=spec,
			interpreter=DictInterpreter(),
			examples=[
				Example(input=[ ['Andie', 'Ryan', 'Polo', '37'] ], output=('Polo', {'37':'Ryan,Andie'})),
			],
			# equal_output=eq_deepcoder
		)
	)
	logger.info('Synthesizing programs...')

	prog = synthesizer.synthesize()
	if prog is not None:
		logger.info('Solution found: {}'.format(prog))
	else:
		logger.info('Solution not found!')

if __name__ == '__main__':
	logger.setLevel('DEBUG')
	main()
