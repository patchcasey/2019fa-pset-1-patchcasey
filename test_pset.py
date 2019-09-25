#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_1` package."""

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from pset_1.hash_str import hash_str
from pset_1.io import atomic_write
from pset_1.hash_str import str_to_byte


class FakeFileFailure(IOError):
    pass


class HashTests(TestCase):

    def setUp(self):
        self.count = 0

    def test_decorator(self):
        @str_to_byte
        def a(x, y):
            if isinstance(x, bytes):
                self.count += 1
            if isinstance(y, bytes):
                self.count += 1
            if self.count == 2:
                return "expected result"

        self.assertEqual(a('test','test'), "expected result")


    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        # raise NotImplementedError()
