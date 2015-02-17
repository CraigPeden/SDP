import sys

from Output import Output

class StdOut(Output):
    formatString = "{tag}:\t{message}\n"

    def write(self, tag, message):
        sys.stdout.write(self.formatString.format(tag=tag, message=message))
        sys.stdout.flush()
