import unittest
import csv
import os

import math
from ulttb import downsample

pwd = os.path.dirname(__file__)

try:
    long(1)
except:
    long = int

class DownsamplingTest(unittest.TestCase):
    def test_full(self):
        source = []
        result = []
        with open(os.path.join(pwd, 'source.csv')) as sf:
            for row in csv.reader(sf, delimiter=','):
                source.append([long(row[0]), float(row[1])])
        with open(os.path.join(pwd,'downsampled.csv')) as sf:
            for row in csv.reader(sf, delimiter=','):
                result.append([long(row[0]), float(row[1])])

        sampled = downsample(source, 500)
        self.assertEqual(len(result), len(sampled))
        for s, r in zip(sampled, result):
            self.assertEqual(s[0], r[0])
            self.assertEqual(s[1], r[1])
            
    def test_wrong_args_int_l(self):
        with self.assertRaises(TypeError):
            downsample(3, [2,3])
            
    def test_wrong_args_int_int(self):
        with self.assertRaises(TypeError):
            downsample(3, 3)
    
    def test_wrong_args_bad_list_1(self):
        with self.assertRaises(ValueError):
            downsample([1,2,3,4,5,6,7,8,9], 3)
    
    def test_wrong_args_bad_list_2(self):
        with self.assertRaises(ValueError):
            downsample([(1,2,3,4,), (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9)], 3)
    
    def test_wrong_args_bad_list_3(self):
        with self.assertRaises(ValueError):
            downsample([(1,2,), (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9),  (5,6,7,8,9)], 3)

    def test_wrong_args_bad_list_4(self):
        with self.assertRaises(ValueError):
            downsample([(1,2,), "test",  "test",  "test",  "test",  (5,6,7,8,9)], 3)


if __name__ == '__main__':
    unittest.main()
