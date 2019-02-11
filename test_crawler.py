import unittest
from unittest.mock import patch

from crawler import chunk, parse_records


class TestUtils(unittest.TestCase):
    def test_chunk_small_list(self):
        chunks = chunk(range(8), 10)
        self.assertEqual(list(chunks), [range(8)])

    def test_chunk_long_list(self):
        chunks = chunk(range(12), 10)
        self.assertEqual(list(chunks), [range(10), range(10,12)])

    def test_chunk_long_list_even(self):
        chunks = chunk(range(20), 10)
        self.assertEqual(list(chunks), [range(10), range(10,20)])

    def test_chunk_very_long_list(self):
        chunks = chunk(range(1000000000), 10)
        current_chunk = next(chunks)
        self.assertEqual(current_chunk, range(10))
        current_chunk = next(chunks)
        self.assertEqual(current_chunk, range(10, 20))
        current_chunk = next(chunks)
        self.assertEqual(current_chunk, range(20, 30))        


class TestParser(unittest.TestCase):
    def test_parse_records(self):
        sample = {'bmx':
                       {'series': [
                           {'datos': [
                               {'dato': '9.00', 'fecha': '01/09/2018'},
                               {'dato': '10.00', 'fecha': '01/10/2018'},
                               {'dato': '11.00', 'fecha': '01/11/2018'},
                               {'dato': '12.00', 'fecha': '01/12/2018'}
                           ],
                            'idSerie': 'SF9739',
                            'titulo': 'Banco de México Inversión neta en UDIBONOS'},
                           {'datos': [
                               {'dato': '0.0', 'fecha': '01/09/2018'},
                               {'dato': '0.0', 'fecha': '01/10/2018'},
                               {'dato': '0.0', 'fecha': '01/11/2018'},
                               {'dato': '0.0', 'fecha': '01/12/2018'},
                           ],
                            'idSerie': 'SF18569',
                            'titulo': 'BANCO DE MEXICO INVERSION NETA EN BONOS A PLAZO'}
                       ]}
        }        
        records = parse_records(sample)
        expected_records = [{
                'value': float(i),
                'date': '2018-%s-01T00:00:00' % str(i).zfill(2),
                'series_id': 'SF9739',
                'original_title': 'Banco de México Inversión neta en UDIBONOS',
                'instrument_type': 'UDIBONOS',
                'short_name': 'Banco de Mexico',
            } for i in range(9, 13)] + [{
                'value': 0.0,
                'date': '2018-%s-01T00:00:00' % str(i).zfill(2),
                'series_id': 'SF18569',
                'original_title': 'BANCO DE MEXICO INVERSION NETA EN BONOS A PLAZO',
                'instrument_type': 'BONOS',
                'short_name': 'Banco de Mexico',
            } for i in range(9, 13)]

        self.assertEqual(records, expected_records)
        
        
if __name__ == "__main__":
    unittest.main()
