import base64
from datetime import datetime
from typing import Dict

import boto3
import json
from uuid import UUID, uuid4

# TODO: Move to models/atm_model
class AtmModel:
    def __init__(self, id: UUID, address: str, provider: str, rating: float, created_on: datetime):
        self.id = id
        self.address = address
        self.provider = provider
        self.rating = rating
        self.created_on = created_on

    @classmethod
    def from_ddb_item(cls, ddb_item):
        id = UUID(ddb_item["id"]["S"])
        address = ddb_item["address"]["S"]
        provider = ddb_item["provider"]["S"]
        rating = float(ddb_item["rating"]["N"])
        created_on = datetime.strptime(ddb_item["created_on"]["S"], "%Y-%m-%d %H:%M:%S.%f")
        return cls(id, address, provider,rating, created_on)

    def to_dict(self):
        return {
            'id': str(self.id),
            'address': self.address,
            'provider': self.provider,
            'rating': str(self.rating),
            'created_on': str(self.created_on)
        }

    def to_ddbItem(self):
        return {
            'id': {'S': str(self.id)},
            'address': {'S': self.address},
            'provider': {'S': self.provider},
            'rating': {'N': str(self.rating)},
            'created_on': {'S': str(self.created_on)}
        }
class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message

# TODO: Move to repositories/atm_repository
class AtmRepository:
    TABLE_NAME = 'EarthdailyAtmStack-AtmDB-ZY0LE9NKVG3H'

    def create(self, atm: AtmModel) -> AtmModel:
        print("In AtmRepository Create")
        atm.id = uuid4()
        atm.created_on = datetime.now()
        response = self._dynamo_client.put_item(
            TableName=self.TABLE_NAME,
            Item=atm.to_ddbItem()
        )
        if response['ResponseMetadata']['HTTPStatusCode'] >= 300:
            print(response)
            return None
        print(atm)
        return atm

    def read(self, id: UUID) -> AtmModel:
        response = self._dynamo_client.get_item(TableName=self.TABLE_NAME,
                                                Key=self._create_key(str(id)))
        if "Item" not in response:
            return None
        return AtmModel.from_ddb_item(response["Item"])


    def update(self, atm: AtmModel):
        pass

    def delete(self, id: str):
        pass

    def _create_key(self, id: str):
        return {
            'id': {
                'S': id
            }
        }

    def __init__(self, ddb_client):
        self._dynamo_client = ddb_client

class AtmService:
    def create(self, address: str, provider: str, rating: float) -> (AtmModel, Error):
        print("In AtmService Create")
        atm = AtmModel(None, address, provider, rating, None)
        atm_with_id = self._atm_repository.create(atm)
        if atm_with_id == None:
            return None, Error(500, "Unable to create item")
        print(atm_with_id)
        return atm_with_id, None

    def getById(self, id: UUID) -> (AtmModel, Error):
        atm = self._atm_repository.read(id)
        if atm == None:
            return None, Error(404,  "No Item exists for id: %d" % (id))
        return atm, None

    def update(self ):
        pass

    def __init__(self, atm_repository: AtmRepository):
        self._atm_repository = atm_repository

class AtmController:

    def get(self, event, context) -> Dict:
        id = event['pathParameters']['atm_id']
        atm, error = self._atm_service.getById(id)
        if error:
            return self.responseError(400, "No Item exists for id: %d" % (id))
        return self.responseSuccess(200, atm)

    def post(self, event, context):
        # TODO: Add Validations
        body = json.loads(base64.b64decode(event['body']).decode('utf-8'))
        atm, error = self._atm_service.create(
            address=body["address"],
            provider=body["provider"],
            rating=float(body["rating"])
        )
        if error:
            return self.responseError(error.code, error.message)
        print(atm)
        return self.responseSuccess(200, atm)

    def put(self, event, context):
        pass

    def __init__(self, atm_service: AtmService):
        self._atm_service = atm_service

    def responseSuccess(self, statusCode: int, atm_model: AtmModel):
        return {
            'statusCode': str(statusCode),
            'body': json.dumps(atm_model.to_dict()),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    def responseError(self, statusCode: int, message: str):
        return {
            'statusCode': str(statusCode),
            'body': message,
            'headers': {
                'Content-Type': 'application/json',
            },
        }


def handler(event, context):
    # Intialization:
    # TODO: Offload to a DI framework
    ddb_client = boto3.client('dynamodb')
    atm_repository = AtmRepository(ddb_client)
    atm_service = AtmService(atm_repository)
    atm_controller = AtmController(atm_service)

    operation = event['httpMethod']
    print(event)
    response = None
    if operation == 'GET':
        response = atm_controller.get(event, context)
    elif operation == 'POST':
        response = atm_controller.post(event, context)
    elif operation == 'PUT':
        response = atm_controller.put(event, context)
    else:
        response = "NOT Supported"

    return response



