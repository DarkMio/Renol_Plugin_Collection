import re
from requests import get
import traceback
import logging


def string_views(view_count):
    if view_count < 1000:
        return view_count
    cnt = 0
    lazy_list = ["", "K", "M", "B", "T"]
    while view_count > 1000:
        view_count /= 1000.0
        cnt += 1
    return "{0:.2f}{1}".format(view_count, lazy_list[cnt])


def execute(string):
    try:
        regex = re.findall(r"(^https?://)?(\w+)?\.?(reddit\.com/|redd\.it/)(r/\w+/)?(comments/)?(\w+)", string)
        if regex:
            headers = {"User-Agent": "Rabscuttle the friendly IRC Bot on #gamesurge"}
            api = "http://reddit.com/{}.json".format(regex[-1][-1])
            result = get(api, headers=headers)
            if result.status_code == 200:
                op_data = result.json()[0]['data']['children'][0]['data']
                sub = op_data['subreddit']
                author = op_data['author']
                score = op_data['score']
                title = op_data['title']
                comments = op_data['num_comments']

                return "/r/{0}: {1} - from {2} ({3} comments, {4} karma)".format(sub,
                                                                                 title,
                                                                                 author,
                                                                                 string_views(comments),
                                                                                 string_views(score))
    except Exception as e:
        print e
        traceback.print_exc()