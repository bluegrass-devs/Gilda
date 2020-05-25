import datetime
import io
import os
import json
import logging
import requests
import uuid

import asyncio
import fdk
import oci

from fdk import response
from slack import WebClient
from slack.errors import SlackApiError

local_dev = os.environ.get('is_local')
compartment_id = os.environ.get('compartment_id')
slack_bot_token = os.environ.get('slack_bot_token')
welcome_channel = os.environ.get('slack_welcome_channel')

FORMAT = '%(asctime)s -- %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()

TABLE_NAME = "slack_events"

slack_client = WebClient(token=slack_bot_token, run_async=True)


def should_post_message(oci_client, event):
    should_post = False

    details = oci.nosql.models.QueryDetails(
        compartment_id=compartment_id,
        statement=f"SELECT * FROM {TABLE_NAME} e where e.event_type = 'member_joined_channel' AND e.data.user = '{event['user']}'"
    )

    try:
        query_resp = oci_client.query(limit=1, query_details=details)
        if len(query_resp.data.items) == 0:
            should_post = True
    except Exception as ex:
        should_post = False
        logger.error(f"error: {str(ex)}")

    return should_post


def update_db(oci_client, event):
    try:
        row = oci.nosql.models.UpdateRowDetails(
            compartment_id=compartment_id,
            value={
                "uuid": str(uuid.uuid4()),
                "last_posted_at": datetime.datetime.now(),
                "event_type": event["type"],
                "data": event
            })

        oci_client.update_row(TABLE_NAME, update_row_details=row)
    except Exception as ex:
        # TODO: if fail to write to DB alarm
        logger.error(f"db write error: {str(ex)}")


async def handle_member_join_channel(event):
    random_channel_id = os.environ.get('random_channel_id')
    if (event["channel"] != random_channel_id):
        return

    oci_client = None
    if local_dev:
        config = oci.config.from_file("./oci_config")
        oci_client = oci.nosql.NosqlClient(config)
    else:
        signer = oci.auth.signers.get_resource_principals_signer()
        oci_client = oci.nosql.NosqlClient({}, signer=signer)

    should_post = should_post_message(oci_client, event)

    if should_post:

        new_message_posted = await post_welcome(event)

        if new_message_posted:
            update_db(oci_client, event)


async def post_welcome(event):
    user_id = event['user']
    message = f"Howdy <@{user_id}> 👋🤠"
    webhook_url = os.environ.get('webhook_url')

    success = False

    if local_dev:
        try:
            await slack_client.chat_postMessage(
                channel=f"#{welcome_channel}",
                text=message)
            success = True
        except SlackApiError as e:
            logger.error(f"error: {e.response['error']}")
    else:
        logger.debug(f"posting {message} to url {webhook_url}")

    return success


async def handler(ctx, data: io.BytesIO = None):
    logger.debug("Launching function")

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
        logger.debug(f"event {event}")
        if (event["type"] == "member_joined_channel"):
            await handle_member_join_channel(event)

    return response.Response(
        ctx, response_data=event_response,
        headers={"Content-Type": "application/json"}
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    fdk.handle(handler, loop=loop)
