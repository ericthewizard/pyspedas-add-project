import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_fgm_data(self):
        out_vars = pyspedas.csswe.fgm(time_clip=True)
        self.assertTrue(data_exists('b_field'))

    def test_load_rep_data(self):
        out_vars = pyspedas.csswe.reptile()
        self.assertTrue(data_exists('E1flux'))

    def test_load_notplot(self):
        out_vars = pyspedas.csswe.reptile(notplot=True)
        self.assertTrue('E1flux' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.csswe.reptile(downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
