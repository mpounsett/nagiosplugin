# -*- coding: utf-8 -*-
"""Exceptions with special meanings for nagiosplugin."""


class CheckError(RuntimeError):
    """Abort check execution.

    This exception should be raised if it becomes clear for a plugin
    that it is not able to determine the system status. Raising this
    exception will make the plugin display the exception's argument and
    exit with an UNKNOWN (3) status.
    """

    pass


class Timeout(RuntimeError):
    """Maximum check run time exceeded.

    This exception is raised internally by nagiosplugin if the check's
    run time takes longer than allowed. Check execution is aborted and
    the plugin exits with an UNKNOWN (3) status.
    """

    pass
