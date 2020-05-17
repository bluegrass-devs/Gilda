import io
import os
import json
import logging
import requests

from fdk import response


def handle_member_join_channel(event):
    random_channel_id = os.environ.get('random_channel_id')

    if (event["channel"] == random_channel_id):
        post_welcome(event)


def post_welcome(event):
    user_id = event['user']
    message = f"Howdy <@{user_id}> 👋🤠"

    r = requests.post(os.environ.get('webhook_url'), json={"text": message})


def handler(ctx, data: io.BytesIO=None):
    logger = logging.getLogger()
    logger.debug("------------- Launching function --------------")

    event = None
    event_response = None
    try:
        body = json.loads(data.getvalue())
        event = body.get("event")
        event_response = json.dumps({
            "token": body.get("token"),
            "challenge": body.get("challenge"),
            "type": body.get("type")
        })
    except (Exception, ValueError) as ex:
        print(str(ex))

    logger.debug(f"------------- event {event}")
    if (event["type"] == "member_joined_channel"):
        handle_member_join_channel(event)


    return response.Response(
        ctx, response_data=event_response,
        headers={"Content-Type": "application/json"}
    )
