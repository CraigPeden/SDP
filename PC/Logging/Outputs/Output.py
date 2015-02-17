class Output(object):
    formatString = "{tag}:\t{message}\n"
    def __init__(self, formatString=None):
        if formatString:
            self.formatString = formatString

    def write(self, tag, message):
        pass

    def close(self):
        pass
