"""
#######################################################################################
# Textparser class eases basic operations like search or data extraction on textfiles.
#
# @package: csutils.textparser
# @author:  cwsoft
# @python:  3.6 or higher
#######################################################################################
"""
__version__ = "1.4.0"
import os.path
import re


class Textparser:
    """Class to perform basic operations like search and data extraction on textfiles."""

    def __init__(self, source):
        """Initalize Textparser object with data from textfile path or from input string."""
        self.from_source(source)

    def __repr__(self):
        """Output string representation of the textparser object."""
        return f"<Textparser: Source '{self.source}' with {self.lines} lines>"

    @property
    def source(self):
        """Return source of the imported data as string."""
        return self._source

    @property
    def lines(self):
        """Return number of textlines from input source."""
        return len(self._lines)

    def from_source(self, source):
        """Read all textlines from specified source into memory and store data in _lines.
        Source can be a valid textfile path or an input string."""
        self._source, self._lines = "String", []
        if os.path.exists(source):
            with open(source, "r") as infile:
                self._source, self._lines = os.path.abspath(source), infile.readlines()
            return
        self._lines = source.splitlines()

    @staticmethod
    def write(path, lines, append=True):
        """Write or append input lines to textfile defined by the path string."""
        with open(path, "a" if append else "w") as outfile:
            outfile.writelines(lines)

    def get_numbered_source_lines(self, output=False, nbrFormat="5d"):
        """Return source lines prepend by their corresponding row indices.
        Set output=True to dump the result to the console stdout."""
        input_lines = [f"{idx:{nbrFormat}}: {line}" for idx, line in enumerate(self._lines)]
        if not output:
            return input_lines

        for input_line in input_lines:
            print(input_line, end="" if input_line.endswith("\n") else "\n")

    def get_lines(self, rows=":", merge="\n", end="\n"):
        """Return all textlines matching given row indices joined by merge char.
        Row indices can be a slice or comma separated string, or a container with indices."""
        rows = Textparser._get_validated_indices(rows)
        if isinstance(rows, slice):
            output = merge.join([line.rstrip("\n\r") for line in self._lines[rows]])
        else:
            output = merge.join([self._lines[idx].rstrip("\n\r") for idx in rows])

        # Append end char to last line if specified.
        return f"{output}{end}" if (end and not output.endswith(end)) else output

    def get_values(self, rows, cols=":", sep=None, merge=" ", end="\n"):
        """Return all values matching the given row and column indices.
        Row and col indices can be a slice or comma separated string, or a container with indices.
        By default, column values are joined with merge char, rows are joined with end char.
        Set merge="," and end=";" to join column values by comma and lines by semicolon."""
        cols = Textparser._get_validated_indices(cols)
        output, input_lines = "", self.get_lines(rows).splitlines()
        for line in input_lines:
            if line:
                if isinstance(cols, slice):
                    output += f"{merge.join([col.strip() for col in line.split(sep)[cols]])}{end}"
                else:
                    output += f"{merge.join([line.split(sep)[idx].strip() for idx in cols])}{end}"

        # Remove last merge char and last end char from output string by default.
        output = output.rstrip(f"{merge}{end}")

        # If end char="\n" and output has multiple values, add end char to ease output to console or file.
        return f"{output}{end}" if (end == "\n" and (merge in output or len(input_lines) > 1)) else output

    def get_match(self, pattern, subpatterns=None, ignoreCase=True):
        """Return tuple with row index and textline of the first row, matching the given pattern.
        To narrow possible matches, one can specify as many optional subpatterns as needed. Subpatterns are
        evaluated relative to the line matching the main pattern using the specified rowOffset. Subpatterns
        are defined as follows: subpatterns = [(rowOffset1, subPattern1),..., (rowOffsetN, subPatternN)].
        
        Note: Patterns starting with 'rx:' will perform a regular expression search on the source lines.
        Set ignoreCase=False to perform a case sensitive search on all specified search patterns.
        Set findAll=False to return a tuple with row index and textline of the first matching result only."""
        return self.get_matches(pattern, subpatterns, ignoreCase, findAll=False)

    def get_matches(self, pattern, subpatterns=None, ignoreCase=True, findAll=True):
        """Return list of tuples with row index and textline for all rows, matching given main pattern.
        To narrow possible matches, one can specify as many optional subpatterns as needed. Subpatterns are
        evaluated relative to the line matching the main pattern using the specified rowOffset. Subpatterns
        are defined as follows: subpatterns = [(rowOffset1, subPattern1),..., (rowOffsetN, subPatternN)].
        
        Note: Patterns starting with 'rx:' will perform a regular expression search on the source lines.
        Set ignoreCase=False to perform a case sensitive search on all specified search patterns.
        Set findAll=False to return a tuple with row index and textline of the first matching result only."""
        matches, regex = [], Textparser._get_compiled_regex(pattern, ignoreCase)
        # Loop over all input lines and check for matching patterns.
        for idx, line in enumerate(self._lines):
            if not regex and ignoreCase:
                pattern, line = pattern.lower(), line.lower()

            # Find input lines matching the specified main pattern.
            if (not regex and pattern in line) or (regex and re.search(regex, line)):
                # Check if all optional subpatterns match.
                if not self._do_subpattern_match(idx, subpatterns, ignoreCase):
                    continue

                if not findAll:
                    return (idx, self.get_lines(idx))
                matches.append((idx, self.get_lines(idx)))

        # Ensure consistent API if findAll=False and no match was found.
        if not findAll and not matches:
            return (None, None)

        # Ensure consistent API if findAll=True although no match was found.
        return matches if matches else [(None, None)]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # METHODS BELOW SHOULD BE TREATED AS PRIVATE METHODS (IMPLEMENTATION DETAILS)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def _get_validated_indices(indices):
        """Convert indices into a valid slice object or a list of integer indices."""
        # Deal with indices defined as string (e.g.: "0:4:1", "0,1,2,3.0", "1.0").
        if isinstance(indices, str):
            if ":" in indices:
                return slice(*map(lambda x: int(x.strip()) if x.strip() else None, indices.split(":")[0:3]))
            if "," in indices:
                return [int(float(x)) for x in indices.split(",")]
            return [int(float(indices))]

        # Deal with collections like lists, tuples or sets (e.g.: ["0",1,"2",3]).
        if isinstance(indices, (list, tuple, set)):
            return [int(float(x)) for x in indices]

        # Assume remaining input to be a single integer or float (e.g.: 1, or 2.0).
        return [int(float(indices))]

    @staticmethod
    def _get_compiled_regex(pattern, ignoreCase):
        """Return a compiled regex for the given pattern considering case flag."""
        if not pattern.startswith("rx:"):
            return None

        # Create a compiled reges from given pattern.
        return re.compile(pattern[3:], re.IGNORECASE) if ignoreCase else re.compile(pattern[3:])

    def _do_subpattern_match(self, row, subpatterns, ignoreCase):
        """Return True if all defined subpattern do match, otherwise False.
        Subpatterns are Tuples with (rowOffset, subpattern) evaluated relative to the main pattern."""
        if not subpatterns and not isinstance(subpatterns, (tuple, list, set)):
            return True

        # Pack single subpattern tuple into list so we can unpack as if user provided a list of tuples.
        subpatterns = [subpatterns] if isinstance(subpatterns[0], int) else subpatterns

        # Loop over all subpatterns: [(rowOffset1, subpattern1), .., (rowOffsetN, subpatternN)]
        for rowOffset, subpattern in subpatterns:
            # Check if specified rowOffset is valid.
            rowIdx = row + int(float(rowOffset))
            if rowIdx < 0 or rowIdx > self.lines - 1:
                return False

            # Extract subline from source defined by row offset and create compiled regex if needed.
            subpattern, subline = str(subpattern), self._lines[rowIdx]
            regex = Textparser._get_compiled_regex(subpattern, ignoreCase)
            if not regex and ignoreCase:
                subpattern, subline = subpattern.lower(), subline.lower()

            # Check if actual subpattern matches the source line defined by row offset.
            if not ((not regex and subpattern in subline) or (regex and re.search(regex, subline))):
                return False

        return True
