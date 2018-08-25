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
    group_name = ""
    event_id = ""

    # Retrieve creds
    client = storage.Client()
    bucket = client.get_bucket('gcpug-meetup-files')
    blob = bucket.get_blob('config/config.json')
    keys = blob.download_as_string()
    keys_json = json.loads(keys)

    # Retrieve slack channel id
    slack_token = keys_json['slack_token']
    slack_channel_name = keys_json['slack_channel_name']
    channel_id = slack.get_channel_list(slack_token, slack_channel_name)

    text_value = request.form.get('text')
    logging.info("Text_Value: %s" % (text_value))
    try:
        if text_value is None or text_value == "":
            logging.info("No Group name passed in")
        else:
            split_text = text_value.split(" ")
            if len(split_text) == 1:
                group_name = split_text[0]
                event_id = meetup.get_latest_upcoming_event(group_name)
            else:
                group_name = split_text[0]
                event_id = split_text[1]
    except ValueError as e:
        logging.error(e)
        slack.send_text_to_channel(
            slack_token, channel_id, "Group name is unavailable. Please check again")
        return "error"
    except Exception as e:
        logging.error(e)
        slack.send_text_to_channel(
            slack_token, channel_id, "Error in retrieving stats. Check logs")
        return "error"

    # TODO: Move default channel to a config file
    if group_name == "":
        group_name = "GCPUGSG"
    if event_id == "":
        event_id = "251921227"
    meetup.get_rsvps(group_name, event_id)

    slack.upload_image_to_channel(slack_token, channel_id,
                                  "/tmp/test.png")

    return 'test v5!'
