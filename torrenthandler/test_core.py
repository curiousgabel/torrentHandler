from unittest import TestCase
from torrenthandler.core import Object, TorrentHandler
import re

__author__ = 'Mike'

class TestObject(TestCase):

    varName = 'propName'
    value = 'value'
    falseValue = 'falseValue'

    def test_setProperty(self):
        obj = Object

        obj.set(obj, name=self.varName, value=self.value)
        self.assertEquals(obj.propName, self.value)

    def test_setProperty_fail(self):
        obj = Object

        obj.set(obj, name=self.varName, value=self.value)
        self.assertNotEquals(obj.propName, self.falseValue)

    def test_getProperty(self):
        obj = Object

        obj.set(obj, name=self.varName, value=self.value)
        self.assertEquals(obj.get(obj, self.varName), self.value)

    def test_getProperty_fail(self):
        obj = Object

        obj.set(obj, name=self.varName, value=self.value)
        self.assertNotEquals(obj.get(obj, self.varName), self.falseValue)

    def test_getProperty_doesnt_exist(self):
        obj = Object

        obj.set(obj, name=self.varName, value=self.value)
        self.assertEquals(obj.get(obj, self.varName + 'novar'), None)


class TestTorrentHandler(TestCase):

    details = {'trackerName': 'http://tracker.name.com',
                'fileName': 'file_name.ext',
                'directory': '\\full\\path\\with.several\\PARTS'}

    def test_setDetails(self):
        obj = TorrentHandler

        obj.setDetails(obj, self.details)
        self.assertEquals(obj.details, self.details)

    def test_getDetails(self):
        obj = TorrentHandler

        obj.setDetails(obj, self.details)
        self.assertEquals(obj.getDetails(obj), self.details)

    def test_getFileName(self):
        obj = TorrentHandler

        obj.setDetails(obj, self.details)
        self.assertEquals(obj.getFileName(obj), self.details['fileName'])