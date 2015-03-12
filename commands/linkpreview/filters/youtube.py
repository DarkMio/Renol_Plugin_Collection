#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import logging


pref = "youtu"


def string_time(seconds):
    m, s = divmod(seconds, 60)
    if not m:
        return "0:{0}".format(s)
    else:
        return "{0}:{1}".format(m, s)


def string_views(view_count):
    cnt = 0
    lazy_list = ["", "K", "M", "B", "T"]
    while view_count > 1000:
        view_count /= 1000.0
        cnt += 1
    return "{0:.2f}{1}".format(view_count, lazy_list[cnt])


def execute(string):
    try:
        regex = re.findall("(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?(?:.*?"
                           "&(?:amp;)?)?v=|\.be/)([\w‌​\-]+)(?:&(?:amp;)?[\w\?=]*)?", string, flags=re.UNICODE)
        # Are the first two characters equal to mainPrefix?
        if regex:
            id = str(regex[0])
            url_api = "http://gdata.youtube.com/feeds/api/videos/{0}".format(id)
            params = {"alt": "json", "v": "2"}
            r = requests.get(url_api, params=params)
            result = r.json()

            time = string_time(result["entry"]["media$group"]["media$content"][0]["duration"])
            view_count = string_views(int(result["entry"]["yt$statistics"]["viewCount"]))

            return u"\"{0}\" [{3}] by {1} | ({2} views)".format(result["entry"]["title"]["$t"],
                                                                result["entry"]["author"][0]["name"]["$t"],
                                                                view_count,
                                                                time)
        else:
            return False

    except Exception as e:
        logger = logging.getLogger("YouTube")
        logger.error("Something gone wrong:")
        logger.error(e)
        pass
