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
        return args[0], set(args[1])


def main():
	logger.info('Parsing Spec...')
	spec = S.parse_file('basic_set.tyrell')
	logger.info('Parsing succeeded')

	logger.info('Building synthesizer...')
	synthesizer = Synthesizer(
        # set(@param0[2], concat(concat(concat(@param0[1], get_delimiter(,)), concat(@param0[0], get_delimiter(,))), @param0[3])) --> depth=6, loc=7
		enumerator=SmtEnumerator(spec, depth=6, loc=7),
		decider=ExampleConstraintDecider(
			spec=spec,
			interpreter=SetInterpreter(),
			examples=[
				Example(input=[ ['Andie', 'Ryan', 'Polo', '37'] ], output=('Polo', {'Ryan,Andie,37'})),
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
