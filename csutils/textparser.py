"""
#######################################################################################
# Textparser class eases basic operations like search or data extraction on textfiles.
#
# @package: csutils.textparser
# @author:  cwsoft
# @version: 1.0.0
# @release: 2020/04/09
# @python:  3.6 or higher
#######################################################################################
"""
__version__ = "1.0.0"


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
        return len(self._path)

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

    def get_line(self, idx):
        """Returns single textline matching the given 0-based row index."""
        return self._lines[int(idx)]

    def get_lines(self, indices=":", end=""):
        """Returns all textlines matching the given row indices.
        Indices can be a slice or comma separated string or a container with indices."""
        indices = Textparser._get_validated_indices(indices)
        if isinstance(indices, slice):
            return end.join(self._lines[indices])
        return end.join([self._lines[idx] for idx in indices])

    @staticmethod
    def get_col(lines, idx, sep=None, merge="\n"):
        """Returns column value(s) from input lines matching given 0-based column index.
        Set merge="," to join individual column values by comma instead a new line char."""
        output, input_lines = "", lines.splitlines()
        for line in input_lines:
            if line:
                output += f"{line.split(sep)[int(idx)].strip()}{merge}"

        # Keep last "\n" if multiple values are joined to ease output to console or file.
        return output if (len(input_lines) > 1 and merge == "\n") else output.rstrip(merge)

    @staticmethod
    def get_cols(lines, indices=":", sep=None, merge=" ", end="\n"):
        """Returns column value(s) from input lines matching given column indices.
        Indices can be a slice or comma separated string or a container with indices.
        Set merge="," and end=";" to join column values by comma and lines by semicolon."""
        indices = Textparser._get_validated_indices(indices)
        output, input_lines = "", lines.splitlines()
        for line in input_lines:
            if line:
                if isinstance(indices, slice):
                    output += f"{merge.join([col.strip() for col in line.split(sep)[indices]])}{end}"
                else:
                    output += f"{merge.join([line.split(sep)[idx].strip() for idx in indices])}{end}"

        # Keep last end character in case of line break to ease output to console or file.
        return output.rstrip(merge) if end == "\n" else output.rstrip(f"{merge}{end}")

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
                    return (idx, self.get_line(idx))
                matches.append((idx, self.get_line(idx)))

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
        """Converts indices into a valid slice object or a tuple of integer indices."""
        # Deal with indices defined as string (e.g.: "0:4:1", "0,1,2,3", "0").
        if isinstance(indices, str):
            if ":" in indices:
                return slice(
                    *map(
                        lambda x: int(x.strip()) if x.strip() else None,
                        indices.split(":")[0:3],
                    )
                )
            if "," in indices:
                return [int(x) for x in indices.split(",")]
            return tuple(int(indices))

        # Deal with containers like lists, tuples or sets (e.g.: [0,1,2,3]).
        if isinstance(indices, (list, tuple, set)):
            return tuple([int(x) for x in indices])

        # Treat rest as single integer and wrap it into tuple for consistent access.
        return tuple(int(indices))
