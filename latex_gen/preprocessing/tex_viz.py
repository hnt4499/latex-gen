DESCRIPTION = """ Display LaTeX formulas, making it easier to spot outliers,
errors and patterns.
"""

import os
import sys
import argparse
import math

import cv2
from tqdm import tqdm

from latex_gen.utils.tex_util import tex_to_img


def main(args):
    # Read arguments
    text_input = args.text_input
    num_display = args.num_display
    dpi = args.dpi
    tmp_dir = args.tmp_dir
    # Read data
    with open(text_input, "r", encoding=args.encoding) as text:
        data = text.readlines()
    # Generate and display intermediate image.
    num_batches = math.ceil(len(data) / num_display)
    batch_index = 0
    processed = []
    while True:
        img_path = os.path.join(tmp_dir, "viz_{}.png".format(batch_index))
        # If not processed
        if batch_index not in processed:
            start = batch_index * num_display
            end = min((batch_index + 1) * num_display, len(data))
            tex_to_img(data[start:end], img_path, dpi, tmp_dir)
            processed.append(batch_index)
        # Display image
        img = cv2.imread(img_path)
        cv2.imshow("LaTeX formulas", img)
        # Handle key inputs
        key = cv2.waitKey(0)
        if key == ord("d"):
            batch_index = (batch_index + 1) % num_batches
        elif key == ord("a"):
            batch_index = (batch_index - 1) % num_batches
        elif key == ord("q"):
            print(">>> Current index: {}".format(batch_index))
            break


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
