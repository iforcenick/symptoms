import unittest
from main import app
import json

class TestSymSytem(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_hpo(self):
        response = self.client.get('/hpo')
        resp_data = response.get_data().decode('utf8')
        self.assertTrue(resp_data is not None)
        self.assertTrue(len(resp_data) > 0)
        json_data = json.loads(resp_data)
        self.assertTrue('id' in json_data[0])
        self.assertTrue('name' in json_data[0])
        self.assertTrue('legal_id' in json_data[0])
    
    def test_rare_conditions(self):
        data = {'hpos': '1,2'}
        response = self.client.get('/rare_conditions', query_string=data)
        resp_data = response.get_data().decode('utf8')
        self.assertTrue(resp_data is not None)
        self.assertTrue(len(resp_data) > 0)
        json_data = json.loads(resp_data)
        self.assertTrue('id' in json_data[0])
        self.assertTrue('orpha_code' in json_data[0])
        self.assertTrue('name' in json_data[0])
        self.assertTrue('expert_link' in json_data[0])
        self.assertTrue('freq' in json_data[0])
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()