from typing import Iterator
from free_example import free_games
import json
import boto3
import os
from boto3.dynamodb.conditions import Key

ddb_client = boto3.resource('dynamodb')
ses_client = boto3.client("ses")
FROM = "me@sygi.xyz"
TO = "sygnowski+free_epic@gmail.com"

def notify(game, url, description=None):
    title = f"New free game: {game}"
    content = f"<p>Link: {url}</p>"
    if description is not None:
        content = f"<p>{description}</p>" + content
    print(f"sending email about {game}")
    response = ses_client.send_email(
        Source=FROM,
        Destination=dict(ToAddresses=[TO]),
        Message=dict(
            Subject=dict(Data=title),
            Body=dict(Html=dict(Data=content))
        ))

def process_free_games():
    for game, url, desc in free_games():
        table = ddb_client.Table(os.environ.get("TABLE_NAME"))
        item = table.get_item(Key={'title': game})
        if not "Item" in item:
            notify(game, url, desc)
            table.put_item(Item={'title': game})
            yield game

def lambda_handler(event, context):
    added = list(process_free_games())
    return {
        'statusCode': 200,
        'body': json.dumps(added)
    }
