from google.cloud import storage
import logging
import json
import os

import meetup
import slack


def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>.
    """
    client = storage.Client()
    text_value = request.form.get('text')
    logging.info(text_value)
    bucket = client.get_bucket('gcpug-meetup-files')
    blob = bucket.get_blob('config/config.json')
    keys = blob.download_as_string()
    keys_json = json.loads(keys)

    meetup.get_rsvps("GCPUGSG", "251921227")

    slack_token = keys_json['slack_token']
    slack_channel_name = keys_json['slack_channel_name']
    channel_id = slack.get_channel_list(slack_token, slack_channel_name)
    slack.upload_image_to_channel(slack_token, channel_id,
                                  "/tmp/test.png")

    return 'test v3!'
