import unittest
from unittest.mock import patch
from OTX_Collector import get_OTX_data
from datetime import datetime 

class TestOTXCollector(unittest.TestCase):

    #Checks if get_OTX_data returns a list
    @patch("OTX_Collector.otx_Key")
    def test_get_OTX_data_return_list(self, mock_otx):
        mock_otx.getall.return_value = [
            {
                "name": "Test Pulse",
                "TLP": "red",
                "modified": "2024-01-15T10:30:00",
                "indicators": [
                    {"type": "IPv4", "indicator": "185.220.101.5"}
                ]
            }
        ]

        result = get_OTX_data()
        self.assertIsInstance(result, list)

    #Checks if get_OTX_data returns a list of dict with the correct keys
    @patch("OTX_Collector.otx_Key")
    def test_get_OTX_has_correct_keys(self, mock_otx):
        mock_otx.getall.return_value = [
            {
                "name": "Test Pulse",
                "TLP": "red",
                "modified": "2024-01-15T10:30:00",
                "indicators": [
                    {"type": "IPv4", "indicator": "185.220.101.5"}
                ]
            }
        ]

        result = get_OTX_data()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        expected_keys = {"type", "value", "source", "severity", "timestamp"}

        for indicator in result:
            self.assertIsInstance(indicator, dict)
            self.assertTrue(
                expected_keys.issubset(indicator.keys()),
                f"Missing Keys: {expected_keys - indicator.keys()}"
            )
    
    ##Checks if get_OTX_data returns a value since it shopld never be None
    @patch("OTX_Collector.otx_Key")
    def test_no_empty_values(self, mock_otx):
        mock_otx.getall.return_value = [
            {
                "name": "Test Pulse",
                "TLP": "red",
                "modified": "2024-01-15T10:30:00",
                "indicators": [
                    {"type": "IPv4", "indicator": "185.220.101.5"},
                    {"type": "FileHash-MD5", "indicator": "abc123"}
                ]
            }
        ]

        result = get_OTX_data()

        for ioc in result:
            self.assertIsNotNone(ioc["value"])
            self.assertNotEqual(ioc["value"], "")

    #Checks if timestamp is a datetime object
    @patch("OTX_Collector.otx_Key")
    def test_timestamp_is_datetime(self, mock_otx):
        mock_otx.getall.return_value = [
            {
                "name": "Test Pulse",
                "TLP": "red",
                "modified": "2024-01-15T10:30:00",
                "indicators": [
                    {"type": "IPv4", "indicator": "185.220.101.5"}
                ]
            }
        ]

        result = get_OTX_data()

        for ioc in result:
            self.assertIsInstance(ioc["timestamp"], datetime)

    #checks what happens if it gets an empty pulse
    @patch("OTX_Collector.otx_Key")
    def test_empty_pulse_list(self, mock_otx):
        mock_otx.getall.return_value = []

        result = get_OTX_data()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    #Tests what happens when theres a pules with no indicators
    @patch("OTX_Collector.otx_Key")
    def test_pulse_with_no_indicators(self, mock_otx):
        mock_otx.getall.return_value = [
            {
                "name": "Empty Pulse",
                "TLP": "white",
                "modified": "2024-01-15T10:30:00",
                "indicators": []
            }
        ]

        result = get_OTX_data()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    


        