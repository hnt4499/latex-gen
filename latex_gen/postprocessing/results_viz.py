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
from matplotlib.patches import Rectangle


def get_x(num_steps, step):
    return np.arange(start=step, stop=step * num_steps + 1, step=step)


def get_minmax(*args):
    minmax = []
    for x, default_value in args:
        minmax.append(default_value if x is None else x)
    return tuple(minmax)


def plot(ax, xdata, ydata,
         xmin, xmax, ymin, ymax,
         xlabel="Steps", ylabel="Loss"):
    line = ax.plot(xdata, ydata)
    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(bottom=ymin, top=ymax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return line


def main(args):
    # Read some arguments
    fig_size = (args.fig_width, args.fig_height)

    train_xmin = args.train_xmin
    train_xmax = args.train_xmax
    train_ymin = args.train_ymin
    train_ymax = args.train_ymax
    train_step = args.train_step

    val_xmin = args.val_xmin
    val_xmax = args.val_xmax
    val_ymin = args.val_ymin
    val_ymax = args.val_ymax
    val_step = args.val_step
    # Load json
    with open(args.input_json, "r") as j:
        data = json.load(j)
    # Get data
    train_y = np.asarray(data["train_loss_history"], dtype=np.float32)
    val_y = np.asarray(data["val_loss_history"], dtype=np.float32)
    # Get x value (similar to `time step`)
    train_x = get_x(num_steps=train_y.shape[0], step=1)
    val_x = get_x(num_steps=val_y.shape[0], step=data["opt"]["checkpoint_every"])
    # Perform outliers filtering
    if args.ignore_outliers:
        train_x, train_y = filter_outliers(train_x, train_y, thresh=args.threshold, mode="last")
        val_x, val_y = filter_outliers(val_x, val_y, thresh=args.threshold, mode="last")
    # Placeholder for extra legend
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    # Formalize xmax and xmin
    train_xmin, train_xmax, train_ymin, train_ymax = get_minmax(
        (train_xmin, min(train_x)),
        (train_xmax, max(train_x)),
        (train_ymin, min(train_y)),
        (train_ymax, max(train_y))
    )
    val_xmin, val_xmax, val_ymin, val_ymax = get_minmax(
        (val_xmin, min(val_x)),
        (val_xmax, max(val_x)),
        (val_ymin, min(val_y)),
        (val_ymax, max(val_y))
    )
    # Plot figure(s)
    fig = plt.figure(figsize=fig_size)
    # If single mode is activated
    if args.single:
        xmin = min(train_xmin, val_xmin)
        xmax = max(train_xmax, val_xmax)
        ymin = min(train_ymin, val_ymin)
        ymax = max(train_ymax, val_ymax)
        # Set min and max value of axes
        ax = plt.subplot(111)
        line1, = plot(ax, train_x[::train_step], train_y[::train_step],
                      xmin, xmax, ymin, ymax)
        line2, = plot(ax, val_x[::val_step], val_y[::val_step],
                      xmin, xmax, ymin, ymax)
        # Legend to put on top
        leg_top = ["train_loss", "val_loss"]
        leg_line = [line1, line2]
    # Else, plot two subplots
    else:
        # Plot train data
        ax = plt.subplot(211)
        line, = plot(ax, train_x[::train_step], train_y[::train_step],
                     train_xmin, train_xmax, train_ymin, train_ymax)
        # Plot val data
        ax2 = plt.subplot(212)
        plot(ax2, val_x[::val_step], val_y[::val_step],
             val_xmin, val_xmax, val_ymin, val_ymax)
        # Legend to put on top
        leg_top = ["train_loss"]
        leg_line = [line]
        # Set legend "val_loss" independently
        ax2.legend(["val_loss"])
    # Add additional information. The idea of extra legend was taken from
    #   https://stackoverflow.com/a/16827257
    info = ["batch_size", "wordvec_size", "seq_length", "num_layers",
            "rnn_size", "dropout", "learning_rate", "lr_decay_factor"]
    info = [r"{}: {}".format(opt, data["opt"][opt]) for opt in info]
    ax.legend(handles=leg_line + [extra] * len(info),
              labels=leg_top + info,
              # Beautify the legends, taken from
              #   https://stackoverflow.com/a/4701285
              loc='upper center',
              bbox_to_anchor=(0.5, 1.1),
              ncol=3, fancybox=True, shadow=True)
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
        help='Whether to ignore outliers when processing `.json` file. '
             'NOTE: this option might not work appropriately when '
             'using with `--single` option. Try setting ymin and ymax instead.')
    parser.add_argument('--threshold', type=float, default=3.5,
        help='Threshold to compare to `z-score`. Only used '
             'when `ignore_outliers` is set to True.')
    parser.add_argument('--single', action="store_true",
        help='When set to `True`, data will be plotted on the same figure.')

    parser.add_argument('--fig_width', type=int, default=10,
        help='Width of the figure.')
    parser.add_argument('--fig_height', type=int, default=10,
        help='Height of the figure.')
    parser.add_argument('--dpi', type=int, default=None,
        help='DPI of the figure.')

    parser.add_argument('--train_step', type=int, default=1000,
        help='Step to process the training losses.')
    parser.add_argument('--val_step', type=int, default=1,
        help='Step to process the validation losses. '
             'NOTE: By default, validation loss is computed every 1000 '
             'iterations, so you won\'t probably need to use this option.')

    parser.add_argument('--train_xmin', type=float, default=None,
        help='Minimum value on x-axis of the `train` figure.')
    parser.add_argument('--train_xmax', type=float, default=None,
        help='Maximum value on x-axis of the `train` figure.')
    parser.add_argument('--val_xmin', type=float, default=None,
        help='Minimum value on x-axis of the `val` figure.')
    parser.add_argument('--val_xmax', type=float, default=None,
        help='Maximum value on x-axis of the `val` figure.')

    parser.add_argument('--train_ymin', type=float, default=None,
        help='Minimum value on y-axis of the `train` figure.')
    parser.add_argument('--train_ymax', type=float, default=None,
        help='Maximum value on y-axis of the `train` figure.')
    parser.add_argument('--val_ymin', type=float, default=None,
        help='Minimum value on y-axis of the `val` figure.')
    parser.add_argument('--val_ymax', type=float, default=None,
        help='Maximum value on y-axis of the `val` figure.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
