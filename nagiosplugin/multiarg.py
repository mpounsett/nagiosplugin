# -*- coding: utf-8 -*-
class MultiArg(object):

    def __init__(self, args, fill=None, splitchar=','):
        if isinstance(args, list):
            self.args = args
        else:
            self.args = args.split(splitchar)
        self.fill = fill

    def __len__(self):
        return self.args.__len__()

    def __iter__(self):
        return self.args.__iter__()

    def __getitem__(self, key):
        try:
            return self.args.__getitem__(key)
        except IndexError:
            pass
        if self.fill is not None:
            return self.fill
        try:
            return self.args.__getitem__(-1)
        except IndexError:
            return None
