DESCRIPTION = """This script extracts LaTeX/TeX formulas from a regular
text file.
"""

import os
import sys
import argparse


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=DESCRIPTION)

    parser.add_argument('text_input', type=str,
        help='Path to the input text file.')

    parser.add_argument('--num_display', type=int, default=10,
        help='Number of formulas to display at a time. '
             'Must be not too large (<=15).')
    parser.add_argument('--dpi', type=int, default=120,
        help='DPI (resolution) of displaying images.')
    parser.add_argument('--tmp_dir', type=str, default="/tmp",
        help='Directory to store all temporary files.')
    parser.add_argument('--encoding', type=str, default="utf-8",
        help='Decoder(s) to try for input data.')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
