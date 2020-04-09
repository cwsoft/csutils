"""
#######################################################################################
# Module: test_textparser.py
# This module executes some tests and shows how the Textparser class can be used.
#
# @package: csutils.textparser
# @author:  cwsoft
# @version: 1.0.0
# @release: 2020/04/09
# @python:  3.6 or higher
#######################################################################################
"""
from pprint import pprint
import os
import sys

# Monkey patch system path so we can access the csutils package without installing it.
sys.path.append(os.path.abspath(r"../../"))
from csutils.textparser import Textparser

# Constants for input and output test data.
INPUT_FILE = r"./data/textparser.in"
OUTPUT_FILE = r"./data/textparser.out"


def header(text, char="*", repeat=80):
    """Prints a simple header"""
    print(f"\n{char*repeat}")
    print(f"{char*2} {text.upper()}")
    print(f"{char*repeat}")


if __name__ == "__main__":
    # -----------------------------------------------------------------------
    # Output some infos about the read textfile.
    # -----------------------------------------------------------------------
    header("Examples for extracting basic file information")

    # Initiate textparser object and load input file.
    print(">> tp = Textparser('path_to_input_textfile')")
    tp = Textparser(INPUT_FILE)

    print(">> print(tp)")
    pprint(tp)
    
    print("\n>> print(tp.path)")
    pprint(tp.path)
    
    print("\n>> print(tp.lines)")
    pprint(tp.lines)

    # -----------------------------------------------------------------------
    # Examples for extracting single and multi-line strings.
    # -----------------------------------------------------------------------
    header("Examples for extracting text lines")

    # Get first line as string.
    print(">> tp.get_line(idx=0)")
    line = tp.get_line(idx=0)
    pprint(line)

    # Get last line as string.
    print("\n>> tp.get_line(idx='-1')")
    line = tp.get_line(idx="-1")
    pprint(line)

    # Get all textlines from start to end.
    print("\n>> tp.get_lines()")
    lines = tp.get_lines()
    pprint(lines)

    # Get all textlines in reverse order.
    print("\n>> tp.get_lines(indices='::-1')")
    lines = tp.get_lines(indices="::-1")
    pprint(lines)

    # Get every second text line from line 3 onwards.
    print("\n>> tp.get_lines(indices='2::2')")
    lines = tp.get_lines(indices="2::2")
    pprint(lines)

    # -----------------------------------------------------------------------
    # Examples for get_match and get_matches method
    # -----------------------------------------------------------------------
    # Find first match of FREQUENCY (case insensitive).
    header("Examples for methods get_match and get_matches")
    
    # Find all matches of frequency (case insensitive)
    print(">> tp.get_matches('frequency')")
    matches = tp.get_matches("frequency")
    pprint(matches)

    print("\n>> tp.get_match('FREQUENCY')")
    match = tp.get_match("FREQUENCY")
    pprint(match)

    # Find first match of FREQUENCY (case sensitive).
    # One can also unpack the result of get_match into row index and textline.
    print("\n>> tp.get_match('FREQUENCY', ignoreCase=False)")
    idx, line = tp.get_match("FREQUENCY", ignoreCase=False)
    pprint((idx, line))

    # Find last match of freq (case insensitive)
    print("\n>> tp.get_matches('freq')[-1]")
    idx, line = tp.get_matches("freq")[-1]
    pprint((idx, line))

    # -----------------------------------------------------------------------
    # Examples for extracting single and multi-line column strings.
    # -----------------------------------------------------------------------
    # Find start of 4x4 matrix and extract the matrix as multi-line string.
    header("Examples for extracting single and multi-line columns strings")
    
    # Find textline index of line containing 4x4 Matrix.
    idx, _ = tp.get_match("4x4 Matrix")
    
    # Extract the 4x4 matrix from textfile as multi-line string.
    print(f">> matrix_4x4 = tp.get_lines(indices='{idx+1}:{idx+5}')")
    matrix_4x4 = tp.get_lines(indices=f"{idx+1}:{idx+5}")
    print(">> print(matrix_4x4)")
    print(matrix_4x4)
    print(">> pprint(matrix_4x4)")
    pprint(matrix_4x4)

    # Extract all 4x4 matrix elements of the second row.
    print("\n>> matrix_2nd_row = matrix_4x4.split('\\n')[1]")
    matrix_2nd_row = matrix_4x4.split("\n")[1]
    print(">> pprint(matrix_2nd_row)")
    pprint(matrix_2nd_row)

    # Extract 2nd element from 2nd row of the 4x4 matrix.
    print("\n>> element_row2_col2 = Textparser.get_col(matrix_2nd_row, idx=1)")
    element_row2_col2 = Textparser.get_col(matrix_2nd_row, idx=1)
    print(">> pprint(element_row2_col2)")
    pprint(element_row2_col2)

    # Extract second column of 4x4 matrix as multi-line string.
    print("\n>> matrix_2nd_col = Textparser.get_col(matrix_4x4, idx=1)")
    matrix_2nd_col = Textparser.get_col(matrix_4x4, idx=1)
    print(">> pprint(matrix_2nd_col)")
    pprint(matrix_2nd_col)

    # Extract last column of 4x4 matrix as comma separated string.
    print("\n>> matrix_last_col = Textparser.get_col(matrix_4x4, idx='-1', merge=', ')")
    matrix_last_col = Textparser.get_col(matrix_4x4, idx="-1", merge=", ")
    print(">> pprint(matrix_last_col)")
    pprint(matrix_last_col)

    # Extract 2x2 submatrix from 4x4 matrix (every 2nd col/row).
    print(f"\n>> lines = tp.get_lines(indices=({idx+2}, {idx+3}))")
    lines = tp.get_lines(indices=(idx + 2, idx + 3))
    print(">> matrix_2x2 = Textparser.get_cols(lines, indices='1:3')")
    matrix_2x2 = Textparser.get_cols(lines, indices="1:3")
    print(">> pprint(matrix_2x2)")
    pprint(matrix_2x2)

    # Output 2x2 submatrix as cols merged by comma, lines merged by semicolon.
    print("\n>> matrix_2x2_formatted = Textparser.get_cols(lines, indices='1,2', merge=',', end=';')")
    matrix_2x2_formatted = Textparser.get_cols(lines, indices="1,2", merge=",", end=";")
    print(">> pprint(matrix_2x2_formatted)")
    pprint(matrix_2x2_formatted)

    # -----------------------------------------------------------------------
    # Examples for some basic file operations.
    # -----------------------------------------------------------------------
    # Write the 2x2 submatrix as multi-line string to new file.
    print(f"\n>> Textparser.write({OUTPUT_FILE}, lines=matrix_2x2, append=False)")
    Textparser.write(OUTPUT_FILE, lines=matrix_2x2, append=False)

    # Append formated 2x2 submatrix to existing file.
    print(f">> Textparser.write({OUTPUT_FILE}, lines=matrix_2x2_formatted, append=True)")
    Textparser.write(OUTPUT_FILE, lines=f"{matrix_2x2_formatted}", append=True)
