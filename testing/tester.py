from encoding.tests.test_sha256 import TestSHA256
from merkle.tests.test_merkle import TestMerkle

import unittest

def run():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSHA256))
    test_suite.addTest(unittest.makeSuite(TestMerkle))
    runner = unittest.TextTestRunner()
    results = runner.run(test_suite)

    print(results)