import unittest
from Animated23Tree import _23TreeVisualizer as VT

class Test_Test23Visualizer(unittest.TestCase):
    def setUp(self):
        self.vt = VT()
        return super().setUp()

    def test_A(self):
        self.vt.show()
        self.vt.animOn('aa')
        self.vt.add(80)
        self.vt.step()

if __name__ == '__main__':
    unittest.main()
