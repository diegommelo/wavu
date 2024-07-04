import unittest
from wavu import Wavu

class TestWavu(unittest.TestCase):
    def setUp(self):
        self.wavu = Wavu()
    
    def test_get_top_head_empty(self):
        self.assertEqual(self.wavu.get_top_head(), [])
    
    def test_get_top_head_less_than_5_elements(self):
        self.wavu.heads = [1, 2, 3]
        self.assertEqual(self.wavu.get_top_head(), [1, 2, 3])
    
    def test_get_top_head_more_than_5_elements(self):
        self.wavu.heads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(self.wavu.get_top_head(), [1, 2, 3, 4, 5])
    
    def test_get_top_head_mixed_elements(self):
        self.wavu.heads = [5, 3, 7, 1, 9, 2, 8, 4, 6, 10]
        self.assertEqual(self.wavu.get_top_head(), [5, 3, 7, 1, 9])

if __name__ == '__main__':
    unittest.main()