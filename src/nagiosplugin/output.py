# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import itertools


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
        self.status = self.format_status(check)
        if self.verbose == 0:
            self.status += ' ' + self.format_perfdata(check)
        else:
            self.add_longoutput(check.verbose_str)
            self.out.append(self.format_perfdata(check, 79))

    def format_status(self, check):
        return self._screen_chars('{} {} - {}'.format(
            check.name.upper(), str(check.state).upper(), check.summary_str),
            'status line')

    def format_perfdata(self, check, linebreak=None):
        if not check.perfdata:
            return ''
        lines = ['|']
        for item, i in zip(check.perfdata, itertools.count()):
            if linebreak and len(lines[-1]) + len(item) >= linebreak:
                lines.append(item)
            else:
                lines[-1] += ' ' + self._screen_chars(
                    item, 'perfdata {}'.format(i))
        return '\n'.join(lines)

    def add_longoutput(self, text):
        if isinstance(text, list) or isinstance(text, tuple):
            for line in text:
                self.add_longoutput(line)
        else:
            self.out.append(self._screen_chars(text, 'long output'))

    def __str__(self):
        output = [elem for elem in
                  [self.status] +
                  self.out +
                  [self._screen_chars(self.logchan.stream.getvalue(),
                                      'logging output')] +
                  self.warnings if elem]
        return '\n'.join(output) + '\n'

    def _screen_chars(self, text, where):
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
