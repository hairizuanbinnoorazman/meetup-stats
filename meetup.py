import requests
import pandas as pd
from datetime import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

BASE_API = "https://api.meetup.com/"


def get_rsvps(group_name, event_id):
    api_endpoint = "%s%s/events/%s/rsvps" % (BASE_API, group_name, event_id)
    req = requests.get(api_endpoint)
    data = req.json()
    filtered_data = [{'time': datetime.fromtimestamp(
        row['updated']/1000), 'guests': row['guests'], 'attendees': row['guests']+1} for row in data if row['response'] == 'yes']
    df = pd.DataFrame(filtered_data)

    fig = plt.figure()
    a = df.plot(x='time', y='attendees')
    fig.savefig('/tmp/test.png')
