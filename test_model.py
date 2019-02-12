import pandas as pd
from pandas.util.testing import assert_frame_equal

import unittest
from unittest.mock import patch, mock_open

from model import get_total_by_instrument, get_total_by_sector, get_latest_data


SAMPLE = """[{"value": 124421854.35, "date": "2018-09-01T00:00:00", "series_id": "SF117725", "original_title": "UDIBONOS En Poder de Residentes en el Pa\u00eds Sector P\u00fablico", "instrument_type": "UDIBONOS", "short_name": "Public Sector"},{"value": 121138203.12, "date": "2018-10-01T00:00:00", "series_id": "SF117725", "original_title": "UDIBONOS En Poder de Residentes en el Pa\u00eds Sector P\u00fablico", "instrument_type": "UDIBONOS", "short_name": "Public Sector"}]"""


class TestGetLatestData(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data=SAMPLE))
    def test_get_latest_data(self):
        df = get_latest_data()

        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['value'], 124421854.35)
        self.assertEqual(df.iloc[1]['value'], 121138203.12)
        self.assertEqual(df.iloc[1]['short_name'], "Public Sector")



class TestTransformations(unittest.TestCase):

    def setUp(self):
        self.sample1 = pd.DataFrame([
            {
                "date": "2018-10-01T00:00:00",
                "instrument_type": "UDIBONOS",
                "short_name": "Foreign Direct Investment",                
                "value": 10.,
            },
            {
                "date": "2018-10-01T00:00:00",
                "instrument_type": "BONOS",
                "short_name": "Banco de Mexico",                
                "value": 5.,
            },            
            {
                "date": "2018-11-01T00:00:00",
                "instrument_type": "UDIBONOS",
                "short_name": "Foreign Direct Investment",
                "value": 20.,
            },
            {
                "date": "2018-11-01T00:00:00",
                "instrument_type": "UDIBONOS",
                "short_name": "Banco de Mexico",
                "value": 20.,
            },            
            {
                "date": "2018-11-01T00:00:00",
                "instrument_type": "CETES",
                "short_name": "Banco de Mexico",                
                "value": 30.,
            }            
        ])
    
    @patch('model.get_latest_data')
    def test_total_by_instrument(self, mock_get_data):
        mock_get_data.return_value = self.sample1

        df = get_total_by_instrument()

        expected_df = pd.DataFrame(
            [[5., None, 10.], [None, 30., 40.]],
            columns=pd.Series(['BONOS', 'CETES', 'UDIBONOS'], name='instrument_type')
        )

        expected_df.index = pd.Series(
            ["2018-10-01T00:00:00", "2018-11-01T00:00:00"],
            name='date'
        )

        assert_frame_equal(df, expected_df)


    @patch('model.get_latest_data')
    def test_total_by_sector_unfiltered(self, mock_get_data):
        mock_get_data.return_value = self.sample1

        df = get_total_by_sector()

        expected_df = pd.DataFrame(
            [[5., 10.], [50., 20.]],
            columns=pd.Series(
                ['Banco de Mexico', 'Foreign Direct Investment'],
                name='short_name'
            )
        )

        expected_df.index = pd.Series(
            ["2018-10-01T00:00:00", "2018-11-01T00:00:00"],
            name='date'
        )

        assert_frame_equal(df, expected_df)


    @patch('model.get_latest_data')
    def test_total_by_sector_single_filter(self, mock_get_data):
        mock_get_data.return_value = self.sample1

        df = get_total_by_sector(("UDIBONOS",))

        expected_df = pd.DataFrame(
            [[None, 10.], [20., 20.]],
            columns=pd.Series(
                ['Banco de Mexico', 'Foreign Direct Investment'],
                name='short_name'
            )
        )

        expected_df.index = pd.Series(
            ["2018-10-01T00:00:00", "2018-11-01T00:00:00"],
            name='date'
        )

        assert_frame_equal(df, expected_df)


    @patch('model.get_latest_data')
    def test_total_by_sector_multi_filter(self, mock_get_data):
        mock_get_data.return_value = self.sample1

        df = get_total_by_sector(("UDIBONOS", "CETES",))

        expected_df = pd.DataFrame(
            [[None, 10.], [50., 20.]],
            columns=pd.Series(
                ['Banco de Mexico', 'Foreign Direct Investment'],
                name='short_name'
            )
        )

        expected_df.index = pd.Series(
            ["2018-10-01T00:00:00", "2018-11-01T00:00:00"],
            name='date'
        )

        assert_frame_equal(df, expected_df)                        

        
if __name__ == "__main__":
    unittest.main()
