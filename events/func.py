import io
import os
import json
import logging
import requests

from fdk import response

local_dev = os.environ.get('is_local')
logger = logging.getLogger()


def handle_member_join_channel(event):
    random_channel_id = os.environ.get('random_channel_id')

    if (event["channel"] == random_channel_id):
        post_welcome(event)


def post_welcome(event):
    user_id = event['user']
    message = f"Howdy <@{user_id}> 👋🤠"
    webhook_url = os.environ.get('webhook_url')

    if not local_dev:
        requests.post(webhook_url, json={"text": message})
    else:
        logger.debug(f"------------- posting {message} to url {webhook_url}")


def handler(ctx, data: io.BytesIO = None):
    logger.debug("------------- Launching function --------------")

    event = None
    event_response = None
    try:
        body = json.loads(data.getvalue())
        event = body.get("event")
        event_response = json.dumps({
            "challenge": body.get("challenge")
        })
    except (Exception, ValueError) as ex:
        print(str(ex))

    if event:
        logger.debug(f"------------- event {event}")
        if (event["type"] == "member_joined_channel"):
            handle_member_join_channel(event)

    return response.Response(
        ctx, response_data=event_response,
        headers={"Content-Type": "application/json"}
    )
