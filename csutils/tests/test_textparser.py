"""
#######################################################################################
# Module: test_textparser.py
# This module executes some tests and shows how the Textparser class can be used.
#
# @package: csutils.textparser
# @author:  cwsoft
# @python:  3.6 or higher
#######################################################################################
"""
import os
import sys
from pprint import pprint

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

    print(">> Initiate textparser object with a multi-line string.")
    print(f">> tp = Textparser(source='This is line 1.\\n'This is line 2.\\n')")
    tp = Textparser(source="This is line 1.\nThis is line 2.")
    print(">> pprint(tp)")
    pprint(tp)

    print("\n>> print(tp.source)")
    pprint(tp.source)

    print("\n>> pprint(tp.lines)")
    pprint(tp.lines)

    print("\n>> Initiate textparser object with data from specified input file.")
    print(f">> tp = Textparser(source={INPUT_FILE})")
    tp = Textparser(source=INPUT_FILE)
    print(">> pprint(tp)")
    pprint(tp)

    print("\n>> pprint(tp.source)")
    pprint(tp.source)

    print("\n>> pprint(tp.lines)")
    pprint(tp.lines)

    # -----------------------------------------------------------------------
    # Examples for extracting single and multi-line strings.
    # -----------------------------------------------------------------------
    header("Examples for extracting text lines from input file")

    print(">> Output all input lines prepend by row indices (Format: 00..99: line)")
    print(">> tp.get_input_lines_with_indices(output=True, nbrFormat='2d')")
    tp.get_input_lines_with_indices(output=True, nbrFormat="02d")
    print()

    print("\n>> Get all textlines from start to end.")
    print(">> lines = tp.get_lines()")
    print(">> pprint(lines)")
    lines = tp.get_lines()
    pprint(lines)

    print("\n>> Get first line as string with default end char '\\n' appended.")
    print(">> pprint(tp.get_lines(rows=0))")
    pprint(tp.get_lines(rows=0))

    print("\n>> Get last line as string with default end char '\\n' appended.")
    print(">> pprint(tp.get_lines(rows='-1'))")
    pprint(tp.get_lines(rows="-1"))

    print("\n>> Get first and last line as string. Lines merged by '\\n' and last line append by '\\n'.")
    print(">> pprint(tp.get_lines(rows='0, -1'))")
    pprint(tp.get_lines(rows="0, -1"))

    print("\n>> Get lines 3+4 as string, with lines merged by ';' and no end char appended.")
    print(">> pprint(tp.get_lines(rows=(0.0, '-1.0'), merge=';', end='')")
    pprint(tp.get_lines(rows=(0.0, "-1.0"), merge=";", end=""))

    print("\n>> Get all textlines in reverse order.")
    print(">> pprint(tp.get_lines(rows='::-1'))")
    pprint(tp.get_lines(rows="::-1"))

    print("\n>> Get every second text line from line 3 onwards.")
    print(">> tp.get_lines(rows='2::2')")
    pprint(tp.get_lines(rows="2::2"))

    # -----------------------------------------------------------------------
    # Examples for get_match and get_matches method
    # -----------------------------------------------------------------------
    # Find first match of FREQUENCY (case insensitive).
    header("Examples for methods get_match and get_matches")

    print(">> Get all matches of 'FREQUENCY' (case insensitive)")
    print(">> matches = tp.get_matches('FREQUENCY')")
    print(">> pprint(matches)")
    matches = tp.get_matches("FREQUENCY")
    pprint(matches)

    print("\n>> Get first match of FREQUENCY (case sensitive) and unpack idx and line.")
    print(">> idx, line = tp.get_match('FREQUENCY', ignoreCase=False)")
    print(">> print(f'Line index: {idx}, Line string: {line}')")
    idx, line = tp.get_match("FREQUENCY", ignoreCase=False)
    print(f"Line index: {idx}, Line string: {line}", end="")

    print("\n>> Get last match of 'freq' (case insensitive, partial)")
    print(">> pprint(tp.get_matches('freq')[-1])")
    pprint(tp.get_matches("freq")[-1])

    # -----------------------------------------------------------------------
    # Examples for extracting values via the get_values method.
    # -----------------------------------------------------------------------
    # Find start of 4x4 matrix and extract the matrix as multi-line string.
    header("Examples for extracting values via the get_values method")

    print(">> Extract 4x4 matrix elements from textfile lines 10-13 as multi-line string.")
    print(">> Note: The stop value of a slice is not included in Python (hence rows:='9:13')")
    print(f">> matrix_4x4 = tp.get_values(rows='9:13')")
    matrix_4x4 = tp.get_values(rows="9:13")
    print(">> print(matrix_4x4)")
    print(matrix_4x4)
    print(">> pprint(matrix_4x4)")
    pprint(matrix_4x4)

    print("\n>> Extract all 4x4 matrix elements from textfile. Join columns by ',', lines by ';'.")
    print(">> matrix_4x4_formatted = tp.get_values(rows='9:13', merge=',', end=';')")
    matrix_4x4_formatted = tp.get_values(rows="9:13", merge=",", end=";")
    print(">> pprint(matrix_4x4_formatted)")
    pprint(matrix_4x4_formatted)

    print("\n>> Extract all matrix elements of the second row.")
    print(">> matrix_2nd_row = tp.get_values(rows=10)")
    matrix_2nd_row = tp.get_values(rows=10)
    print(">> pprint(matrix_2nd_row)")
    pprint(matrix_2nd_row)

    print("\n>> Extract all matrix elements of the second row. No end char.")
    print(">> matrix_2nd_row_skip_end = tp.get_values(rows='10', end=None)")
    matrix_2nd_row_skip_end = tp.get_values(rows="10", end=None)
    print(">> pprint(matrix_2nd_row_formatted)")
    pprint(matrix_2nd_row_skip_end)

    print("\n>> Extract single element from 2nd row and 2nd col from 4x4 matrix.")
    print(">> element_r2c2 = tp.get_values(rows=10, cols=1)")
    element_r2c2 = tp.get_values(rows=10, cols=1)
    print(">> pprint(element_r2c2)")
    pprint(element_r2c2)

    print("\n>> Extract second column of 4x4 matrix as multi-line string.")
    print(">> matrix_2nd_col = tp.get_values(rows='9:13', cols='1.0')")
    matrix_2nd_col = tp.get_values(rows="9:13", cols="1.0")
    print(">> pprint(matrix_2nd_col)")
    pprint(matrix_2nd_col)

    print("\n>> Extract last column of 4x4 matrix as comma separated string.")
    print(">> Note: Use 'end' char instead of 'merge', as we join row values for a single column!!!")
    print(">> matrix_last_col = tp.get_values(rows=12, cols=['-1.0'])")
    matrix_last_col_formatted = tp.get_values(rows="9:13", cols=[-1.0])
    print(">> pprint(matrix_last_col_formatted)")
    pprint(matrix_last_col_formatted)

    print("\n>> Extract a 2x2 submatrix from the 4x4 matrix as multi-line string.")
    print(">> matrix_2x2 = tp.get_values(rows='10.0, 11.0', cols='1.0, 2.0')")
    matrix_2x2 = tp.get_values(rows="10.0, 11.0", cols="1.0, 2.0")
    print(">> print(matrix_2x2)")
    print(matrix_2x2)

    print(">> Output 2x2 submatrix as cols merged by comma, lines merged by semicolon.")
    print(">> Note: Last 'end' char is stripped off by default, unless 'end' is set to '\\n'.")
    print(">> matrix_2x2_formatted = tp.get_values(rows=[10, 11], cols=('1', '2.8'), merge=',', end=';')")
    matrix_2x2_formatted = tp.get_values(rows=[10, 11], cols=("1", "2.8"), merge=",", end=";")
    print(">> pprint(matrix_2x2_formatted)")
    pprint(matrix_2x2_formatted)

    # -----------------------------------------------------------------------
    # Examples for some basic file operations.
    # -----------------------------------------------------------------------
    header("Examples for some basic file operations")
    print(f">> Write 2x2 submatrix as multi-line string to '{OUTPUT_FILE}'.")
    print(">> Use append=False to overwrite a possible existing outfile.")
    print(f">> Textparser.write({OUTPUT_FILE}, lines=matrix_2x2, append=False)")
    Textparser.write(OUTPUT_FILE, lines=matrix_2x2, append=False)

    print(f"\n>> Append formated 2x2 submatrix to '{OUTPUT_FILE}'.")
    print(">> Use append=True to append output to an existing outfile.")
    print(f">> Textparser.write({OUTPUT_FILE}, lines=matrix_2x2_formatted, append=True)")
    Textparser.write(OUTPUT_FILE, lines=f"{matrix_2x2_formatted}", append=True)

    print(f"\n>> Output lines of created file '{OUTPUT_FILE}' with row inidces to console.")
    print(f">> tp.from_source(source='{OUTPUT_FILE}')")
    tp.from_source(source=OUTPUT_FILE)
    print(">> tp.get_input_lines_with_indices(output=True, nbrFormat='02d')")
    tp.get_input_lines_with_indices(output=True, nbrFormat="02d")

    header("All tests/examples completed")
