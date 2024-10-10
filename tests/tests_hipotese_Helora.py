import __init__
import unittest
import pandas as pd
import hipotese_Helora as hh

class TestDataLoader(unittest.TestCase):

    def test_remove_lines_diff(self):
        df1_raw_dict = {'Date':{0: 25/12/1995, 1: 26/12/1996, 2: 27/12/1996},
                        'Col1':{0: 10, 1: 20, 2: 30}}
        df2_raw_dict = {'Date':{0: 27/12/1996},
                        'Col1':{0: 40}}
        df3_raw_dict = {'Date':{0: 26/12/1996, 1: 27/12/1996},
                        'Col1':{0: 10, 1: 30}}
        df1 = pd.DataFrame(df1_raw_dict)
        df2 = pd.DataFrame(df2_raw_dict)
        df3 = pd.DataFrame(df3_raw_dict)
        rdf1, rdf2, rdf3 = hh.remove_lines_diff(df1, df2, df3)
        edf1 = {'Date': {2: 27/12/1996}, 'Col1': {2: 30}}
        edf2 = {'Date': {0: 27/12/1996}, 'Col1': {0: 40}}
        edf3 = {'Date': {1: 27/12/1996}, 'Col1': {1: 30}}

        pd.testing.assert_frame_equal(rdf1, pd.DataFrame(edf1))
        pd.testing.assert_frame_equal(rdf2, pd.DataFrame(edf2))
        pd.testing.assert_frame_equal(rdf3, pd.DataFrame(edf3))
    
    def test_qtd_same_sign(self):
        df_raw_dict = {'Col1': {0: 5, 1: 6, 2: 7, 3: -1, 4: -1}, 
                       'Col2': {0: 1, 2: -1, 2: 0, 3: 5, 4: -8}}
        df = pd.DataFrame(df_raw_dict)
        bools = hh.qtd_same_sign(df, ['Col1', 'Col2'])
        self.assertTupleEqual(bools, (3, 2))
