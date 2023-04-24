import boto3
import json
import base64

print('Loading function')
dynamo = boto3.client('dynamodb')


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
    payload = json.loads(base64.b64decode(event['body']).decode('utf-8'))
    response = dynamo.put_item(TableName='EarthdailyAtmStack-AtmDB-ZY0LE9NKVG3H',
                    Item={
                        'id': {
                            'S': payload['id'],
                        },
                        'address': {
                            'S': payload['address'],
                        },
                        'provider': {
                            'S': payload['provider'],
                        },
                        'rating': {
                            'N': str(payload['rating']),
                        }
                    }
                    )
    return respond(None, response)



