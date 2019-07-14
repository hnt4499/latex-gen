'''
This script was highly inspired from this code:
    https://github.com/calebrob6/latexify/blob/master/latexify.py
However, I rewrite the script from the scratch for readability and
functionalities. I also keep the author's comments, because I find it useful.

Author: Hoang Nghia Tuyen
'''

import sys
import os
import argparse

from tqdm import tqdm

from latex_gen.utils.tex_util import tex_to_img


# Mimics the `which` unix command
# Taken from: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def main(args):
    # Test for dependencies.
    if which("latex") == None or which("dvipng") == None:
        print("Error! The commands `latex` and `dvipng` are required and "
              "could not be found in your environment.")
        return
    # Read arguments
    text_input = os.path.abspath(args.text_input)
    output_dir = os.path.abspath(args.output_dir)
    img_prefix = args.img_prefix
    dpi = args.dpi
    tmp_dir = os.path.abspath(args.tmp_dir)
    encoding = args.encoding
    # Read and assert mode.
    mode = args.mode
    assert mode in ["single", "combine"]

    generate_filepath = lambda x: os.path.join(output_dir,
                                               "{}_{}.png".format(img_prefix, x)
                                               )
    if mode == "single":
        slice = 1
    else:
        slice = 15

    i = 0
    start = 0

    with open(text_input, "r", encoding=encoding) as text:
        lines = text.readlines()
        for line in tqdm(lines[::slice]):
            end = start + slice
            end = len(lines) if end > len(lines) else end

            tex_to_img(text=lines[start:end],
                       output_path=generate_filepath(i),
                       dpi=dpi,
                       tmp_dir=tmp_dir)
            i += 1
            start += slice


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text_input', type=str,
        help='Path to the input text file.')
    parser.add_argument('output_dir', type=str,
        help='Path to the output png.')
    parser.add_argument('img_prefix', type=str,
        help='Image prefix. Images will be saved in `output_dir` '
             'and named `prefix`_`index`.png')

    parser.add_argument('--mode', type=str, default="single",
        help='If `mode == single`, each line will be saved to a separate '
             '`.png` file. If `mode == combine`, one `.png` file '
             'will contain a maxmimum of 15 formulas.')
    parser.add_argument('--dpi', type=int, default=120,
        help='DPI (resolution) of output png.')
    parser.add_argument('--tmp_dir', type=str, default="/tmp",
        help='Directory to which all temporary file(s) will be saved.')
    parser.add_argument('--encoding', type=str, default="utf-8",
        help='Decoder(s) to try for input data.')

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
