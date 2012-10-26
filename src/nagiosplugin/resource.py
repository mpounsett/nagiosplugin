# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Domain model for data acquisition."""


class Resource(object):
    """Base class for resource :term:`domain model`.

    A resource models anything that a plugin is supposed to check. You
    should subclass :class:`Resource` in your check and write whatever
    methods are needed to get the interesting bits of information. The
    most important resource subclass of a check (if there are several)
    should have the same name as the whole check.

    Subclasses may add arguments to the constructor to parametrize
    information retrieval.
    """

    @property
    def name(self):
        return self.__class__.__name__

    def probe(self):
        """Query system state and return metrics.

        This is the only method called by the check controller.
        It should trigger all necessary actions and create metrics.

        :return: list of :class:`Metric` objects.
        """
        return []
