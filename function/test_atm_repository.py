import unittest
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import boto3

from function.atm_function import AtmRepository, AtmModel


class TestAtmRepository(unittest.TestCase):
    UUID_STR = 'eb1e0c98-f05b-4742-9c4d-a469415b684d'
    ADDRESS = "3588 Crowley Dr"
    PROVIDER = "TD"
    RATING_STR = "5.0"
    CREATED_ON_STR = '2023-04-24 17:14:20.782652'
    mock_ddb_client = boto3.client('dynamodb')
    class_under_test = AtmRepository(mock_ddb_client)

    def test_create_successful(self):
        # Arrange
        CREATE_ATM_MODEL = AtmModel(None, self.ADDRESS, self.PROVIDER, float(self.RATING_STR), None)
        response = {
            'ConsumedCapacity': {
                'CapacityUnits': 1,
                'TableName': 'Music',
            },
            "ResponseMetadata": {
                "RequestId": "LEQEDJF51JB0NB0PVLR7SNU3LFVV4KQNSO5AEMVJF66Q9ASUAAJG",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "server": "Server",
                    "date": "Tue, 25 Apr 2023 04:38:39 GMT",
                    "content-type": "application/x-amz-json-1.0",
                    "content-length": "2",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "LEQEDJF51JB0NB0PVLR7SNU3LFVV4KQNSO5AEMVJF66Q9ASUAAJG",
                    "x-amz-crc32": "2745614147"
                },
                "RetryAttempts": 0
            }
        }
        self.mock_ddb_client.put_item = MagicMock(return_value = response)

        # Act
        result = self.class_under_test.create(CREATE_ATM_MODEL)

        # Assert
        self.assertTrue(result.id is not None)
        self.assertTrue(result.created_on is not None)

    def test_get_successful(self):
        # Arrange
        response = {
            "Item": {
                "id": {"S": self.UUID_STR},
                "provider": {"S": self.PROVIDER},
                "address": {"S": self.ADDRESS},
                "rating": {"N": self.RATING_STR},
                "created_on": {"S": self.CREATED_ON_STR}
            },
            "ResponseMetadata": {
                "RequestId": "EUHH1L60IFNGI7SGD7D4ERRGIBVV4KQNSO5AEMVJF66Q9ASUAAJG",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "server": "Server",
                    "date": "Tue, 25 Apr 2023 05:01:37 GMT",
                    "content-type": "application/x-amz-json-1.0",
                    "content-length": "102",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "EUHH1L60IFNGI7SGD7D4ERRGIBVV4KQNSO5AEMVJF66Q9ASUAAJG",
                    "x-amz-crc32": "3977540516"
                },
                "RetryAttempts": 0
            }
        }
        self.mock_ddb_client.get_item = MagicMock(return_value=response)

        # Act
        result = self.class_under_test.read(UUID(self.UUID_STR))

        # Assert
        self.assertEqual(self.UUID_STR, str(result.id))
        self.assertEqual(self.PROVIDER, result.provider)
        self.assertEqual(self.ADDRESS, result.address)
        self.assertEqual(self.RATING_STR, str(result.rating))
        self.assertEqual(self.CREATED_ON_STR, str(result.created_on))

    def test_update_successful(self):
        # Arrange
        response = {
            "Attributes": {
                "id": {"S": self.UUID_STR},
                "provider": {"S": self.PROVIDER + "_updated"},
                "address": {"S": self.ADDRESS + "_updated"},
                "rating": {"N": self.RATING_STR + "99"},
                "created_on": {"S": self.CREATED_ON_STR}
            },
            "ResponseMetadata": {
                "RequestId": "EUHH1L60IFNGI7SGD7D4ERRGIBVV4KQNSO5AEMVJF66Q9ASUAAJG",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "server": "Server",
                    "date": "Tue, 25 Apr 2023 05:01:37 GMT",
                    "content-type": "application/x-amz-json-1.0",
                    "content-length": "102",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "EUHH1L60IFNGI7SGD7D4ERRGIBVV4KQNSO5AEMVJF66Q9ASUAAJG",
                    "x-amz-crc32": "3977540516"
                },
                "RetryAttempts": 0
            }
        }
        self.mock_ddb_client.update_item = MagicMock(return_value=response)
        parameters = {
            AtmModel.FIELD_ADDRESS: self.ADDRESS,
            AtmModel.FIELD_PROVIDER: self.PROVIDER,
            AtmModel.FIELD_RATING: self.RATING_STR,
        }

        # Act
        result = self.class_under_test.update(UUID(self.UUID_STR), parameters)

        # Assert
        self.assertEqual(self.UUID_STR, str(result.id))
        self.assertEqual(self.PROVIDER+"_updated", result.provider)
        self.assertEqual(self.ADDRESS+"_updated", result.address)
        self.assertEqual(self.RATING_STR+"99", str(result.rating))
        self.assertEqual(self.CREATED_ON_STR, str(result.created_on))
