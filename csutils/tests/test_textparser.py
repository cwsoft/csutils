"""
#######################################################################################
# Module: test_textparser.py
# This module contains the unit tests for the Textparser class.
#
# @package: csutils.textparser
# @author:  cwsoft
# @python:  3.6 or higher
#######################################################################################
"""
import os
import sys
import unittest
from pprint import pprint

# Monkey patch system path so we can access the csutils package without installing it.
sys.path.append(os.path.abspath(r"../../"))
from csutils.textparser import Textparser

# Global values
INPUT_FILE = os.path.abspath(r"./data/test.dat")
tp = Textparser(source=INPUT_FILE)


class TextparserTest(unittest.TestCase):
    def test_properties_file(self):
        """Test class properties, __repr__, _lines with source from file."""
        self.assertEqual(
            str(tp), f"<Textparser: Source '{INPUT_FILE}' with 20 lines>",
        )
        self.assertEqual(tp.source, INPUT_FILE)
        self.assertEqual(tp.lines, 20)

    def test_properties_string(self):
        """Test class properties, __repr__, _lines with source from string."""
        _tp = Textparser(source="This is line 1.\nThis is line 2.\n")
        self.assertEqual(str(_tp), r"<Textparser: Source 'String' with 2 lines>")
        self.assertEqual(_tp.source, "String")
        self.assertEqual(_tp.lines, 2)

    def test_write_read_lines(self):
        """Test methods write, from_source and _lines."""
        # Write input to temporary file and append it.
        data = "This is line 1.\nThis is line 2.\n"
        Textparser.write(r"./tmp.out", data, append=False)
        Textparser.write(r"./tmp.out", data, append=True)

        # Read content of temporary file and prepare output.
        output = data + data
        result = [f"{line}\n" for line in output.split("\n")][0:4]
        _tp = Textparser(source=r"./tmp.out")
        os.remove(r"./tmp.out")

        self.assertEqual(_tp._lines, result)

    def test_get_numbered_source_lines(self):
        """Test method get_numbered_source_lines"""
        data = "This is line 1.\nThis is line 2.\nThis is line 3.\nThis is line 4.\n"
        _tp = Textparser(source=data)
        result = [
            "0: This is line 1.\n",
            "1: This is line 2.\n",
            "2: This is line 3.\n",
            "3: This is line 4.\n",
        ]
        self.assertEqual(_tp.get_numbered_source_lines(output=False, nbrFormat="d"), result)

        # Testing custom nbrFormat and end string.
        result = ["0: This is line 1.;", "1: This is line 2.;", "2: This is line 3.;", "3: This is line 4.;"]
        self.assertEqual(_tp.get_numbered_source_lines(output=False, nbrFormat="d", end=";"), result)

        # Testing string output to console (redirect stdout to file and reset afterwards)
        result = "0: This is line 1.\n1: This is line 2.\n2: This is line 3.\n3: This is line 4.\n"
        default = sys.stdout
        with open("./dummy.tmp", mode="w") as outfile:
            sys.stdout = outfile
            _tp.get_numbered_source_lines(output=True, nbrFormat="d", end="")
            sys.stdout.close()
        sys.stdout = default
        _tp.from_source(source="./dummy.tmp")
        self.assertEqual(_tp.get_lines(), result)
        os.remove("./dummy.tmp")

        # Testing empty source output.
        _tp.from_source(source="")
        self.assertEqual(_tp.get_numbered_source_lines(output=False), [])

    def test_get_lines_defaults(self):
        """Test method get_lines with default parameters."""
        # Test single row output.
        result = "1  2  3  4\n"
        lines = tp.get_lines(rows=9)
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows=9.0)
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9.0")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9.99")
        self.assertEqual(lines, result)

        # Test multi-row output.
        result = "1  2  3  4\n5  6  7  8\n9  10 11 12\n13 14 15 16\n"
        lines = tp.get_lines(rows="9:13")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9:13:1")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9:10,10:11,11:12,12:13")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9:12:1, 12:13:1")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9:12:1:99, 12:13:1:99")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows="9,10,11,12")
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows=(9, 10, 11, 12))
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows=[9, 10, 11, 12])
        self.assertEqual(lines, result)

        lines = tp.get_lines(rows=[9, "10", "11.0", "12.99"])
        self.assertEqual(lines, result)

        # Test slice with steps.
        result = "1  2  3  4\n9  10 11 12\n"
        lines = tp.get_lines(rows="9:13:2")

    def test_get_lines_formatted(self):
        """Test method get_lines with custom formats specified."""
        result = "1  2  3  4;9  10 11 12\n"
        lines = tp.get_lines(rows="9:13:2", merge=";")
        self.assertEqual(lines, result)

        result = "1  2  3  4;9  10 11 12"
        lines = tp.get_lines(rows="9:13:2", merge=";", end="?")
        self.assertEqual(lines, result)

        result = "1  2  3  4;9  10 11 12\r\n"
        lines = tp.get_lines(rows="9:13:2", merge=";", end="\r\n")
        self.assertEqual(lines, result)

    def test_get_values_defaults(self):
        """Test method get_values with default values."""
        result = "Frequency = 50 Hz\nFREQUENCY = 60 Hz\nFrEqUeNcY = 70 Hz\nfrequency = 80 Hz\n"
        values = tp.get_values(rows="3:7")
        self.assertEqual(values, result)

        result = "50 Hz\n60 Hz\n70 Hz\n80 Hz\n"
        values = tp.get_values(rows="3:7", cols="2, 3")
        self.assertEqual(values, result)

    def test_get_values_formatted(self):
        """Test method get_values with formatted output."""
        result = "Frequency,=,50,Hz\nFREQUENCY,=,60,Hz\nFrEqUeNcY,=,70,Hz\nfrequency,=,80,Hz\n"
        values = tp.get_values(rows="3:7", merge=",")
        self.assertEqual(values, result)

        result = "Frequency,=,50,Hz|FREQUENCY,=,60,Hz|FrEqUeNcY,=,70,Hz|frequency,=,80,Hz"
        values = tp.get_values(rows="3:7", merge=",", end="|")
        self.assertEqual(values, result)

        result = "50 Hz,60 Hz,70 Hz,80 Hz"
        values = tp.get_values(rows="3:7", cols="2, 3", end=",")
        self.assertEqual(values, result)

        result = "50->Hz,60->Hz,70->Hz,80->Hz"
        values = tp.get_values(rows="3:7", cols="2, 3", merge="->", end=",")
        self.assertEqual(values, result)

        result = "50 Hz\n60 Hz\n70 Hz\n80 Hz\n"
        values = tp.get_values(rows="3:7", cols=1, sep="=")
        self.assertEqual(values, result)

        result = "50 Hz,60 Hz,70 Hz,80 Hz"
        values = tp.get_values(rows="3:7", cols=1, sep="=", end=",")
        self.assertEqual(values, result)

        result = "1 2 3\n4 5 6\n7 8 9\n"
        values = tp.get_values(rows="15:18", cols="0:1,1:2,2:3")
        self.assertEqual(values, result)

        result = "1,2,3;4,5,6;7,8,9"
        values = tp.get_values(rows="15:18", cols="0:1,1:2,2:3", merge=",", end=";")
        self.assertEqual(values, result)

    def test_get_match(self):
        """Test method get_match."""
        # Test simple main pattern.
        result = [
            (3, "Frequency = 50 Hz\n"),
            (4, "FREQUENCY = 60 Hz\n"),
            (5, "FrEqUeNcY = 70 Hz\n"),
            (6, "frequency = 80 Hz\n"),
        ]
        matches = tp.get_match(pattern="Freq")
        self.assertEqual(matches, result[0])

        matches = tp.get_match(pattern="FrEq", ignoreCase=False)
        self.assertEqual(matches, result[2])

        matches = tp.get_match(pattern="NOT_CONTAINED")
        self.assertEqual(matches, (None, None))

        # Test regex patterns and subpatterns.
        matches = tp.get_match(pattern="rx:Freq.*[6-7]0")
        self.assertEqual(matches, result[1])

        matches = tp.get_match(pattern="rx:Freq", subpatterns=(-1, "rx:[0-9]{2}"))
        self.assertEqual(matches, result[1])

        matches = tp.get_match(pattern="rx:FREQ", subpatterns=(-1, "rx:[0-9]{2}"), ignoreCase=False)
        self.assertEqual(matches, result[1])

        matches = tp.get_match(
            pattern="rx:Freq", subpatterns=[(1, "rx:[0-9]{2}"), (-1, "DUMMY")], ignoreCase=False
        )
        self.assertEqual(matches, (None, None))

    def test_get_matches(self):
        """Test method get_matches and get_match."""
        # Test simple main pattern.
        result = [
            (3, "Frequency = 50 Hz\n"),
            (4, "FREQUENCY = 60 Hz\n"),
            (5, "FrEqUeNcY = 70 Hz\n"),
            (6, "frequency = 80 Hz\n"),
        ]
        matches = tp.get_matches(pattern="Freq")
        self.assertEqual(matches, result)

        matches = tp.get_matches(pattern="NOT_CONTAINED")
        self.assertEqual(matches, [(None, None)])

        matches = tp.get_matches(pattern="FrEq", ignoreCase=True)
        self.assertEqual(matches, result)

        matches = tp.get_matches(pattern="FrEq", ignoreCase=False)
        self.assertEqual(matches, [result[2]])

        matches = tp.get_matches(pattern="FrEq", ignoreCase=False, findAll=False)
        self.assertEqual(matches, result[2])

        # Test regex main pattern.
        matches = tp.get_matches(pattern="rx:Freq")
        self.assertEqual(matches, result)

        matches = tp.get_matches(pattern="rx:Freq.*[6-7]0")
        self.assertEqual(matches, result[1:3])

        matches = tp.get_matches(pattern="rx:Freq.*[6-7]0", ignoreCase=False)
        self.assertEqual(matches, [(None, None)])

        # Test subpatterns.
        matches = tp.get_matches(pattern="rx:Freq", subpatterns=(-1, "rx:[0-9]{2}"))
        self.assertEqual(matches, result[1:])

        matches = tp.get_matches(pattern="rx:Freq", subpatterns=(1, "rx:[0-9]{2}"))
        self.assertEqual(matches, result[:3])

        matches = tp.get_matches(pattern="rx:Freq", subpatterns=[(1, "rx:[0-9]{2}"), (-1, "DUMMY")])
        self.assertEqual(matches, [result[0]])

        matches = tp.get_matches(
            pattern="rx:Freq", subpatterns=[(1, "rx:[0-9]{2}"), (-1, "DUMMY")], ignoreCase=False
        )
        self.assertEqual(matches, [(None, None)])

        matches = tp.get_matches(
            pattern="rx:Freq",
            subpatterns=[(1, "rx:[0-9]{2}"), (-1, "DUMMY")],
            ignoreCase=False,
            findAll=False,
        )
        self.assertEqual(matches, (None, None))

        matches = tp.get_matches(pattern="rx:Freq", subpatterns=(999, "rx:[0-9]{2}"))
        self.assertEqual(matches, [(None, None)])

        matches = tp.get_matches(pattern="rx:Freq", subpatterns=(-999, "rx:[0-9]{2}"))
        self.assertEqual(matches, [(None, None)])


if __name__ == "__main__":
    unittest.main()
