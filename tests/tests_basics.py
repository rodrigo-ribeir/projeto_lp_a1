import __init__
import unittest
import unittest.mock
import basics as bs
import pandas as pd

class TestDataLoader(unittest.TestCase):
    def test_read_data_name(self):
        data = bs.read_data("tests\\test_1.csv")
        expected = {'Date': {0: '07/18/2010', 1: '07/19/2010',2: '07/20/2010', 3: '07/21/2010', 4: '07/22/2010'},
                    'Price': {0: "0.1", 1: "0.1", 2: "0.1", 3: "0.1", 4: "1,000.1"}, 
                    'Open': {0: "0.0", 1: "0.1", 2: "0.1", 3: "0.1", 4: "1,000.1"}, 
                    'High': {0: "0.1", 1: "0.1", 2: "0.1", 3: "0.1", 4: "1,000.1"},
                    'Low': {0: "0.1", 1: "0.1", 2: "0.1", 3: "0.1", 4: "1,00,0.1"}, 
                    'Vol.': {0: '0.0,8K', 1: '0.57M', 2: '0.26M', 3: '0.50B', 4: '2.16B'},
                    'Change %': {0: '0.00%', 1: '0.00%', 2: '0.00%', 3: '0.00%', 4: '10.00%'}}
        expected = pd.DataFrame(expected)

        pd.testing.assert_frame_equal(data, expected)
        
    def test_read_data_separator(self):
        data = bs.read_data("tests\\test_2.csv", separator=';')
        expected = {'Date': {0: '07/18/2010', 1: '07/19/2010', 2: '07/20/2010', 3: '07/21/2010', 4: '07/22/2010'}, 
                    'Price': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Open': {0: 0.0, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'High': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Low': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Vol.': {0: '0.08K', 1: '0.57K', 2: '0.26K', 3: '0.58K', 4: '2.16K'}, 
                    'Change %': {0: '0.00%', 1: '0.00%', 2: '0.00%', 3: '0.00%', 4: '0.00%'}}
        expected = pd.DataFrame(expected)
        pd.testing.assert_frame_equal(data, expected)

    def test_read_data_encode(self):
        data = bs.read_data("tests\\test_3.csv", encode="utf_16_le")
        expected = {'Date': {0: '07/18/2010', 1: '07/19/2010', 2: '07/20/2010', 3: '07/21/2010', 4: '07/22/2010'}, 
                    'Price': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Open': {0: 0.0, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'High': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Low': {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}, 
                    'Vol.': {0: '0.08K', 1: '0.57K', 2: '0.26K', 3: '0.58K', 4: '2.16K'}, 
                    'Change %': {0: '0.00%', 1: '0.00%', 2: '0.00%', 3: '0.00%', 4: '0.00%'}}
        expected = pd.DataFrame(expected)
        pd.testing.assert_frame_equal(data, expected)

    def test_error_wrong_name_read_data(self):
        try:
            self.assertRaises(FileNotFoundError, bs.read_data('teste'))
        except FileNotFoundError:
            assert True
        
    def test_permission_error_read_data(self):
        try:
            self.assertRaises(PermissionError, bs.read_data('tests'))
        except PermissionError:
            assert True

    def test_choose_dataset_return_name(self):
        name_1 = (bs.choose_dataset(1, True))[1]
        expected_1 = "Bitcoin"
        name_2 = (bs.choose_dataset(2, True))[1]
        expected_2 = "Ethereum"
        name_3 = (bs.choose_dataset(3, True))[1]
        expected_3 = "Solana"
        self.assertEqual(name_1, expected_1)
        self.assertEqual(name_2, expected_2)
        self.assertEqual(name_3, expected_3)

    @unittest.mock.patch("basics.input")
    def test_choose_dataset_return_only_dataframe(self, mock_input):
        mock_input.side_effect = ['4', 'tests\\test_1']
        df_real = bs.choose_dataset()
        df_expected = pd.read_csv("..\\data\\tests\\test_1.csv")
        pd.testing.assert_frame_equal(df_real, df_expected)
    
    @unittest.mock.patch("basics.input")
    def test_error_wrong_input_choose_dataset(self, mocked_input):
        mocked_input.side_effect = ['espero_erro']
        try:
            self.assertRaises(TypeError,bs.choose_dataset(0, False))
        except TypeError:
            assert True

    @unittest.mock.patch("basics.input")
    def test_error_invalid_number_choose_dataset(self, mocked_input):
        mocked_input.side_effect = [5]
        try:
            self.assertRaises(ValueError, bs.choose_dataset(0, False))
        except ValueError:
            assert True
    
    @unittest.mock.patch("basics.input")
    def test_choose_dataset_open_another_csv(self, mocked_input):
        mocked_input.side_effect = ['4','tests\\test_1']
        real_df, real_name = bs.choose_dataset(0, True)
        expected_df = pd.read_csv("..\\data\\tests\\test_1.csv")
        expected_name = "tests\\test_1"
        self.assertEqual(real_name, expected_name)
        pd.testing.assert_frame_equal(real_df, expected_df)
    
    def test_filtrar_colunas_two_columns(self):
        expected = {'Date': {0: '07/18/2010', 1: '07/19/2010',2: '07/20/2010', 3: '07/21/2010', 4: '07/22/2010'},
                    'Price': {0: "0.1", 1: "0.1", 2: "0.1", 3: "0.1", 4: "1,000.1"}}
        expected = pd.DataFrame(expected)
        foo = pd.read_csv("..\\data\\tests\\test_1.csv")
        real = bs.filtrar_colunas(foo, ['Date', 'Price'])
        pd.testing.assert_frame_equal(expected, real)
    
    def test_filtrar_colunas_vol_na(self):
        raw_dict = {'Data': {1: 1, 2: 2, 3: 3, 4: 4},
                    'Vol.': {1: pd.NA,2: 1, 3: '1K', 4: '1M', 5: '1B' }}
        expected_raw_dict ={'Data': {1: 1, 2: 2, 3: 3, 4: 4},
                            'Vol.': {1: 0,2: 1, 3: 1000, 4: 1000000, 5: 1000000000 }}
        real_df = bs.converter_dados(pd.DataFrame(raw_dict))
        expected_df = pd.DataFrame(expected_raw_dict)
        pd.testing.assert_frame_equal(real_df, expected_df)

    def test_error_filtrar_colunas_wrong_columns(self):
        df = pd.read_csv("..\\data\\tests\\test_1.csv")
        coluna = ['Coluna']
        try:
            bs.filtrar_colunas(df,coluna)
        except ValueError:
            assert True
    
    def test_converter_dados_values_columns(self):
        test_1 = pd.read_csv("..\\data\\tests\\test_1.csv")
        test_1_c = bs.converter_dados(test_1)
        Prices = pd.Series([0.1,0.1,0.1,0.1, 1_000.1], name='Price')
        Opens = pd.Series([0.0, 0.1, 0.1, 0.1, 1_000.1], name='Open')
        Highs = pd.Series([0.1, 0.1, 0.1, 0.1, 1_000.1], name='High')
        Lows = pd.Series([0.1, 0.1, 0.1, 0.1, 1_000.1], name='Low')
        
        pd.testing.assert_series_equal(test_1_c['Price'], Prices)
        pd.testing.assert_series_equal(test_1_c['Open'], Opens)
        pd.testing.assert_series_equal(test_1_c['High'], Highs)
        pd.testing.assert_series_equal(test_1_c['Low'], Lows)
    
    def test_converter_dados_amount_columns(self):
        test_1 = pd.read_csv("..\\data\\tests\\test_1.csv")
        vol_real = bs.converter_dados(test_1)['Vol.']
        change_real = bs.converter_dados(test_1)['Change %']
        vols = pd.Series([80.0, 570_000.0, 260_000.0, 500_000_000.0, 2_160_000_000.0], name="Vol.")
        changes = pd.Series([0.0, 0.0, 0.0, 0.0, 0.001], name = "Change %")

        pd.testing.assert_series_equal(vol_real, vols)
        pd.testing.assert_series_equal(change_real, changes)
        
    def test_converter_dados_date_column(self):
        test_1 = pd.read_csv("..\\data\\tests\\test_1.csv")
        real_dates = bs.converter_dados(test_1)['Date']
        dates = pd.Series(["07/18/2010","07/19/2010","07/20/2010","07/21/2010","07/22/2010"], name='Date')
        dates_pd = pd.to_datetime(dates)
        pd.testing.assert_series_equal(real_dates, dates_pd)
