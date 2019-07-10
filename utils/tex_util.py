import sys
import os
import subprocess
import random
import string
from shutil import copy


def write_tex(tex_path, text):
    if isinstance(text, str):
        text = [text]

    with open(tex_path, "w") as tex:
        tex.write("\documentclass{minimal}\n")
        tex.write("\\begin{document}\n")
        # Write equations starting and ending with `$`, line by line
        for line in text:
            tex.write("${}$\n".format(line))
        tex.write("\\end{document}\n")


def tex_to_dvi(tex_path, stdin=None, stdout=None):
    code = subprocess.call(
        ["latex", "-src", "-interaction=nonstopmode", tex_path],
        stdout=stdout,
        stderr=stderr
    )
    return code


def tex_to_img(text, output_path, dpi, tmp_dir):
    """Function to convert text form of a LaTeX formulas to `.png`.

    Parameters
    ----------
    text : str or list of str
        If `text` is a list of string, multiple formulas will be
        written into the same `.png` file.
    output_path : str
    dpi : str
        dpi of the output `.png` file.
    tmp_dir : str
        Directory to store temporary files while processing.

    """
    # Save `output_path`
    output_path = os.path.abspath(output_path)
    # Save current directory
    cwd = os.getcwd()
    # Change directory to `tmp_dir`
    os.chdir(tmp_dir)
    # Use the same name as the output_path to debug easily.
    _, filename = os.path.split(output_path)
    tmp_file, _ = os.path.splitext(filename)

    tmp_tex_path, tmp_dvi_path, tmp_png_path = ("{}.{}".format(tmp_file, ext)
                                            for ext in ["tex", "dvi", "png"])
    # Write out a temporary file containing enough latex code to hold the input
    # expression. The minimal documentclass type will turn off page numbers
    write_tex(tmp_tex_path, text)

    # Turn off stdin and stdout when executing scripts within Python
    with open(os.devnull, 'w') as null_io:
        stdout = null_io
        stderr = null_io

        # We call `latex` in nonstop mode to generate a .dvi
        # file from our temporary latex file
        tex_to_dvi(tmp_tex_path)

        # We then call `dvipng` to create a cropped png image
        # from the dvi output from the last script
        code = subprocess.call(
            ["dvipng", "--width*", "--height*", "-T", "tight",
            "-D", str(dpi), tmp_dvi_path, "-o", tmp_png_path],
            stdout=stdout,
            stderr=stderr
        )
        if code != 0:
            print("\nError generating {}. "
                  "Returned code {}".format(tmp_png_path, code))
        else:
            # Copy final file to `output_path` and clean up
            copy(tmp_png_path, output_path)


    os.system("rm -rf {}*".format(tmp_file))
    # Change back to original working directory
    os.chdir(cwd)
