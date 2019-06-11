import pytest
import os
import logging
from glob import glob

from pipeline import sanitizers
from pipeline.sanitizers.definitions import DEFINITIONS

def test_sanitisation():
    cwd = os.getcwd()
    types_fixtures = glob(pathname=os.path.join(cwd, 'fixtures/*'))

    for type_dir in types_fixtures:
        csl_type = os.path.basename(type_dir)
        logging.info("Testing %s...", csl_type)

        for style_dir in glob(pathname=os.path.join(os.path.join(type_dir, '*'))):
            examples_file_path = os.path.join(style_dir, 'examples.txt')
            expected_file_path = os.path.join(style_dir, 'expected.txt')

            if os.path.exists(examples_file_path) and os.path.exists(expected_file_path):
                style = os.path.basename(style_dir).split('/')[-1]
                logging.info("Testing %s...", style)

                with open(examples_file_path, 'r') as example_file:
                    examples = example_file.read().split('\n')

                with open(expected_file_path, 'r') as expected_file:
                    expected = expected_file.read().split('\n')

                # Sanisation here
                sanitised_examples = [sanitizers.sanitise(example, DEFINITIONS[csl_type][style]) for example in examples]

                for result, expected in zip(sanitised_examples, expected):
                    assert result == expected, f"{os.path.basename(style_dir)} failed!"
            else:
                print(f"{examples_file_path} and {expected_file_path} not found.")
