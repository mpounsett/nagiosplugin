# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def filter_output(output, filtered):
    """ Filters out characters from output """
    for char in filtered:
        output = output.replace(char, '')
    return output


class Output(object):

    ILLEGAL = '|'

    def __init__(self, logchan, verbose=0):
        self.logchan = logchan
        self.verbose = verbose
        self.status = ''
        self.out = []
        self.warnings = []
        self.longperfdata = []

    def add(self, check):
        self.status = self.format_status(check)
        if self.verbose == 0:
            perfdata = self.format_perfdata(check)
            if perfdata:
                self.status += ' ' + perfdata
        else:
            self.add_longoutput(check.verbose_str)
            self.longperfdata.append(self.format_perfdata(check, 79))

    def format_status(self, check):
        if check.name:
            name_prefix = check.name.upper() + ' '
        else:
            name_prefix = ''
        summary_str = check.summary_str.strip()
        return self._screen_chars('{0}{1}{2}'.format(
            name_prefix, str(check.state).upper(),
            ' - ' + summary_str if summary_str else ''), 'status line')

    def format_perfdata(self, check, linebreak=None):
        if not check.perfdata:
            return ''
        out = ' '.join(check.perfdata)
        return '| ' + self._screen_chars(out, 'perfdata')

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
                  self.warnings +
                  self.longperfdata
                  if elem]
        return '\n'.join(output) + '\n'

    def _screen_chars(self, text, where):
        text = text.rstrip('\n')
        screened = filter_output(text, self.ILLEGAL)
        if screened != text:
            self.warnings.append(self._illegal_chars_warning(
                where, set(text) - set(screened)))
        return screened

    def _illegal_chars_warning(self, where, removed_chars):
        hex_chars = ', '.join('0x{0:x}'.format(ord(c)) for c in removed_chars)
        return 'warning: removed illegal characters ({0}) from {1}'.format(
            hex_chars, where)
