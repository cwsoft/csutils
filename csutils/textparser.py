"""
#######################################################################################
# Textparser class eases basic operations like search or data extraction on textfiles.
#
# @package: csutils.textparser
# @author:  cwsoft
# @python:  3.6 or higher
#######################################################################################
"""
__version__ = "1.1.0"


class Textparser:
    """Class to perform basic operations like search and data extraction on textfiles."""

    def __init__(self, path):
        """Reads specified textfile into memory when initializing Textparser object."""
        self.read(path)

    def __repr__(self):
        """String representation of the textparser object."""
        return f"<Textparser: '{self._path}' contains {self.lines} lines>"

    @property
    def path(self):
        """Returns the file path of the opened textfile."""
        return self._path

    @property
    def lines(self):
        """Returns number of textlines in the opened textfile."""
        return len(self._lines)

    def read(self, path):
        """Reads all textlines of the specified textfile into memory."""
        self._path, self._lines = None, []
        with open(path, "r") as infile:
            self._path, self._lines = path, infile.readlines()

    @staticmethod
    def write(path, lines, append=True):
        """Writes or appends all input lines to the textfile defined as path string."""
        with open(path, "a" if append else "w") as outfile:
            outfile.writelines(lines)

    def get_input_lines_with_indices(self, output=False, nbrFormat="5d"):
        """Returns all input lines prepend by their corresponding row indices.
        Set output=True to dump the result to the standard output."""
        input_lines = [f"{idx:{nbrFormat}}: {line}" for idx, line in enumerate(self._lines)]
        if not output:
            return input_lines

        for input_line in input_lines:
            print(input_line, end="")

    def get_lines(self, rows=":", merge="\n", end="\n"):
        """Returns all textlines matching given row indices merged by the merge char.
        Indices can be a slice or comma separated string or a container with indices."""
        rows = Textparser._get_validated_indices(rows)
        if isinstance(rows, slice):
            output = merge.join([line.rstrip("\n\r") for line in self._lines[rows]])
        else:
            output = merge.join([self._lines[idx].rstrip("\n\r") for idx in rows])

        # Append end char to last line if specified.
        return f"{output}{end}" if (end and not output.endswith(end)) else output

    def get_values(self, rows, cols=":", sep=None, merge=" ", end="\n"):
        """Returns all values matching the given row and column indices.
        Row and col indices can be a slice or comma separated string or a container with indices.
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

        # Remove the last merge char and the last end char from the output string by default.
        output = output.rstrip(f"{merge}{end}")

        # If end char="\n" and we have multiple values, add end char to ease output to console or file.
        return f"{output}{end}" if (end == "\n" and (merge in output or len(input_lines) > 1)) else output

    def get_match(self, pattern, ignoreCase=True):
        """Returns tuple with row index and textline of first matching pattern."""
        return self.get_matches(pattern, ignoreCase, findAll=False)

    def get_matches(self, pattern, ignoreCase=True, findAll=True):
        """Returns list of tuples with row index and textline of all matching patterns.
        Set findAll=False to return a tuple with the first matching pattern only."""
        matches = []
        for idx, line in enumerate(self._lines):
            if ignoreCase:
                pattern, line = pattern.lower(), line.lower()

            if pattern in line:
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
        """Converts indices into a valid slice object or a list with integer indices."""
        # Deal with indices defined as string (e.g.: "0:4:1", "0,1,2,3.0", "1.0").
        if isinstance(indices, str):
            if ":" in indices:
                return slice(*map(lambda x: int(x.strip()) if x.strip() else None, indices.split(":")[0:3]))
            if "," in indices:
                return [int(float(x)) for x in indices.split(",")]
            return [int(float(indices))]

        # Deal with containers like lists, tuples or sets (e.g.: ["0",1,"2",3]).
        if isinstance(indices, (list, tuple, set)):
            return [int(float(x)) for x in indices]

        # Assume remaining input to be a single integer or float (e.g.: 1, or 2.0).
        return [int(float(indices))]
