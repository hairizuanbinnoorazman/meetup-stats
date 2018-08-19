import json
import requests


def get_channel_list(slack_token, slack_channel):
    slack_list_url = "https://slack.com/api/channels.list"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    query_params = {"token": slack_token}

    response = requests.get(
        slack_list_url, headers=headers, params=query_params)
    channels_response = response.json()

    for channel_info in channels_response['channels']:
        if channel_info['name'] == slack_channel:
            return channel_info['id']

    raise Exception(json.dumps({"error": "Channel name not found"}))


def upload_image_to_channel(slack_token, slack_channel_id, image_file_name):
    upload_url = "https://slack.com/api/files.upload"
    data = {"token": slack_token,
            "channels": slack_channel_id}
    file = {'file': open(image_file_name, 'rb')}

    response = requests.post(upload_url, params=data, files=file)

    if response.status_code != 200:
        raise Exception(json.dumps({"error": "Unable to upload image"}))


def send_text_to_channel(slack_token, slack_channel_id, text):
    upload_url = "https://slack.com/api/chat.postMessage"
    data = {"token": slack_token,
            "channel": slack_channel_id,
            "text": text}

    response = requests.post(upload_url, params=data)

    if response.status_code != 200:
        raise Exception(json.dumps({"error": "Unable to send text"}))
