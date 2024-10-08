import __init__
import unittest
import unittest.mock
import pandas as pd
import basics as bs
import analise_temporal as at

class TestDataLoader(unittest.TestCase):

    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_negative(self, mocked_input):
        mocked_input.side_effect = ['N']
        self.assertEqual(at.ask_period(), 'M')
    
    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_week(self, mocked_input):
        mocked_input.side_effect = ['Y', 'W']
        self.assertEqual(at.ask_period(), 'W')
    
    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_month(self, mocked_input):
        mocked_input.side_effect = ['Y', 'M']
        self.assertEqual(at.ask_period(), 'M')
    
    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_bimonthly(self, mocked_input):
        mocked_input.side_effect = ['Y','B']
        self.assertEqual(at.ask_period(), 'B')
    
    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_quarter(self, mocked_input):
        mocked_input.side_effect = ['Y','T']
        self.assertEqual(at.ask_period(), 'T')
    
    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_semester(self, mocked_input):
        mocked_input.side_effect = ['Y','S']
        self.assertEqual(at.ask_period(), 'S')

    @unittest.mock.patch("analise_temporal.input")
    def test_ask_period_positive_year(self, mocked_input):
        mocked_input.side_effect = ['Y','Y']
        self.assertEqual(at.ask_period(), 'Y')

    @unittest.mock.patch("analise_temporal.input")
    def test_error_in_ask_period(self, mocked_input):
        mocked_input.side_effect = ['Y','L']
        try:
            at.ask_period()
        except ValueError:
            assert True

    def test_agrupate_dates_weekly(self):
        expected_raw_dict = {'Price': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 1.2590000000000001, pd.Timestamp('2020-07-20 00:00:00'): 1.2848333333333335, pd.Timestamp('2020-07-27 00:00:00'): 1.6829999999999998, pd.Timestamp('2020-08-03 00:00:00'): 2.3284285714285713, pd.Timestamp('2020-08-10 00:00:00'): 3.6336666666666666}, 
                    'Open': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 1.1343333333333332, pd.Timestamp('2020-07-20 00:00:00'): 1.1323333333333334, pd.Timestamp('2020-07-27 00:00:00'): 1.675, pd.Timestamp('2020-08-03 00:00:00'): 2.1287142857142856, pd.Timestamp('2020-08-10 00:00:00'): 3.4523333333333333}, 
                    'High': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 1.3139999999999998, pd.Timestamp('2020-07-20 00:00:00'): 1.3724999999999998, pd.Timestamp('2020-07-27 00:00:00'): 1.789, pd.Timestamp('2020-08-03 00:00:00'): 2.400714285714286, pd.Timestamp('2020-08-10 00:00:00'): 3.815}, 
                    'Low': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 1.0793333333333333, pd.Timestamp('2020-07-20 00:00:00'): 1.1211666666666666, pd.Timestamp('2020-07-27 00:00:00'): 1.5805714285714285, pd.Timestamp('2020-08-03 00:00:00'): 2.009857142857143, pd.Timestamp('2020-08-10 00:00:00'): 3.1799999999999997}, 
                    'Vol.': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 0.0, pd.Timestamp('2020-07-20 00:00:00'): 0.0, pd.Timestamp('2020-07-27 00:00:00'): 0.0, pd.Timestamp('2020-08-03 00:00:00'): 0.0, pd.Timestamp('2020-08-10 00:00:00'): 0.0}, 
                    'Change %': 
                    {pd.Timestamp('2020-07-13 00:00:00'): 0.12643333333333331, pd.Timestamp('2020-07-20 00:00:00'): 0.054116666666666674, pd.Timestamp('2020-07-27 00:00:00'): 0.005871428571428572, pd.Timestamp('2020-08-03 00:00:00'): 0.09184285714285714, pd.Timestamp('2020-08-10 00:00:00'): 0.054733333333333335}, 
                    'Start Date': 
                    {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00'), pd.Timestamp('2020-07-20 00:00:00'): pd.Timestamp('2020-07-20 00:00:00'), pd.Timestamp('2020-07-27 00:00:00'): pd.Timestamp('2020-07-27 00:00:00'), pd.Timestamp('2020-08-03 00:00:00'): pd.Timestamp('2020-08-03 00:00:00'), pd.Timestamp('2020-08-10 00:00:00'): pd.Timestamp('2020-08-10 00:00:00')}, 
                    'End Date': 
                    {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-20 00:00:00'), pd.Timestamp('2020-07-20 00:00:00'): pd.Timestamp('2020-07-27 00:00:00'), pd.Timestamp('2020-07-27 00:00:00'): pd.Timestamp('2020-08-03 00:00:00'), pd.Timestamp('2020-08-03 00:00:00'): pd.Timestamp('2020-08-10 00:00:00'), pd.Timestamp('2020-08-10 00:00:00'): pd.Timestamp('2020-08-17 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_4_bimester.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'W')
        pd.testing.assert_frame_equal(df, expected)
    
    def test_agrupate_dates_monthly(self):
        expected_raw_dict = {'Price': {pd.Timestamp('2020-07-13 00:00:00'): 1.8695599999999999, pd.Timestamp('2020-08-12 00:00:00'): 3.728}, 
                             'Open': {pd.Timestamp('2020-07-13 00:00:00'): 1.7380799999999998, pd.Timestamp('2020-08-12 00:00:00'): 3.728}, 
                             'High': {pd.Timestamp('2020-07-13 00:00:00'): 1.9531999999999998, pd.Timestamp('2020-08-12 00:00:00'): 4.12}, 
                             'Low': {pd.Timestamp('2020-07-13 00:00:00'): 1.6421199999999998, pd.Timestamp('2020-08-12 00:00:00'): 3.585}, 
                             'Vol.': {pd.Timestamp('2020-07-13 00:00:00'): 0.0, pd.Timestamp('2020-08-12 00:00:00'): 0.0}, 
                             'Change %': {pd.Timestamp('2020-07-13 00:00:00'): 0.062088000000000004, pd.Timestamp('2020-08-12 00:00:00'): 0.0}, 
                             'Start Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00'), pd.Timestamp('2020-08-12 00:00:00'): pd.Timestamp('2020-08-12 00:00:00')}, 
                             'End Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-08-12 00:00:00'), pd.Timestamp('2020-08-12 00:00:00'): pd.Timestamp('2020-09-11 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_4_bimester.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'M')
        pd.testing.assert_frame_equal(df, expected)
    
    def test_agrupate_dates_bimonthly(self):
        expected_raw_dict = {'Price': {pd.Timestamp('2020-07-13 00:00:00'): 1.9410384615384615}, 
                             'Open': {pd.Timestamp('2020-07-13 00:00:00'): 1.8146153846153845}, 
                             'High': {pd.Timestamp('2020-07-13 00:00:00'): 2.036538461538462}, 
                             'Low': {pd.Timestamp('2020-07-13 00:00:00'): 1.7168461538461537}, 
                             'Vol.': {pd.Timestamp('2020-07-13 00:00:00'): 0.0}, 
                             'Change %': {pd.Timestamp('2020-07-13 00:00:00'): 0.0597}, 
                             'Start Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00')}, 
                             'End Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-09-11 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_4_bimester.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'B')
        pd.testing.assert_frame_equal(df, expected)
    
    def test_agrupate_dates_by_trimester(self):
        expected_raw_dict = {'Price': {pd.Timestamp('2020-07-13 00:00:00'): 2.7614823529411763, pd.Timestamp('2020-10-11 00:00:00'): 1.8996222222222223, pd.Timestamp('2021-01-09 00:00:00'): 11.195651685393258, pd.Timestamp('2021-04-09 00:00:00'): 36.62312222222222, pd.Timestamp('2021-07-08 00:00:00'): 31.428199999999997}, 
                             'Open': {pd.Timestamp('2020-07-13 00:00:00'): 2.738235294117647, pd.Timestamp('2020-10-11 00:00:00'): 1.8931444444444445, pd.Timestamp('2021-01-09 00:00:00'): 10.917820224719101, pd.Timestamp('2021-04-09 00:00:00'): 36.484144444444446, pd.Timestamp('2021-07-08 00:00:00'): 32.269400000000005}, 
                             'High': {pd.Timestamp('2020-07-13 00:00:00'): 2.9335882352941174, pd.Timestamp('2020-10-11 00:00:00'): 2.008811111111111, pd.Timestamp('2021-01-09 00:00:00'): 11.826696629213483, pd.Timestamp('2021-04-09 00:00:00'): 38.68677777777778, pd.Timestamp('2021-07-08 00:00:00'): 32.924400000000006}, 
                             'Low': {pd.Timestamp('2020-07-13 00:00:00'): 2.5457882352941175, pd.Timestamp('2020-10-11 00:00:00'): 1.7784333333333333, pd.Timestamp('2021-01-09 00:00:00'): 10.363224719101124, pd.Timestamp('2021-04-09 00:00:00'): 34.313766666666666, pd.Timestamp('2021-07-08 00:00:00'): 30.7906}, 
                             'Vol.': {pd.Timestamp('2020-07-13 00:00:00'): 0.0, pd.Timestamp('2020-10-11 00:00:00'): 0.0, pd.Timestamp('2021-01-09 00:00:00'): 0.0, pd.Timestamp('2021-04-09 00:00:00'): 68431.0, pd.Timestamp('2021-07-08 00:00:00'): 0.0}, 
                             'Change %': {pd.Timestamp('2020-07-13 00:00:00'): 0.01686, pd.Timestamp('2020-10-11 00:00:00'): 0.00855222222222222, pd.Timestamp('2021-01-09 00:00:00'): 0.0286438202247191, pd.Timestamp('2021-04-09 00:00:00'): 0.0070688888888888884, pd.Timestamp('2021-07-08 00:00:00'): -0.024120000000000003}, 
                             'Start Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00'), pd.Timestamp('2020-10-11 00:00:00'): pd.Timestamp('2020-10-11 00:00:00'), pd.Timestamp('2021-01-09 00:00:00'): pd.Timestamp('2021-01-09 00:00:00'), pd.Timestamp('2021-04-09 00:00:00'): pd.Timestamp('2021-04-09 00:00:00'), pd.Timestamp('2021-07-08 00:00:00'): pd.Timestamp('2021-07-08 00:00:00')}, 
                             'End Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-10-11 00:00:00'), pd.Timestamp('2020-10-11 00:00:00'): pd.Timestamp('2021-01-09 00:00:00'), pd.Timestamp('2021-01-09 00:00:00'): pd.Timestamp('2021-04-09 00:00:00'), pd.Timestamp('2021-04-09 00:00:00'): pd.Timestamp('2021-07-08 00:00:00'), pd.Timestamp('2021-07-08 00:00:00'): pd.Timestamp('2021-10-06 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_5_year.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'T')
        pd.testing.assert_frame_equal(df, expected)
      
    def test_agrupate_dates_by_semester(self):
        expected_raw_dict = {'Price': {pd.Timestamp('2020-07-13 00:00:00'): 2.31824, pd.Timestamp('2021-01-09 00:00:00'): 23.980413407821228, pd.Timestamp('2021-07-08 00:00:00'): 31.428199999999997}, 
                             'Open': {pd.Timestamp('2020-07-13 00:00:00'): 2.3036171428571426, pd.Timestamp('2021-01-09 00:00:00'): 23.772396648044694, pd.Timestamp('2021-07-08 00:00:00'): 32.269400000000005}, 
                             'High': {pd.Timestamp('2020-07-13 00:00:00'): 2.4579885714285714, pd.Timestamp('2021-01-09 00:00:00'): 25.33176536312849, pd.Timestamp('2021-07-08 00:00:00'): 32.924400000000006}, 
                             'Low': {pd.Timestamp('2020-07-13 00:00:00'): 2.1511485714285716, pd.Timestamp('2021-01-09 00:00:00'): 22.405396648044693, pd.Timestamp('2021-07-08 00:00:00'): 30.7906}, 
                             'Vol.': {pd.Timestamp('2020-07-13 00:00:00'): 0.0, pd.Timestamp('2021-01-09 00:00:00'): 34406.64804469274, pd.Timestamp('2021-07-08 00:00:00'): 0.0}, 
                             'Change %': {pd.Timestamp('2020-07-13 00:00:00'): 0.01258742857142857, pd.Timestamp('2021-01-09 00:00:00'): 0.017796089385474858, pd.Timestamp('2021-07-08 00:00:00'): -0.024120000000000003}, 
                             'Start Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00'), pd.Timestamp('2021-01-09 00:00:00'): pd.Timestamp('2021-01-09 00:00:00'), pd.Timestamp('2021-07-08 00:00:00'): pd.Timestamp('2021-07-08 00:00:00')}, 
                             'End Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2021-01-09 00:00:00'), pd.Timestamp('2021-01-09 00:00:00'): pd.Timestamp('2021-07-08 00:00:00'), pd.Timestamp('2021-07-08 00:00:00'): pd.Timestamp('2022-01-04 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_5_year.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'S')
        pd.testing.assert_frame_equal(df, expected)
    
    def test_agrupate_dates_by_year(self):
        expected_raw_dict = {'Price': {pd.Timestamp('2020-07-13 00:00:00'): 13.52458774373259}, 
                             'Open': {pd.Timestamp('2020-07-13 00:00:00'): 13.425456824512533}, 
                             'High': {pd.Timestamp('2020-07-13 00:00:00'): 14.2873426183844}, 
                             'Low': {pd.Timestamp('2020-07-13 00:00:00'): 12.648941504178273}, 
                             'Vol.': {pd.Timestamp('2020-07-13 00:00:00'): 17155.40389972145}, 
                             'Change %': {pd.Timestamp('2020-07-13 00:00:00'): 0.01467325905292479}, 
                             'Start Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2020-07-13 00:00:00')}, 
                             'End Date': {pd.Timestamp('2020-07-13 00:00:00'): pd.Timestamp('2021-07-13 00:00:00')}}
        expected = pd.DataFrame(expected_raw_dict)
        expected.index.name = 'Date'
        df = pd.read_csv("..\\data\\tests\\test_5_year.csv")
        df = bs.converter_dados(df)
        df = at.agrupate_dates(df, 'Y')
        pd.testing.assert_frame_equal(df, expected)
        
    def test_error_agrupate_dates(self):
        df = pd.read_csv("..\\data\\tests\\test_1.csv")
        df = bs.converter_dados(df)
        try:
            at.agrupate_dates(df, "L")
        except ValueError:
            assert True
    
    def test_rename_columns(self):
        raw_dict = {'Date': {1:'0',2:'0',3:'0'},
                    'Col1': {1:'1',2:'1',3:'1'},
                    'Col2': {1:'2',2:'2',3:'2'},
                    'Col3': {1:'3',2:'3',3:'3'}
                    }
        df = pd.DataFrame(raw_dict)
        at.rename_columns(df,'T')
        expected = ['Date', 'Col1 T', 'Col2 T', 'Col3 T']
        real = list(df.columns)
        self.assertEqual(expected, real)

    def test_normalize_value_columns(self):
        raw_dict = {'Date':{1:'10/10',2:'11/11',3:'12/12'},
                    'Valor1':{1: 100, 2: 100,3: 100},
                    'Valor2':{1: 100, 2: 50,3: 0},
                    'Valor3':{1: 2500, 2: 250,3: 25},
                    'Valor %':{1: 0.0, 2: 0.5,3: 0.11}}
        expected_raw_dict = {'Date':{1:'10/10',2:'11/11',3:'12/12'},
                    'Valor1':{1: 1.0, 2: 1.0,3: 1.0},
                    'Valor2':{1: 1.0, 2: 0.5,3: 0.0},
                    'Valor3':{1: 1, 2: 0.1,3: 0.01},
                    'Valor %':{1: 0.0, 2: 0.5,3: 0.11}}
        real = pd.DataFrame(raw_dict)
        at.normalize_value_columns(real)
        expected = pd.DataFrame(expected_raw_dict)
        pd.testing.assert_frame_equal(real, expected)

    # Importante!
    def test_agrupate_datasets(self):
        df1_raw_dict = {'Date':{1: 0, 2: 1, 3: 2, 4: 3, 5: 4},
                        'C1':{1: "never", 2: "gonna", 3: "give", 4: "you", 5: "up"},
                        'C2':{1: "never", 2: "gonna", 3: "let", 4: "you", 5: "down "},
                        'C3':{1: "never", 2: "gonna", 3: "run", 4: "around and", 5: "desert you"},}
        df2_raw_dict = {'Date':{1: 0, 2: 1, 3: 2, 4: 3, 5: 4},
                        'C1':{1: "never", 2: "gonna", 3: "make", 4: "you", 5: "cry"},
                        'C2':{1: "never", 2: "gonna", 3: "say", 4: "goodbye"},
                        'C3':{1: "never", 2: "gonna", 3: "tell a", 4: "lie and", 5: "hurt you"}}
        df_expected_raw = {'Date': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}, 
                           'C1 Got': {0: 'never', 1: 'gonna', 2: 'give', 3: 'you', 4: 'up'}, 
                           'C2 Got': {0: 'never', 1: 'gonna', 2: 'let', 3: 'you', 4: 'down '}, 
                           'C3 Got': {0: 'never', 1: 'gonna', 2: 'run', 3: 'around and', 4: 'desert you'}, 
                           'C1 Rickrolled': {0: 'never', 1: 'gonna', 2: 'make', 3: 'you', 4: 'cry'}, 
                           'C2 Rickrolled': {0: 'never', 1: 'gonna', 2: 'say', 3: 'goodbye', 4: 0}, 
                           'C3 Rickrolled': {0: 'never', 1: 'gonna', 2: 'tell a', 3: 'lie and', 4: 'hurt you'}}
        df1 = pd.DataFrame(df1_raw_dict)
        df2 = pd.DataFrame(df2_raw_dict)
        expected = pd.DataFrame(df_expected_raw)
        df_agrupated = at.agrupate_datasets(df1,df2,"Got","Rickrolled")
        pd.testing.assert_frame_equal(df_agrupated, expected)
