"""
#######################################################################################
# Module: example.py
# This module show how the Textparser class can be used in own projects.
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
INPUT_FILE = r"../tests/data/test.dat"
OUTPUT_FILE = r"./dummy.out"


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
    tp = Textparser(source="This is line 1.\nThis is line 2.\n")
    print(">> pprint(tp)")
    pprint(tp)

    print("\n>> print(tp.source)")
    pprint(tp.source)

    print("\n>> pprint(tp.lines)")
    pprint(tp.lines)

    print("\n>> Initiate textparser object with data from input file.")
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

    print(">> Output source lines prepend by it's row indices (00..99: line)")
    print(">> tp.get_numbered_source_lines(output=True, nbrFormat='2d')")
    tp.get_numbered_source_lines(output=True, nbrFormat="02d")

    print("\n>> Get all source lines from start to end.")
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
    print(">> pprint(tp.get_lines(rows=(3.0, '4.0'), merge=';', end='')")
    pprint(tp.get_lines(rows=(2.0, "3.0"), merge=";", end=""))
    print(">> pprint(tp.get_lines(rows='2.0, 3.0', merge=';', end='')")
    pprint(tp.get_lines(rows="2.0, 3.0", merge=";", end=""))
    print(">> pprint(tp.get_lines(rows='2:3,3:4', merge=';', end='')")
    pprint(tp.get_lines(rows="2:3,3:4", merge=";", end=""))

    print("\n>> Get all source textlines in reverse order.")
    print(">> pprint(tp.get_lines(rows='::-1'))")
    pprint(tp.get_lines(rows="::-1"))

    print("\n>> Get every second text line starting from source line 3.")
    print(">> tp.get_lines(rows='2::2')")
    pprint(tp.get_lines(rows="2::2"))

    print("\n>> Get all lines containing frequency and lines of the 4x4 matrix.")
    print(">> tp.get_lines(rows='3,4,5,6,9,10,11,12,13', merge=';', end='')")
    print(tp.get_lines(rows="3,4,5,6,9,10,11,12,13", merge=";", end=""))

    print("\n>> Get all lines containing frequency and all lines of the 4x4 matrix.")
    print(">> tp.get_lines(rows='3:7:1, 9:13', merge=';', end='')")
    print(tp.get_lines(rows="3:7:1, 9:13", merge=";", end=""))

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

    print("\n>> Get tuple with first match of FREQUENCY (case sensitive) and unpack to idx and line.")
    print(">> idx, line = tp.get_match('FREQUENCY', ignoreCase=False)")
    print(">> print(f'Line index: {idx}, Line string: {line}')")
    idx, line = tp.get_match("FREQUENCY", ignoreCase=False)
    print(f"Line index: {idx}, Line string: {line}", end="")

    print("\n>> Get last match of 'freq' (case insensitive, partial)")
    print(">> pprint(tp.get_matches('freq')[-1])")
    pprint(tp.get_matches("freq")[-1])

    print("\n>> Get all source lines containing at least one digit surrounded by at least on whitespace")
    print(">> Note: If pattern starts with 'rx:', the part behind is evaluated as regular expression.")
    print(">> Note: '\s+':= one or more white space chars, '\d+':= one ore more digits [0-9].")
    print(">> pprint(tp.get_matches(pattern='rx:\s+\d+\s+'), ignoreCase=True")
    print(tp.get_matches(pattern="rx:\s+\d+\s+", ignoreCase=True))

    print("\n>> Get all source lines containing a digit matching {10, 20, .., 70}")
    print(">> Note: '[1-7]0':= matches single digit between 1-7 directly followed by 0.")
    print(">> pprint(tp.get_matches(pattern='rx:[1-7]0'), ignoreCase=True")
    print(tp.get_matches(pattern="rx:[1-7]0", ignoreCase=True))

    print(
        "\n>> Get source lines containing 'Frequency', where line before contains '60' and line after '80'."
    )
    print(">> Note: Subpatterns are optional and defined rel. to the line matching the main pattern.")
    print(
        ">> Subpatterns is a collections of tuples: [(rowOffset1, subpattern1), .., (rowOffset2, subpattern2)]"
    )
    print(">> match = tp.get_matches(pattern='Frequency', subpattens=[(-1, '60'), (1, '80')])")
    match = tp.get_matches(pattern="Frequency", subpatterns=((-1, "60"), (1, "80")))
    print(match)

    print("\n>> Get source lines containing 'Frequency', if number [50,60,70,80] is present two lines below.")
    print(
        ">> Note: Patterns starting with 'rx:' will perform a regular expression search on the source lines."
    )
    print(">> match = tp.get_matches(pattern='Frequency', subpattens=(2, 'rx:[5-8]0'))")
    match = tp.get_matches(pattern="Frequency", subpatterns=(2, "rx:[5-8]0"))
    print(match)

    print(
        "\n>> Get first source line containing 'Frequency', if number [50,60,70,80] is present two lines below."
    )
    print(">> match = tp.get_match(pattern='Frequency', subpattens=(2, 'rx:[5-8]0'))")
    match = tp.get_match(pattern="Frequency", subpatterns=(2, "rx:[5-8]0"))
    print(match)

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

    print("\n>> Extract 4x4 matrix elements from textfile, join columns by ',' and lines by ';'.")
    print(">> Note: Last end char removed for multiple values by default unless end char is '\\n'.")
    print(">> matrix_4x4_formatted = tp.get_values(rows='9:13', merge=',', end=';')")
    matrix_4x4_formatted = tp.get_values(rows="9:13", merge=",", end=";")
    print(">> pprint(matrix_4x4_formatted)")
    pprint(matrix_4x4_formatted)

    print("\n>> Extract single 4x4 matrix element from 2nd row and 2nd col.")
    print(">> element_r2c2 = tp.get_values(rows=10, cols=1)")
    element_r2c2 = tp.get_values(rows=10, cols=1)
    print(">> pprint(element_r2c2)")
    pprint(element_r2c2)

    print("\n>> Extract 4x4 matrix elements of the second row.")
    print(">> matrix_2nd_row = tp.get_values(rows=10)")
    matrix_2nd_row = tp.get_values(rows=10)
    print(">> pprint(matrix_2nd_row)")
    pprint(matrix_2nd_row)

    print("\n>> Extract 4x4 matrix elements of the second row, join elements by ',' and lines by ';'.")
    print(">> Note: Last end char removed for multiple values by default unless end char is '\\n'.")
    print(">> matrix_2nd_row_skip_end = tp.get_values(rows='10', merge=',', end=';')")
    matrix_2nd_row_skip_end = tp.get_values(rows="10", merge=",", end=";")
    print(">> pprint(matrix_2nd_row_formatted)")
    pprint(matrix_2nd_row_skip_end)

    print("\n>> Extract 4x4 matrix elements of the second column as multi-line string.")
    print(">> matrix_2nd_col = tp.get_values(rows='9:13', cols='1.0')")
    matrix_2nd_col = tp.get_values(rows="9:13", cols="1.0")
    print(">> pprint(matrix_2nd_col)")
    pprint(matrix_2nd_col)

    print("\n>> Extract 4x4 matrix elements of second column, join elements by ','.")
    print(">> Note: Set 'end' char instead 'merge', as we join row values in case of a single column!!!")
    print(">> matrix_last_col = tp.get_values(rows=9:13, cols=['1.0'], end=',')")
    matrix_last_col_formatted = tp.get_values(rows="9:13", cols=[1.0], end=",")
    print(">> pprint(matrix_last_col_formatted)")
    pprint(matrix_last_col_formatted)

    print("\n>> Extract 2x2 submatrix from center of the 4x4 matrix as multi-line string.")
    print(">> matrix_2x2 = tp.get_values(rows='10.0, 11.0', cols='1.0, 2.0')")
    matrix_2x2 = tp.get_values(rows="10.0, 11.0", cols="1.0, 2.0")
    print(">> print(matrix_2x2)")
    print(matrix_2x2)

    print(">> Extract 2x2 submatrix from center of the 4x4 matrix, join elements by ',' and lines by ';'.")
    print(">> Note: Last 'end' char is stripped off by default, unless 'end' is set to '\\n'.")
    print(">> matrix_2x2_formatted = tp.get_values(rows=[10, 11], cols=('1', '2.8'), merge=',', end=';')")
    matrix_2x2_formatted = tp.get_values(rows=[10, 11], cols=("1", "2.8"), merge=",", end=";")
    print(">> pprint(matrix_2x2_formatted)")
    pprint(matrix_2x2_formatted)

    print("\n>> Extract 3x3 submatrix from Fortran fixed format w/o spaces using multi-slice strings.")
    print(">> Tipp: Using cols='0:1,1:2,2:3' allows to extract values as string indices from source line.")
    print(">> matrix_3x3 = tp.get_values(rows='15:18', cols='0:1,1:2,2:3')")
    matrix_3x3 = tp.get_values(rows="15:18", cols="0:1,1:2,2:3")
    print(">> print(matrix_3x3")
    print(matrix_3x3)
    print(">> pprint(matrix_3x3")
    pprint(matrix_3x3)

    print("\n>> Extract 3x3 submatrix from Fortran fixed format w/o spaces, join cols by ',' and rows by ';'")
    print(">> matrix_3x3_formatted = tp.get_values(rows='15:18', cols='0:1,1:2,2:3'), merge=',', end=';'")
    matrix_3x3_formatted = tp.get_values(rows="15:18", cols="0:1,1:2,2:3", merge=",", end=";")
    print(">> pprint(matrix_3x3_formatted)")
    pprint(matrix_3x3_formatted)

    # -----------------------------------------------------------------------
    # Examples for some basic file operations.
    # -----------------------------------------------------------------------
    header("Examples for some basic file operations")
    print(f">> Write 3x3 matrix as multi-line string to '{OUTPUT_FILE}'.")
    print(">> Set append=False to overwrite an possible existing outfile.")
    print(f">> Textparser.write({OUTPUT_FILE}, lines=matrix_3x3, append=False)")
    Textparser.write(OUTPUT_FILE, lines=matrix_3x3, append=False)

    print(f"\n>> Append formated 3x3 matrix to existing '{OUTPUT_FILE}'.")
    print(">> Set append=True to append output to an existing outfile.")
    print(f">> Textparser.write({OUTPUT_FILE}, lines=matrix_3x3_formatted, append=True)")
    Textparser.write(OUTPUT_FILE, lines=f"{matrix_3x3_formatted}", append=True)

    print(f"\n>> Output lines of created file '{OUTPUT_FILE}' with row inidces to console.")
    print(f">> tp.from_source(source='{OUTPUT_FILE}')")
    tp.from_source(source=OUTPUT_FILE)
    print(">> tp.get_numbered_source_lines(output=True, nbrFormat='d')")
    tp.get_numbered_source_lines(output=True, nbrFormat="d")

    header("All tests/examples sucessfully completed")
