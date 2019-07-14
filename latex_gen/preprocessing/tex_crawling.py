DESCRIPTION = """This script extracts LaTeX/TeX formulas from a regular
text file.
"""

import os
import sys
import argparse
import re


REGEX_PATTERN = r"\\(?:begin\{equation\*?\})\s?(?:\\(?:begin|label)\{(?:.*?)\}\s?)*(.*?)\\end\{(?:equation\*?|split)\}"


def main(args):
    # Read arguments
    text_input = args.text_input
    text_output = args.text_output
    # Read input data
    with open(text_input, "r", encoding=args.encoding) as file:
        data = file.read().replace("\n", " ") # replace newline char with space.
    # Use regular expression to extract data
    formulas = re.findall(REGEX_PATTERN, data)
    # Write output data
    with open(text_output, "w") as out:
        for formula in formulas:
            out.write(formula)
            

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=DESCRIPTION)

    parser.add_argument('text_input', type=str,
        help='Path to the input text file.')
    parser.add_argument('text_output', type=str,
        help='Path to the output text file.')

    parser.add_argument('--encoding', type=str, default="utf-8",
        help='Decoder(s) to try for input data.')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
