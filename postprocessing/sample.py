import os
import sys
import argparse
import subprocess


def main(args):
    out = os.path.abspath(args.output_path)
    ckpt = os.path.abspath(args.checkpoint)
    length = args.length
    start_text = args.start_text
    sample = args.sample
    temp = args.temperature

    assert sample == 0 or sample == 1

    cmd = "th sample.lua -checkpoint {} -length {} \-start_text \'{}\' \
           -sample {} -temperature {}".format(ckpt, length, start_text, sample, temp)
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    
    with open(out, "w") as out_:
        out_.write(result)


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('output_path', type=str,
        help='Path to which output file will be saved.')
    parser.add_argument('checkpoint', type=str,
        help='Path to the checkpoint.')
    parser.add_argument('length', type=str,
        help='Length of the entire generated text.')

    parser.add_argument('--start_text', type=str, default='',
        help='Piece of text used before start sampling. By default '
             'this is \'\', meaning that text will be sample from scratch.')
    parser.add_argument('--sample', type=int, default=1,
        help='`1`: sample from the next-character distribution at each '
             'timestep.\n`0`: pick the argmax at each timestep. '
             'Sampling (`sample=1`) tends to produce more interesting results.')
    parser.add_argument('--temperature', type=int, default=1,
        help='Softmax temperature to use when sampling. '
             'Higher temperatures give noiser samples.')

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
