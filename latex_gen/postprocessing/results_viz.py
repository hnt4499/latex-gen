DESCRIPTION = '''
This script processes a `.json` file generated during training to visualize
the results.
'''
import json
import sys
import argparse

import matplotlib.pyplot as plt
import numpy as np
from latex_gen.utils.vis_util import filter_outliers


def get_x(num_steps, step):
    return np.arange(start=step, stop=step * num_steps + 1, step=step)


def get_minmax(x1, x2, mode):
    # If both are not None
    if x1 and x2:
        return mode(x1, x2)
    # If both is None
    elif (not x1) and (not x2):
        return None
    else:
        return x1 if x1 else x2


def get_kwargs(mi, ma):
    # Just a fun and convenience function
    d = {}
    if mi: d["left"] = mi
    if ma: d["right"] = ma
    return d


def main(args):
    # Read some arguments
    fig_size = (args.fig_width, args.fig_height)
    train_xmin = args.train_xmin
    train_xmax = args.train_xmax
    train_step = args.train_step
    val_xmin = args.val_xmin
    val_xmax = args.val_xmax
    val_step = args.val_step
    # Load json
    with open(args.input_json, "r") as j:
        data = json.load(j)

    train_y = np.asarray(data["train_loss_history"], dtype=np.float32)
    val_y = np.asarray(data["val_loss_history"], dtype=np.float32)
    if args.ignore_outliers:
        train_y = filter_outliers(train_y, thresh=args.threshold)
        val_y = filter_outliers(val_y, thresh=args.threshold)

    train_x = get_x(num_steps=train_y.shape[0], step=1)
    val_x = get_x(num_steps=val_y.shape[0], step=data["opt"]["checkpoint_every"])
    # Plot figure(s)
    fig = plt.figure(figsize=fig_size)
    # If single mode is activated
    if args.single:
        xmin = get_minmax(train_xmin, val_xmin, min)
        xmax = get_minmax(train_xmax, val_xmax, max)
        # Set min and max value of axes if both are specified
        plt.xlim(**get_kwargs(xmin, xmax))
        plt.plot(train_x[::train_step], train_y[::train_step])
        plt.plot(val_x[::val_step], val_y[::val_step])
    # Else, plot two subplots
    else:
        # Plot train data
        ax1 = plt.subplot(211)
        plt.xlim(**get_kwargs(train_xmin, train_xmax))
        ax1.plot(train_x[::train_step], train_y[::train_step])
        # Plot val data
        ax2 = plt.subplot(212)
        plt.xlim(**get_kwargs(val_xmin, val_xmax))
        ax2.plot(val_x[::val_step], val_y[::val_step])
    # Save figure
    plt.savefig(fname=args.output_file, dpi=args.dpi)


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

    parser.add_argument('--train_step', type=int, default=1000,
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
