import logging
import os

import meetup


def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>.
    """
    meetup.get_rsvps("GCPUGSG", "251921227")
    print(os.listdir())
    return 'test v2!'
