class Resource(object):

    @property
    def name(self):
        return self.__class__.__name__

    def peek(self):
        return []
