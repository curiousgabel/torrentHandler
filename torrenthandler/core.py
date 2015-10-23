import unittest
from os import remove

__author__ = 'Mike'


class BaseTestCase(unittest.TestCase):

    objectParams = {}

    def setUp(self):
        obj = self.__importObject()
        self.testObject = obj(**self.objectParams)
        self.setupData()

    def tearDown(self):
        del self.testObject
        self.cleanupData()

    def setupData(self):
        pass

    def cleanupData(self):
        pass

    def __importObject(self):
        name = self.__class__.__name__
        name = name.replace('Test', '', 1)
        fully_qualified_name = self.__module__ + '.' + name
        parts = fully_qualified_name.split('.')

        obj = __import__(parts[0])
        for part in parts[1:]:
            obj = getattr(obj, part)

        return obj


class Object:
    def __str__(self):
        return self.dump(True)

    def dump(self, returnString=False):
        props = vars(self)
        result = ''

        for item in props.items():
            result = str(item)

        if (not returnString):
            print(result)

        return result

    def setProperty(self, name, value):
        setattr(self, name, value)

    def set(self, name, value):
        self.setProperty(self, name, value)

    def getProperty(self, name):
        result = None

        if name in self.__dict__:
            result = self.__dict__[name]

        return result

    def get(self, name):
        return self.getProperty(self, name)

    def clear(self):
        self.__dict__.clear()


class TestObject(BaseTestCase):
    propertyName = 'testprop'
    propertyValue = 'testval'
    newPropertyValue = 'newval'
    noPropertyValue = 'noprop'

    def test_setProperty(self):
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.assertEqual(self.testObject.testprop, self.propertyValue)

    def test_setPropertyOverride(self):
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.testObject.setProperty(self.propertyName, self.newPropertyValue)
        self.assertEqual(self.testObject.testprop, self.newPropertyValue)

    def test_getProperty(self):
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.assertEqual(self.testObject.getProperty(self.propertyName), self.propertyValue)

    def test_getPropertyNone(self):
        self.assertEqual(self.testObject.getProperty(self.noPropertyValue), None)

    def test_clear(self):
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.testObject.clear()
        self.assertEqual(self.testObject.__dict__, {})

    def test_dumpString(self):
        self.testObject.clear()
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.assertEqual(self.testObject.dump(True), "('testprop', 'testval')")

    def test_dumpStringNotEqual(self):
        self.testObject.clear()
        self.testObject.setProperty(self.propertyName, self.propertyValue)
        self.assertNotEqual(self.testObject.dump(True), "badval")

    def test_dumpStringEmpty(self):
        self.testObject.clear()
        self.assertEqual(self.testObject.dump(True), '')


class Logger(Object):
    fileName = ''
    fileHandle = None

    def __init__(self, fileName):
        if fileName is not None and fileName != '':
            self.fileName = fileName
            self.startUp()
        else:
            raise TypeError('Missing filename')

    def __del__(self):
        self.close()

    def startUp(self):
        self.open()

    def open(self):
        self.fileHandle = open(self.fileName, 'a')

    def close(self):
        if self.fileHandle is not None:
            self.fileHandle.close()

    def out(self, text, ending='\n'):
        handle = self.fileHandle
        handle.write(text + ending)


class TestLogger(BaseTestCase):
    filename = 'C:\\Windows\\Temp\\tmplogfile'
    dataString = 'thisissomedata'
    objectParams = {'fileName': filename}

    def cleanupData(self):
        remove(self.filename)

    def test_noFileName(self):
        self.assertRaises(TypeError, Logger)

    def test_emptyFileName(self):
        self.assertRaises(TypeError, Logger, '')

    def test_noneFileName(self):
        self.assertRaises(TypeError, Logger, None)

    def test_out(self):
        self.testObject.out(self.dataString, '')
        self.testObject.close()

        handle = open(self.filename, 'r')
        data = handle.read()
        handle.close()

        self.testObject.open()

        self.assertEqual(self.dataString, data)
