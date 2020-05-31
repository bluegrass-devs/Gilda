import io
import os
import json
import logging

import asyncio
import fdk
import oci

from fdk import response
from slack import WebClient
from slack.errors import SlackApiError

local_dev = os.getenv('is_local', False)
local_oci_config = os.getenv('local_oci_config', False)

compartment_id = os.environ.get('compartment_id')
slack_bot_token = os.environ.get('slack_bot_token')

FORMAT = '%(asctime)s -- %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()

TABLE_NAME = "slack_events"

slack_client = WebClient(token=slack_bot_token, run_async=True)


def init_client():
    oci_client = None
    if local_oci_config:
        config = oci.config.from_file("./oci_config")
        oci_client = oci.nosql.NosqlClient(config)
    else:
        signer = oci.auth.signers.get_resource_principals_signer()
        oci_client = oci.nosql.NosqlClient({}, signer=signer)

    return oci_client


def update_db(oci_client, event):
    updated = False

    if local_dev:
        # Local dev we can assume most of the time the event will
        # be updated in the db. This simulates a new record
        updated = True
    else:
        try:
            row = oci.nosql.models.UpdateRowDetails(
                compartment_id=compartment_id,
                option="IF_ABSENT",
                is_get_return_row=True,
                value={
                    "event_type": event["type"],
                    "channel_id": event["channel"],
                    "user_id": event["user"],
                    "data": event
                })

            response = oci_client.update_row(
                TABLE_NAME,
                update_row_details=row
            )

            if response.data.existing_version is None:
                updated = True
        except Exception as ex:
            # TODO: if fail to write to DB alarm
            logger.error(f"db write error: {str(ex)}")

    return updated


async def handle_member_join_channel(event):
    random_channel_id = os.environ.get('random_channel_id')
    if (event["channel"] != random_channel_id):
        return

    oci_client = init_client()

    # Write to DB to block other functions
    # If write fails event already handled
    should_post = update_db(oci_client, event)

    if should_post:
        success = await post_welcome(event)
        if not success:
            raise NameError("postingWelcomeFail")
    else:
        logger.debug("Nothing to post. The user join is already in the DB.")


async def post_welcome(event):
    user_id = event['user']
    message = f"Howdy <@{user_id}> 👋🤠"

    success = False

    if local_dev:
        logger.debug(f"posting message: {message}")
    else:
        try:
            await slack_client.chat_postMessage(
                channel=event['channel'],
                text=message)
            success = True
        except SlackApiError as e:
            logger.error(f"error: {e.response['error']}")

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
