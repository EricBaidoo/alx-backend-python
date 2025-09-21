#!/usr/bin/env python3
"""Unit tests for utils.py"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ( {"a": 1}, ("a",), 1 ),
        ( {"a": {"b": 2}}, ("a",), {"b": 2} ),
        ( {"a": {"b": 2}}, ("a", "b"), 2 ),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ( {}, ("a",), KeyError ),
        ( {"a": 1}, ("a", "b"), KeyError ),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)

if __name__ == "__main__":
    unittest.main()
import unittest
from utils import add

class TestAdd(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2,2),4)

if __name__ == '__main__':
    unittest.main()