from datetime import datetime
from typing import Dict

import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')
class AtmModel:
    def __init__(self, id: int, address: str, provider: str, rating: float, created_on: datetime):
        self.id = id
        self.address = address
        self.provider = provider
        self.rating = rating
        self.created_on = created_on

    def __init__(self, json_model: Dict):
        self.id = json_model["id"]
        self.address = json_model["address"]
        self.provider = json_model["provider"]
        self.rating = json_model["rating"]
        self.created_on = json_model["created_on"]

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }



def handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))
    response = dynamo.get_item(TableName='EarthdailyAtmStack-AtmDB-ZY0LE9NKVG3H',
                           Key={
                               'id': {
                                   'S': '1'
                                }
                           })

    return respond(None, response)



