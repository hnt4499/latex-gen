import sys
import os
import subprocess
import random
import string
from shutil import copy, SameFileError


def write_tex(tex_path, text):
    if isinstance(text, str):
        text = [text]

    with open(tex_path, "w") as tex:
        tex.write("\documentclass{minimal}\n")
        tex.write("\\begin{document}\n")
        # Write equations starting and ending with `$`, line by line
        # If only one formula
        if len(text) == 1:
            tex.write("${}$\n".format(text[0]))
        # Else if multiple formulas
        else:
            for line in text:
                equation = "\\begin{equation} " + line + " \\end{equation}\n"
                tex.write(equation)
        tex.write("\\end{document}\n")


def tex_to_dvi(tex_path, stdout=None, stderr=None):
    code = subprocess.call(
        ["latex", "-src", "-interaction=nonstopmode", tex_path],
        stdout=stdout,
        stderr=stderr
    )
    return code


def dvi_to_png(dvi_path, png_path, dpi=120, stdout=None, stderr=None):
    code = subprocess.call(
        ["dvipng", "--width*", "--height*", "-T", "tight",
        "-D", str(dpi), dvi_path, "-o", png_path],
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

    # Turn off stdout and stderr when executing scripts within Python
    with open(os.devnull, 'w') as null_io:
        stdout = null_io
        stderr = null_io

        # We call `latex` in nonstop mode to generate a .dvi
        # file from our temporary latex file
        tex_to_dvi(tmp_tex_path, stdout=stdout, stderr=stderr)

        # We then call `dvipng` to create a cropped png image
        # from the dvi output from the last script
        code = dvi_to_png(dvi_path=tmp_dvi_path, png_path=tmp_png_path,
                          dpi=dpi, stdout=stdout, stderr=stderr)
    # If error generating image, keep all the intermediate files for inspecting.
    if code != 0:
        print("\nError generating {}. "
              "Returned code {}".format(tmp_png_path, code))
    else:
        # Copy final file to `output_path` and clean up
        try:
            copy(tmp_png_path, output_path)
            os.system("rm -rf {} {}".format(tmp_dvi_path, tmp_tex_path))
        # If SameFileError, remove all intermediate files except the `.png` file.
        except SameFileError:
            os.system("ls {}* | grep -v {} | xargs rm".format(tmp_file, tmp_png_path))

    # Change back to original working directory
    os.chdir(cwd)


class TeX():
    def __init__(self, text):
        """Initialize a TeX class containing sequence(s)
        of raw TeX formulas and can be manipulated to generate `.tex`,
        `.dvi` or `.png` files.

        Parameters
        ----------
        text : str or list of str or None
            Contains raw TeX formula(s).

        """
        self.text = []
        self.add(text)

    def add(self, text):
        if text is not None:
            if isinstance(text, list):
                self.text.extend(text)
            else:
                self.text.append(text)

    def to_tex(self, tex_path):
        if self.text == []:
            return
        write_tex(tex_path, self.text)


class AutoTeX(TeX):
    def __init__(self, length, *args):
        """Automate the process of generating metadata from TeX formulas.

        Parameters
        ----------
        length : int
            Number of formulas to keep, must be greater or equal 1.
            If `len(self.text)` reached `self.length`, the functions in *args
            are executed sequentially.
        *args : callable(s)
            Functions to perform when the number of formulas stored reaches.
            These funtions must accept only one argument, `text` stored.

        """
        assert length >= 1
        self.length = length
        self.f = args
        super().__init__(self, text=None)

    def release(self, *args):
        """
        If `*arg` is provided explicitly, self.f is discarded.
        """
        if self.text == []:
            return
        if args != ():
            self.f = args
        for function in self.f:
            function(self.text)
        self.text = []

    def _add(self, text, *args):
        """
        Convenience function, only accept text as a single string.
        """
        assert isinstance(text, str)
        self.text.append(text)
        if len(self.text) == self.length:
            self.release(args)

    def add(self, text, *args):
        if isinstance(text, str):
            self._add(text, args)
        else:
            for formula in text:
                self._add(formula, args)
