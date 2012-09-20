import collections
import itertools
import re


def zap_none(val):
    if val is None:
        return ''
    return val


def quote(label):
    if re.match(r'^\w+$', label):
        return label
    return "'%s'" % label


class Performance(collections.namedtuple('Performance', [
    'label', 'value', 'uom', 'warn', 'crit', 'min', 'max'])):

    def __new__(cls, label, value, uom='', warn='', crit='', min='', max=''):
        if len(label) > 20:
            raise RuntimeError('label is too long (20 chars max)', label)
        if "'" in label:
            raise RuntimeError('label contains illegal character "\'"',
                               label)
        return super(cls, Performance).__new__(
            cls, label, value, zap_none(uom), zap_none(warn), zap_none(crit),
            zap_none(min), zap_none(max))

    def __str__(self):
        out = ['%s=%s%s' % (quote(self.label), self.value, self.uom),
               str(self.warn), str(self.crit), str(self.min), str(self.max)]
        out = reversed(list(
            itertools.dropwhile(lambda x: x == '', reversed(out))))
        return ';'.join(out)
