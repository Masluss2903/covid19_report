import unittest
import boto3
import json
from covid.get_summary_database import get_global_summary, get_data_by_country


class My_test(unittest.TestCase):
    def setUp(self):
        with open('./tests/response.json','r') as f:
            self.covid_summary = json.load(f)

    def test_get_global_summary(self):
        self.assertEqual(get_global_summary(self.covid_summary),'Right now there are 81,849 new confirmed cases, 2,519,183 total confirmed, 6,788 new deaths, 172,976 total deaths and 679,101 total recovered.')

    def test_get_data_by_country(self):
        self.assertEqual(get_data_by_country(self.covid_summary,'mexico'),'In Mexico there are 511 new confirmed cases, 8,772 total confirmed, 26 new deaths, 712 total deaths and 2,627 total recovered.')
        self.assertEqual(get_data_by_country(self.covid_summary,'jjhl'),'Try again, we do not have what you are looking for')



if __name__ == '__main__':
    unittest.main()
