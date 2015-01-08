'''
============================================================
Misc code project - main test suite.

Created on Jun 28, 2012
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
from tests.TestMergeGenesets import TestMergeGenesets
import test_util as tu
from tests.TestCythonExamples import TestCythonExamples
from tests.TestMultiprocessing import TestMultiprocessing

def suite():
    return tu.load_tests_from_classes([TestMergeGenesets, TestCythonExamples, TestMultiprocessing])
