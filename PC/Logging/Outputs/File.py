from Output import Output

class File(Output):
    formatString = "{tag}:\t{message}\n"
    handle = None

    def __init__(self, fileName, formatString=None):
        super(File, self).__init__(formatString)
        self.handle = open(fileName, 'w')

    def write(self, tag, message):
        print message
        self.handle.write(self.formatString.format(tag=tag, message=message))
        self.handle.flush()

    def close(self):
        self.handle.close()
