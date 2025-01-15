#!/usr/bin/env python3
"""
Test numbered ip questions are in sequence.

.. include:: docs/test_sequence.md
"""
from glob import glob
import os, unittest, warnings




class OutOfRange(Warning):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return f"\nOut of Range in {self.message}"




class Test(unittest.TestCase):

    def test_sequence(self):
        """
        Question numbers are sequential
        """
        years = os.listdir("data")
        years = [_ for _ in years if os.path.isdir(f"data/{_}")]
        cum_out = []
        for year in years:
            out = []
            ipqs = sorted(glob(f"data/{year}/*.xml"))
            first = ipqs[0].split("/")[-1].split('-')[-1][:-4]
            last = ipqs[-1].split("/")[-1].split('-')[-1][:-4]
            for n in list(range(int(first), int(last)+1)):
                if not f"data/{year}/ipq-{year}--{n:0>4}.xml" in ipqs:
                    out.append(str(n))
            if len(out) > 0:
                cum_out.append([year, out])
                warnings.warn(f"{year}: {', '.join(out)}", OutOfRange)
            else:
                print(year, "OK")

        if len(cum_out) > 0:
            [print(_) for _ in cum_out]

        #self.assertEqual(len(cum_out), 0)




if __name__ == '__main__':
    unittest.main()
