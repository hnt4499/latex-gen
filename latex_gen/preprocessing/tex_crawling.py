DESCRIPTION = """This script extracts LaTeX/TeX formulas from all regular
text files contained within the same folder.
"""

import os
import sys
import argparse
import re

from tqdm import tqdm

# REGEX_PATTERN = r"\\(?:begin\{equation\*?\})\s?(?:\\(?:begin|label)\{(?:.*?)\}(?:.*?))*\s*(.*?)\s*(?:\\label\s?\{(?:.*?)\})?\s*\\end\{(?:equation\*?|split)\}"
REGEX_PATTERN = r"[^\{^(?:def)]\\(?:begin\{equation\*?\}|bq)\s*(?:\\(?:begin)\{[^(?:array)]*\}(?:.*?))*\s*(.*?)\s*\\(?:end\s?\{(?:equation\*?|split)\}|eq )"

# The below regex pattern is used to find small, in-line formulas
# that do not start with \begin{equation}
REGEX_PATTERN_2 = r"(?:\$\s*(.*?)\s*\$|\$\$\s*(.*?)\s*\$\$)"
# Note that r"\$+\s*(.*?)\s*\$+" is not used because the pattern "$$" can appear
# inside the equation starting and ending with "$", which may introduces errors.
# For example: ${\cA}(A;x^++1,x^-+1)$$={\cA}(A^m;x^+,x^-)$

def main(args):
    # Read arguments
    text_input = args.text_input
    text_output = args.text_output
    min_len = args.min_len
    max_len = args.max_len
    # Read input data
    with open(text_output, "w") as out:
        for file_name in tqdm(os.listdir(text_input)):
            file_path = os.path.join(text_input, file_name)
            # Skip directories
            if os.path.isdir(file_path):
                continue
            with open(file_path, "r", encoding=args.encoding) as file:
                data = file.read().replace("\n", " ") # replace newline char with space
            # Use regular expression to extract data
            formulas = re.findall(REGEX_PATTERN, data)
            small_formulas = re.findall(REGEX_PATTERN_2, data)
            # Since LaTeX formulas span multiple lines and part of the formulas
            # can be commented out by using `%`, and since we turn all formulas
            # to just one line, we need to get rid of `%`
            formulas = list(map(lambda x: x.replace("%", ""), formulas))
            # The second regex return two matches at a time, but only one
            # of them are usable, it needs to be concatenated
            small_formulas = list(map(lambda x: "".join(x), small_formulas))
            # Write output data
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
        help='Directory to the input text files.')
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
