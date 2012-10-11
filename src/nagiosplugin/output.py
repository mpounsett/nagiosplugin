# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

class Output:

    ILLEGAL = '|'
    ILLEGAL_TRANSLATE = ''.maketrans('', '', ILLEGAL)

    def __init__(self, logchan, verbose=0):
        self.logchan = logchan
        self.verbose = verbose
        self.status = ''
        self.out = []
        self.warnings = []

    def add(self, check):
        if self.verbose > 0:
            self.multiline()
        else:
            self.oneline()

    def add_status(self, statusline):
        self.status = self._screen(statusline, 'status line')

    def add_longoutput(self, text):
        if isinstance(text, list) or isinstance(text, tuple):
            for line in text:
                self.add_longoutput(line)
        else:
            self.out.append(self._screen(text, 'long output'))

    def __str__(self):
        output = [elem for elem in
                  [self.status] +
                  self.out +
                  [self._screen(self.logchan.stream.getvalue(),
                                'logging output')] +
                  self.warnings if elem]
        return '\n'.join(output) + '\n'

    def _screen(self, text, where):
        text = text.rstrip('\n')
        screened = text.translate(self.ILLEGAL_TRANSLATE)
        if screened != text:
            self.warnings.append(self._illegal_chars_warning(
                where, set(text) - set(screened)))
        return screened

    def _illegal_chars_warning(self, where, removed_chars):
        hex_chars = ', '.join('0x{:x}'.format(ord(c)) for c in removed_chars)
        return 'warning: removed illegal characters ({}) from {}'.format(
            hex_chars, where)
