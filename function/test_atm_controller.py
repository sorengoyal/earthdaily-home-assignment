import base64
import json
from datetime import datetime
import unittest
from unittest.mock import MagicMock


from uuid import UUID

from function.atm_function import AtmModel, AtmService, AtmController


class TestAtmController(unittest.TestCase):
    UUID_STR = 'eb1e0c98-f05b-4742-9c4d-a469415b684d'
    ADDRESS = "3588 Crowley Dr"
    PROVIDER = "TD"
    RATING_STR = "5.0"
    CREATED_ON_STR = '2023-04-24 17:14:20.782652'
    mock_atm_service = AtmService(None)
    class_under_test = AtmController(mock_atm_service)

    def test_get_200(self):
        # Arrange
        event = {
            "pathParameters": {"atm_id": self.UUID_STR}
        }
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        expected_response = self.class_under_test.responseSuccess(200, atm)
        self.mock_atm_service.getById = MagicMock(return_value=(atm, None))

        # Act
        result = self.class_under_test.get(event, None)

        # Assert
        self.assertEqual(expected_response, result)

    def test_post_200(self):
        # Arrange
        '''
        ASCII representation of the base64 encoded body
        {
            "address": "3588 Crowley Dr",
            "provider": "TD",
            "rating": 5.0
        }
        '''
        event = {
            "body": "ewogICAgImFkZHJlc3MiOiAiMzU4OCBDcm93bGV5IERyIiwKICAgICJwcm92aWRlciI6ICJURCIsCiAgICAicmF0aW5nIjogNS4wCn0="
        }
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        expected_response = self.class_under_test.responseSuccess(200, atm)
        self.mock_atm_service.create = MagicMock(return_value=(atm, None))

        # Act
        result = self.class_under_test.post(event, None)

        # Assert
        self.assertEqual(expected_response, result)

    def test_put_200(self):
        # Arrange
        '''
        ASCII representation of the base64 encoded body
        {
            "address": "3588 Crowley Dr",
            "provider": "TD",
            "rating": 5.0
        }
        '''
        event = {
            "body": "ewogICAgImFkZHJlc3MiOiAiMzU4OCBDcm93bGV5IERyIiwKICAgICJwcm92aWRlciI6ICJURCIsCiAgICAicmF0aW5nIjogNS4wCn0=",
            "pathParameters": {"atm_id": self.UUID_STR}

        }
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        expected_response = self.class_under_test.responseSuccess(200, atm)
        self.mock_atm_service.update = MagicMock(return_value=(atm, None))

        # Act
        result = self.class_under_test.put(event, None)

        # Assert
        self.assertEqual(expected_response, result)



