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



if __name__ == '__main__':
    unittest.main()
