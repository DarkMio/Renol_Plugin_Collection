import simplejson

from random import randint
from time import time as unixtime
from os import path
from os import makedirs
from datetime import datetime, timedelta, time


class quoteService:
    
    quoteDB = []
    filepath = None
    filename = None
    fileEdit = False
    avg = None
    DBlen = None
    js01 = None
    js02 = None

    def __init__(self):
        self.filepath = path.dirname(__file__)
        self.filename = self.filepath + '/quote.json'
        self.quoteDB = self.ReadDB()
        self.DBlen = len(self.quoteDB)

    def ReadDB(self):
        # in case it's a fresh DB, write a samplefile.
        if not path.exists(self.filename):
            makedirs(self.filename)
            with open(self.filename+'quote.json', 'w') as f:
                f.write('[]')
        # and then read and return it
        with open(self.filename, 'r') as f:
            jsonDB = simplejson.loads(f.read().encode("utf-8"), strict = False)
            return jsonDB

    def WriteDB(self):
        with open(self.filename, 'w') as f:
            f.write(simplejson.dumps(self.quoteDB, sort_keys = True, indent = 4 * ' ').encode("utf-8"))
        self.fileEdit = True


    """Returns a random Quote from the database."""
    def ReturnRandomQuote(self):
        i = randint(0, len(self.quoteDB) - 1)
        return self.quoteDB[i]

    """Returns a quote with this index nummer. Returns with
       false in case there is no quote with this index."""
    def ReturnIndexQuote(self, i):
        for quote in self.quoteDB:
            if quote[0] == i:
                return quote
        return False

    def ReturnLastQuote(self):
        return self.quoteDB[-1]

    def DeleteIndexQuote(self, i):
        copyDB = self.quoteDB
        for quote in copyDB:
            if quote[0] == i:
                self.quoteDB.remove(quote)
                self.WriteDB()
                return True
        return False

    """Currently only returns the amount of submitters and
       the total length of the db (amount of quotes)."""
    def ReturnStats(self):
        usernames = set([])
        textlen = 0.0
        i = 0
        for iq, quotes in enumerate(self.quoteDB):
            usernames.add(quotes[2])
            textlen += len(quotes[1])
            i = iq
        # handle empty quoteDBs.
        i += 1
        textlen = textlen / i
        return len(self.quoteDB), len(usernames), round(textlen, 3)

    """ Writes a quote into the DB and stores it."""
    def WriteIndexQuote(self, quote, submitter):
        date = int(unixtime())
        # Take last index, add one up, store it
        # Or else: set it to zero, bc there is nothing.
        try:
            indexNr = (self.quoteDB[-1][0]) + 1 
        except:
            indexNr = 0
        self.quoteDB.append([indexNr, quote, submitter, date])
        self.WriteDB()

    def DefragDB(self):
        for i, quote in enumerate(self.quoteDB):
            quote[0] = i
        self.WriteDB()


    def convertDataToTimestamp(self):
        self.quoteDB[:] = [[k[0], k[1], k[2], datetime.utcfromtimestamp(float(k[3]))] for k in self.quoteDB]
        return

    """THIS SHIT IS THE MOST IMPORTANT PIECE OF SHIT"""
    def returnStringForJS(self):
        self.convertDataToTimestamp()
        # self.renderQuotesPerHour()
        # self.renderQuotesPerDay()
        # self.renderPercentPerSubmitter()
        return self.quoteDB

    def renderQuotesPerDay(self):
        dataset = str(self.quotesPerDay())

        with open(self.filepath+"chart01.js", 'r') as f:
            self.js01 = f.read().replace("{js}", dataset).replace("{avg}", str(self.avg))
        return


    def renderPercentPerSubmitter(self):
        dataset = str(self.percentPerSubmitter())

        with open(self.filepath+"chart03.js", "r") as f:
            self.js03 = f.read().replace("{js}", dataset).replace("{avg}", str(self.avgPPS)).replace("{len}", str(self.DBlen))
        return

    def renderQuotesPerHour(self):
        dataset = str(self.quotesPerHours())

        with open(self.filepath+"chart02.js", "r") as f:
            self.js02 = f.read().replace("{js}", dataset). replace("{avg}", str(float(self.DBlen)/24))
        return

    def quotesPerHours(self):
        dataset = dict()
        datalist = list()

        for entry in self.quoteDB:
            hour = entry[3].hour
            if not hour in dataset:
                dataset.update({hour: 1})
                continue
            #[dates.update({date.date(): v+1}) for k, v in dates.iteritems() if k == date.date()]
            for k, v in dataset.iteritems():
                if k == hour:
                    dataset.update({hour: v+1})

        for x in range(0,24):
            if x not in dataset:
                dataset.update({x:0})

        for k in sorted(dataset.keys()):
            datalist.append(dataset[k])
        return datalist

    def percentPerSubmitter(self):
        dataset = dict()
        datalist = list()

        for entry in self.quoteDB:
            submitter = entry[2]
            if not submitter in dataset:
                dataset.update({submitter: 1})
                continue
            # [dates.update({date.date(): v+1}) for k, v in dates.iteritems() if k == date.date()]
            for k, v in dataset.iteritems():
                if k == submitter:
                    dataset.update({submitter: v+1})

        dataset = dict((str(k), v) for k, v in dataset.iteritems())
        for k, v in dataset.iteritems():
            datalist.append([k, v])
        self.avgPPS = float(self.DBlen) / len(datalist)
        return datalist

    """A statistic about the quotes submitted per day."""
    def quotesPerDay(self):
        datelist = list()
        dates = self.countQuotesPerDay()
        dates = self.toSparseDataset(dates)

        datelist[:] = [[(datetime.combine(k, time.min) - datetime(1970,1,1)).total_seconds() * 1000,
                          dates[k]] for k in sorted(dates.iterkeys())]

        return datelist

    def avgQuotesPerDay(self, data):
        carelist = sorted(data.keys())
        first_date = carelist[0]
        last_date = carelist[-1]
        days = (last_date - first_date).days
        self.avg = float(len(self.quoteDB)) / days


    def countQuotesPerDay(self):
        dates = dict()
        for entry in self.quoteDB:
            date = entry[3]
            if not date.date() in dates:
                dates.update({date.date(): 1})
                continue
            #[dates.update({date.date(): v+1}) for k, v in dates.iteritems() if k == date.date()]
            for k, v in dates.iteritems():
                if k == date.date():
                    dates.update({date.date(): v+1})
        self.avgQuotesPerDay(dates)
        return dates


    def toSparseDataset(self, data):
        dictionary = dict(data)
        lastday = None
        for k in sorted(data):
            if lastday:
                if abs(k - lastday).days == 2:
                    dictionary.update({lastday+timedelta(days=1): 0})
                if abs(k - lastday).days > 2:
                    dictionary.update({k-timedelta(days=1): 0})
                    dictionary.update({lastday+timedelta(days=1): 0})
            lastday = k
        return dictionary