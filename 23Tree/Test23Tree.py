import unittest

from _23Tree import _23Set


class Test23Tree(unittest.TestCase):
    def setUp(self):
        self.ttt = _23Set()
        return super().setUp()

    def testStr(self):
        self.assertEqual(str(self.ttt), '')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '99')
        self.ttt.insert(88)
        self.assertEqual(str(self.ttt), '88,99')
        self.ttt.insert(77)
        self.assertEqual(str(self.ttt), '77,88,99')
        self.ttt.insert(66)
        self.assertEqual(str(self.ttt), '66,77,88,99')
        self.ttt.insert(55)
        self.assertEqual(str(self.ttt), '55,66,77,88,99')
        self.ttt.insert(44)
        self.assertEqual(str(self.ttt), '44,55,66,77,88,99')
        self.ttt.insert(33)
        self.assertEqual(str(self.ttt), '33,44,55,66,77,88,99')
        
    def testStr2(self):
        self.assertEqual(str(self.ttt), '')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '99')
        self.ttt.insert(88)
        self.assertEqual(str(self.ttt), '88,99')
        self.ttt.insert(77)
        self.assertEqual(str(self.ttt), '77,88,99')
        self.ttt.insert(66)
        self.assertEqual(str(self.ttt), '66,77,88,99')
        self.ttt.insert(111)
        self.assertEqual(str(self.ttt), '66,77,88,99,111')
        self.ttt.insert(222)
        self.assertEqual(str(self.ttt), '66,77,88,99,111,222')

    def testStr3(self):
        self.assertEqual(str(self.ttt), '')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '99')
        self.ttt.delete(99)
        self.assertEqual(str(self.ttt), '')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '99')
        self.ttt.delete(99)
        self.assertEqual(str(self.ttt), '')

    def testStr4(self):
        self.assertEqual(str(self.ttt), '')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '99')
        self.ttt.insert(88)
        self.assertEqual(str(self.ttt), '88,99')
        self.ttt.delete(99)
        self.assertEqual(str(self.ttt), '88')
        self.ttt.insert(99)
        self.assertEqual(str(self.ttt), '88,99')
        self.ttt.insert(77)
        self.assertEqual(str(self.ttt), '77,88,99')
        self.ttt.delete(88)
        self.assertEqual(str(self.ttt), '77,99')

if __name__ == '__main__':
    unittest.main()
