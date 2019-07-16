DESCRIPTION = """A convenience script to combine multiple text files into
one single file.
"""

import sys
import argparse


def main(args):
    with open(args.output_path, "w") as out:
        for path in args.input_path:
            with open(path, "r", encoding=args.encoding) as inp:
                out.write(inp.read() + "\n")
                

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=DESCRIPTION)

    parser.add_argument('output_path', type=str,
        help='Path to the output text file.')
    parser.add_argument('-i', '--input_path', nargs="+",
        help='Path(s) to the input text file(s).')
    parser.add_argument('--encoding', type=str, default="utf-8",
        help='Encoding for input text file(s).')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
