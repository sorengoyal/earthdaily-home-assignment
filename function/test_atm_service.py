from datetime import datetime
import unittest
from unittest.mock import MagicMock
from uuid import UUID

from function.atm_function import AtmRepository, AtmModel, AtmService


class TestAtmService(unittest.TestCase):
    UUID_STR = 'eb1e0c98-f05b-4742-9c4d-a469415b684d'
    ADDRESS = "3588 Crowley Dr"
    PROVIDER = "TD"
    RATING_STR = "5.0"
    CREATED_ON_STR = '2023-04-24 17:14:20.782652'
    mock_atm_repository = AtmRepository(None)
    class_under_test = AtmService(mock_atm_repository)

    def test_create_successful(self):
        # Arrange
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        self.mock_atm_repository.create = MagicMock(return_value=atm)

        # Act
        result, error = self.class_under_test.create(self.ADDRESS, self.PROVIDER, float(self.RATING_STR))

        # Assert
        self.assertIsNone(error)
        self.assertTrue(atm, result)

    def test_getById_successful(self):
        # Arrange
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        self.mock_atm_repository.read = MagicMock(return_value=atm)

        # Act
        result, error = self.class_under_test.getById(UUID(self.UUID_STR))

        # Assert
        self.assertIsNone(error)
        self.assertTrue(atm, result)

    def test_update_successful(self):
        # Arrange
        created_on = datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f")
        atm = AtmModel(UUID(self.UUID_STR), self.ADDRESS, self.PROVIDER, float(self.RATING_STR), created_on)
        self.mock_atm_repository.update = MagicMock(return_value=atm)
        parameters = {}
        # Act
        result, error = self.class_under_test.update(UUID(self.UUID_STR), parameters)

        # Assert
        self.assertIsNone(error)
        self.assertTrue(atm, result)



