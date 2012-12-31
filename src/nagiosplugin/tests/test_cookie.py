# vim: set fileencoding=utf-8 :
# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.cookie import Cookie
import unittest
import tempfile
import os


class CookieTest(unittest.TestCase):

    def setUp(self):
        self.tf = tempfile.NamedTemporaryFile(prefix='cookietest_')

    def tearDown(self):
        self.tf.close()

    def test_get_default_value_if_empty(self):
        with Cookie(self.tf.name) as c:
            self.assertEqual('default value', c.get('key', 'default value'))

    def test_get_file_contents(self):
        with open(self.tf.name, 'w') as f:
            f.write('{"hello": "world"}\n')
        with Cookie(self.tf.name) as c:
            self.assertEqual('world', c['hello'])

    def test_get_without_open_should_raise_keyerror(self):
        c = Cookie(self.tf.name)
        with self.assertRaises(KeyError):
            c['foo']

    def test_exit_should_write_content(self):
        with Cookie(self.tf.name) as c:
            c['hello'] = 'wörld'
        with open(self.tf.name) as f:
            self.assertEqual('{"hello": "w\\u00f6rld"}\n', f.read())

    def test_should_not_commit_on_exception(self):
        try:
            with Cookie(self.tf.name) as c:
                c['foo'] = True
                raise RuntimeError()
        except RuntimeError:
            pass
        with open(self.tf.name) as f:
            self.assertEqual('', f.read())

    def test_double_close_raises_no_exception(self):
        c = Cookie(self.tf.name)
        c.open()
        c.close()
        c.close()
        self.assertTrue(True)

    def test_close_within_with_block_fails(self):
        with self.assertRaises(IOError):
            with Cookie(self.tf.name) as c:
                c.close()

    def test_multiple_commit(self):
        c = Cookie(self.tf.name)
        c.open()
        c['key'] = 1
        c.commit()
        with open(self.tf.name) as f:
            self.assertIn('"key": 1', f.read())
        c['key'] = 2
        c.commit()
        with open(self.tf.name) as f:
            self.assertIn('"key": 2', f.read())
        c.close()

    def test_corrupted_cookie_should_raise(self):
        with open(self.tf.name, 'w') as f:
            f.write('{{{')
        with self.assertRaises(ValueError):
            with Cookie(self.tf.name):
                pass

    def test_wrong_cookie_format(self):
        with open(self.tf.name, 'w') as f:
            f.write('[1, 2, 3]\n')
        with self.assertRaises(ValueError):
            with Cookie(self.tf.name):
                pass

    def test_cookie_format_exception_truncates_file(self):
        with open(self.tf.name, 'w') as f:
            f.write('{slö@@ä')
        try:
            with Cookie(self.tf.name):
                pass
        except ValueError:
            self.assertEqual(0, os.stat(self.tf.name).st_size)
