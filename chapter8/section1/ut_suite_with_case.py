# coding=utf-8
import unittest
from ut_case import TestCounter


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCounter('test_basics'))
    suite.addTest(TestCounter('test_update'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
