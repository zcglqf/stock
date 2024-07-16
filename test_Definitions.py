import unittest
import copy
from Definitions import DataRequestInfo, RequestInfoDataType

class Test_DataRequestInfo(unittest.TestCase):
    # Request: In the initialization, all defined fields must be specified, missing or adding fields not allowed.
    def test_initialization(self):
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        data = DataRequestInfo( RequestInfo)
        self.assertEqual(data.keys(), RequestInfoDataType.keys())

        # Error if missing a field.
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        del RequestInfo['Curve']
        with self.assertRaises(KeyError):
            data = DataRequestInfo(RequestInfo)

        # Error if found unknown field.
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        RequestInfo['ShouldNotBeHere'] = None
        with self.assertRaises(KeyError):
            data = DataRequestInfo(RequestInfo)

    # Request: update of predefined field is allowed; seting of undefined field is not allowed.   
    def test_set_field(self):
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        data = DataRequestInfo(RequestInfo)

        data['ID'] = 'ABCDEF'
        self.assertEqual('ABCDEF', data['ID'])

        with self.assertRaises(KeyError):
            data['IIDD'] = 'ABCDEF'

    # Request: Field name to be updated should be pre-defined, otherwise not allowed.
    def test_update_field(self):
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        data = DataRequestInfo(RequestInfo)
        data.update({'ID': 'ABCDEF', 'EnglishName': 'ABCDEF'})
        self.assertEqual('ABCDEF', data['ID'])
        self.assertEqual('ABCDEF', data['EnglishName'])

        with self.assertRaises(KeyError):
            data.update({'ID': 'ABCDEF', 'UnknownName': 'ABCDEF'})


    def test_unlock(self):
        RequestInfo = copy.deepcopy(RequestInfoDataType)
        data = DataRequestInfo(RequestInfo)
        data.unlock()
        data['WhatEverField'] = 'Whatever'
        self.assertEqual('Whatever', data['WhatEverField'])

        data.update({'ID': 'ABCDEF', 'UnknownName': 'ABCDEF'})
        self.assertEqual('ABCDEF', data['UnknownName'])

if __name__ == '__main__':
    unittest.main()