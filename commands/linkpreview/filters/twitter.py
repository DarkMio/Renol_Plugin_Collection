import requests
import re
from requests_oauthlib import OAuth1
import logging


def execute(string):
    try:
        regex = re.findall("(^|/|\.)twitter\.com/(.+?)/status/([0-9]+)/?", string, flags=re.UNICODE)
        print regex
        if regex:
            api = "https://api.twitter.com/1.1/statuses/show/{}.json".format(regex[-1][-1])
            auth = OAuth1('TtO8GHrXNiXkvPmL1ctuRnxgn', 'hUxJJLFKEsaXwB2UfpdvHdb5N2cqqppG5VdNVPzqXJVl0LPjtT')
            r = requests.get(api, auth=auth)
            result = r.json()
            if r.status_code == 200:
                return u"Twitter: @{user}: {msg}".format(user=result['user']['screen_name'], msg=result['text'])
            else:
                return False

        else:
            return False

    except Exception as e:
        logger = logging.getLogger("Twitter")
        logger.error("Something gone wrong:")
        logger.error(e)
        pass