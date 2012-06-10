# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Platform-specific services"""

import os

if os.name == 'nt':
    from .nt import with_timeout
elif os.name == 'posix':
    from .posix import with_timeout
else:
    raise NotImplementedError('unsupported platform %s' % os.name)
