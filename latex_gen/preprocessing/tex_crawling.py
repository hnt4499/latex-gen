DESCRIPTION = """This script extracts LaTeX/TeX formulas from a regular
text file.
"""

import os
import sys
import argparse
import re


REGEX_PATTERN = r"\\(?:begin\{equation\*?\})\s?(?:\\(?:begin|label)\{(?:.*?)\}\s?)*\s*(.*?)\s*\\end\{(?:equation\*?|split)\}"
# The below regex pattern is used to find small, in-line formulas
# that do not start with \begin{equation}
REGEX_PATTERN_2 = r"\$+\s*(.*?)\s*\$+"

def main(args):
    # Read arguments
    text_input = args.text_input
    text_output = args.text_output
    min_len = args.min_len
    max_len = args.max_len
    # Read input data
    with open(text_input, "r", encoding=args.encoding) as file:
        data = file.read().replace("\n", " ") # replace newline char with space.
    # Use regular expression to extract data
    formulas = re.findall(REGEX_PATTERN, data)
    small_formulas = re.findall(REGEX_PATTERN_2, data)
    # Write output data
    with open(text_output, "w") as out:
        for formula in formulas:
            if min_len <= len(formula) <= max_len:
                out.write(formula + "\n")
        for formula in small_formulas:
            if min_len <= len(formula) <= max_len:
                out.write(formula + "\n")


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
    parser.add_argument('--min_len', type=int, default=3,
        help='Minimum length of sequences to keep')
    parser.add_argument('--max_len', type=int, default=1000,
        help='Maximum length of sequences to keep')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
