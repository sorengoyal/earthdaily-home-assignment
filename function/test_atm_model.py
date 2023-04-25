from datetime import datetime
from uuid import UUID, uuid4

from function.atm_function import AtmModel

import unittest

class TestAtmModel(unittest.TestCase):

    UUID_STR = 'eb1e0c98-f05b-4742-9c4d-a469415b684d'
    ADDRESS = "3588 Crowley Dr"
    PROVIDER = "TD"
    RATING_STR = "5.0"
    CREATED_ON_STR = '2023-04-24 17:14:20.782652'

    def test_to_dict(self):
        # Arrange
        id, created_on = uuid4(), datetime.now()
        atm_model = AtmModel(id=id,
                             address=self.ADDRESS,
                             provider=self.PROVIDER,
                             rating=float(self.RATING_STR),
                             created_on=created_on)

        # Act
        result = atm_model.to_dict()

        # Assert
        self.assertEqual(result["id"], str(id))
        self.assertEqual(result["address"], self.ADDRESS)
        self.assertEqual(result["provider"], self.PROVIDER)
        self.assertEqual(result["rating"], self.RATING_STR)
        self.assertEqual(result["created_on"], str(created_on))

    def test_to_ddbitem(self):
        # Arrange
        id, created_on = uuid4(), datetime.now()
        atm_model = AtmModel(id=id,
                             address=self.ADDRESS,
                             provider=self.PROVIDER,
                             rating=float(self.RATING_STR),
                             created_on=created_on)

        # Act
        result = atm_model.to_ddbItem()

        # Assert
        self.assertEqual(str(id), result["id"]["S"])
        self.assertEqual(self.ADDRESS, result["address"]["S"])
        self.assertEqual(self.PROVIDER, result["provider"]["S"],)
        self.assertEqual(self.RATING_STR, result["rating"]["N"], )
        self.assertEqual(str(created_on), result["created_on"]["S"],)

    def test_from_ddb_item(self):
        # Arrange
        item = {
                'id': {'S': self.UUID_STR},
                'address': {'S': self.ADDRESS},
                'provider': {'S': self.PROVIDER},
                'rating': {'N': self.RATING_STR},
                'created_on': {'S': str(self.CREATED_ON_STR)}
        }

        #Act
        atm_model = AtmModel.from_ddb_item(item)

        # Assert
        self.assertEqual(atm_model.id, UUID(self.UUID_STR))
        self.assertEqual(atm_model.address, self.ADDRESS)
        self.assertEqual(atm_model.provider, self.PROVIDER)
        self.assertEqual(atm_model.rating, float(self.RATING_STR))
        self.assertEqual(atm_model.created_on, datetime.strptime(self.CREATED_ON_STR, "%Y-%m-%d %H:%M:%S.%f"))



if __name__ == '__main__':
    unittest.main()