import sys
import os
import subprocess
import random
import string
from shutil import copy

def tex_to_img(text, output_path, dpi, tmp_dir):
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
    with open(tmp_tex_path, "w") as tmp_tex:
        tmp_tex.write("\documentclass{minimal}\n")
        tmp_tex.write("\\begin{document}\n")
        # Write equation starting and ending with `$`
        tmp_tex.write("${}$\n".format(text))
        tmp_tex.write("\\end{document}\n")

    # Turn off stdin and stdout when executing scripts within Python
    with open(os.devnull, 'w') as null_io:
        stdout = null_io
        stderr = null_io

        # We call `latex` in nonstop mode to generate a .dvi
        # file from our temporary latex file
        subprocess.call(
            ["latex", "-src", "-interaction=nonstopmode", tmp_tex_path],
            stdout=stdout,
            stderr=stderr
        )

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
