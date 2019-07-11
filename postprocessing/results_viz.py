DESCRIPTION = '''
This script processes a `.json` file generated during training to visualize
the results.
'''
import matplotlib.pyplot as plt
import numpy as np
import json


def main(args):
    # Read some arguments
    fig_size = (args.fig_width, args.fig_height)
    train_xmin = args.train_xmin
    train_xmax = args.train_xmax
    val_xmin = args.val_xmin
    val_xmax = args.val_xmax


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=DESCRIPTION)

    parser.add_argument('input_json', type=str,
        help='Path to the input `.json` file.')
    parser.add_argument('output_file', type=str,
        help='Path to the output file (`.png` or `.jpg`).')

    parser.add_argument('--ignore_outliers', action="store_true",
        help='Whether to ignore outliers when processing `.json` file.')
    parser.add_argument('--threshold', type=float, default=3.5,
        help='Threshold to compare to `z-score`. Only used '
             'when `ignore_outliers` is set to True.')
    parser.add_argument('--single', action="store_true",
        help='When set to `True`, data will be plotted on the same figure.')

    parser.add_argument('--fig_width', type=int, default=20,
        help='Width of the figure.')
    parser.add_argument('--fig_height', type=int, default=20,
        help='Height of the figure.')
    parser.add_argument('--dpi', type=int, default=None,
        help='DPI of the figure.')

    parser.add_argument('--train_step', type=int, default=1,
        help='Step to process the training losses.')
    parser.add_argument('--val_step', type=int, default=1,
        help='Step to process the validation losses. '
             'NOTE: By default, validation loss is computed every 1000 '
             'iterations, so you won\'t probably need to use this option.')

    parser.add_argument('--train_xmin', type=int, default=None,
        help='Minimum value on x-axis of the `train` figure.')
    parser.add_argument('--train_xmax', type=int, default=None,
        help='Maximum value on x-axis of the `train` figure.')
    parser.add_argument('--val_xmin', type=int, default=None,
        help='Minimum value on x-axis of the `val` figure.')
    parser.add_argument('--val_xmax', type=int, default=None,
        help='Maximum value on x-axis of the `val` figure.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
