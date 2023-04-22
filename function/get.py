import boto3
import json

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
    payload = json.loads(event['body'])
    payload["SourceLambda"] = "GET"
    return respond(None, payload)



