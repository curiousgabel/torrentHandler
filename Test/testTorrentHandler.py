__author__ = 'Mike'

import unittest

from torrenthandler.core import Object


class TestCore(unittest.TestCase):

    objectClass = None

    def setup(self):
        self.objectClass = Object()

    def tearDown(self):
        self.objectClass = None


class TestObject(TestCore):

    def runTest(self):
        self.testSetProperty()

    def testSetProperty(self):
        obj = self.objectClass
        name = 'propName'
        value = 'val'

        obj.setProperty(name, value)
        self.assertEquals(obj.propName, value)


def testSuite():
    result = unittest.TestSuite()
    result.addTest(TestCore())

    return result




"""testRunner = unittest.TextTestRunner()
testSuite = testSuite()
testRunner.run(testSuite)"""
unittest.main()