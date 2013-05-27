# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.logtail import LogTail
import nagiosplugin
import tempfile

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class LogTailTest(unittest.TestCase):

    def setUp(self):
        self.lf = tempfile.NamedTemporaryFile(prefix='log.')
        self.cf = tempfile.NamedTemporaryFile(prefix='cookie.')
        self.cookie = nagiosplugin.Cookie(self.cf.name)

    def tearDown(self):
        self.cf.close()
        self.lf.close()

    def test_empty_file(self):
        with LogTail(self.lf.name, self.cookie) as tail:
            self.assertEqual([], list(tail))

    def test_successive_reads(self):
        self.lf.write(b'first line\n')
        self.lf.flush()
        with LogTail(self.lf.name, self.cookie) as tail:
            self.assertEqual(b'first line\n', next(tail))
        self.lf.write(b'second line\n')
        self.lf.flush()
        with LogTail(self.lf.name, self.cookie) as tail:
            self.assertEqual(b'second line\n', next(tail))
        # no write
        with LogTail(self.lf.name, self.cookie) as tail:
            with self.assertRaises(StopIteration):
                next(tail)

    def test_offer_same_content_again_after_exception(self):
        self.lf.write(b'first line\n')
        self.lf.flush()
        try:
            with LogTail(self.lf.name, self.cookie) as tail:
                self.assertEqual([b'first line\n'], list(tail))
                raise RuntimeError()
        except RuntimeError:
            pass
        with LogTail(self.lf.name, self.cookie) as tail:
            self.assertEqual([b'first line\n'], list(tail))
