# -*- coding: utf-8 -*-
"""Domain model for data :term:`acquisition`.

:class:`Resource` is the base class for the plugin's :term:`domain
model`. It shoul model the relevant details of reality that a plugin is
supposed to check. The :class:`~.check.Check` controller calls
:meth:`Resource.probe` on all passed resource objects to acquire data.

Plugin authors should subclass :class:`Resource` and write
whatever methods are needed to get the interesting bits of information.
The most important resource subclass should be named after the plugin
itself.
"""


class Resource(object):
    """Abstract base class for custom domain models.

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

        :return: list of :class:`~nagiosplugin.metric.Metric` objects,
            or generator that emits :class:`~nagiosplugin.metric.Metric`
            objects, or single :class:`~nagiosplugin.metric.Metric`
            object
        """
        return []
