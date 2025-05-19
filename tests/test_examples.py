# -*- coding: utf-8 -*-
import re
import subprocess
import sys
import os.path as p

try:
    from importlib.resources import files as resource_files
    USING_IMPORTLIB = True
except ImportError:
    from pkg_resources import resource_filename as resource_files
    USING_IMPORTLIB = False

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class ExamplesTest(unittest.TestCase):
    base = p.normpath(p.join(p.dirname(p.abspath(__file__)), '..', '..'))

    def _run_example(self, program, regexp):
        if USING_IMPORTLIB:
            program_path = resource_files('nagiosplugin.examples') / program
        else:
            program_path = resource_files('nagiosplugin.examples', program)
        proc = subprocess.Popen([sys.executable, program_path, '-v'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env={'PYTHONPATH': ':'.join(sys.path)})
        out, err = proc.communicate()
        self.assertEqual(err.decode(), '')
        self.assertTrue(re.match(regexp, out.decode()) is not None,
                        '"{0}" does not match "{1}"'.format(
                            out.decode(), regexp))
        self.assertEqual(0, proc.returncode)

    def test_check_load(self):
        if not sys.platform.startswith('linux'):  # pragma: no cover
            self.skipTest('requires Linux')
        self._run_example('check_load.py', """\
LOAD OK - loadavg is [0-9., ]+
| load15=[0-9.]+;;;0 load1=[0-9.]+;;;0 load5=[0-9.]+;;;0
""")

    def test_check_users(self):
        self._run_example('check_users.py', """\
USERS OK - \\d+ users logged in
users: .*
| total=\\d+;;;0 unique=\\d+;;;0
""")

    def test_check_world(self):
        self._run_example('check_world.py', '^WORLD OK$')
