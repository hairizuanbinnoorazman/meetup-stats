import requests
import pandas as pd
from datetime import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

BASE_API = "https://api.meetup.com/"


def get_rsvps(group_name, event_id):
    assert isinstance(group_name, str)
    assert isinstance(event_id, str)

    api_endpoint = "%s%s/events/%s/rsvps" % (BASE_API, group_name, event_id)
    req = requests.get(api_endpoint)
    data = req.json()
    filtered_data = [{'time': datetime.fromtimestamp(
        row['updated']/1000), 'guests': row['guests'], 'attendees': row['guests']+1} for row in data if row['response'] == 'yes']
    df = pd.DataFrame(filtered_data)
    df = df.sort_values(['time'], ascending=True)
    df['total_attendees'] = df['attendees'].cumsum()

    a = df.plot(x='time', y='total_attendees')
    plt.title("Meetup details for %s, event: %s" % (group_name, event_id))
    plt.savefig('/tmp/test.png')


def get_latest_upcoming_event(group_name):
    api_endpoint = "%s%s/events" % (BASE_API, group_name)
    req = requests.get(api_endpoint)
    data = req.json()

    if len(data) == 0:
        raise ValueError("No ID is available to be used")

    filtered_data = [{'time': row['time'], 'id': row['id']} for row in data]
    df = pd.DataFrame(filtered_data)
    df = df.sort_values(['time'], ascending=True)

    return df['id'].iloc[0]
