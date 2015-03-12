import urllib2
import json
import urllib
import simplejson
import logging


def intWithCommas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


ID = "cf"
permission = 0


def execute(self, name, params, channel, userdata, rank):
    try:
        url = "https://robertsspaceindustries.com/api/stats/getCrowdfundStats"
        data1 = {"fans" : True, "funds" : True}
        data2 = urllib.urlencode(data1)
        req = urllib2.Request(url, data2)
        jsonurl = urllib2.urlopen(req)

        text = jsonurl.read()
        dictionary = simplejson.loads(text)
        wwwant = dictionary['data']
        funds = intWithCommas(wwwant['funds'] // 100)
        fans = intWithCommas(wwwant['fans'])
        self.sendChatMessage(self.send, channel, "Starcitizen Crowdfund Total: $%s | Fans: %s" % (funds, fans))
    except:
        logger = logging.getLogger("StarCitizenCrowdFunding")
        logger.error("No Data received, sending error to requester.")
        self.sendChatMessage(self.send, channel, "Can't connect to RSI API. Blame Chris Roberts.")