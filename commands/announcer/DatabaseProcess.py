import logging

from pprint import pprint
from datetime import datetime, timedelta
from commands.announcer.DatabaseInterface import DatabaseInterface as dbi


class DatabaseProcess(object):
    dbi = None              # Object of DatabaseInterface, needs no buffer, doesn't write
    categories = None       # Store all categories with IDs: {id:category}
    users = None            # Stores all Users with their IDs: {id:user}
    threads = None          # Stores latest threads
    logger = logging.getLogger("DatabaseProcess")

    def __init__(self):
        self.dbi = dbi()
        self.get_categories()
        # self.get_users()
        self.get_latest_threads()
        self.logger.debug("Successfully initialized.")
        # self.filter_threads()
        # self.build_threads_with_names()

    def get_categories(self):
        data = self.dbi.query_categories()
        self.categories = self.tuple_to_dict(data)

    def get_users(self):
        data = self.dbi.query_users()
        self.users = self.tuple_to_dict(data)

    def get_latest_threads(self, timeframe=24):
        carelist = list()
        data = self.dbi.query_threads(timeframe)
        self.threads = data
        for line in data:
            carelist.append({
                "threadID":     int(line[0]),
                "categoryID":  int(line[1]),
                "userID":      int(line[2]),
                "title":       line[3],
                "datetime":    line[4]
                })
        self.threads = carelist
        return carelist

    def build_threads_with_names(self):
        for thread in self.threads:
            self.build_thread_with_names(thread)

    def build_thread_with_names(self, thread):
        self.get_users()    # Refresh Username List, or it will go out of date.
        return thread.update({
                'categoryID': self.categories[thread['categoryID']],
                'userID': self.users[thread['userID']]
                })

    def replace_categories_with_name(self, categoryID):
        return self.categories[categoryID]

    def replace_name_with_categories(self, categoryID):
        for k, v in self.categories.iteritems():
            if v == categoryID:
                return k

    def filter_threads(self, hours=24, days=0, minutes=0):
        timeseconds = (((days * 24 + hours) * 60) + minutes) * 60
        deltatime = timedelta(seconds=timeseconds)
        copylist = list()
        for thread in self.threads:
            delta = datetime.now() - thread['datetime']
            if delta < deltatime:
                copylist.append(thread)

        self.threads = copylist

        #pprint(self.threads)



    """Be wary: Usernames can be Unicode: str.decode('UTF-8')"""
    def tuple_to_dict(self, tuple):
        caredict = dict()
        for line in tuple:
            caredict[int(line[0])] = line[1]
        return caredict



if __name__ == "__main__":
    dbp = DatabaseProcess()
    # pprint(dbp.categories)
    # for key, val in dbp.users.iteritems():
    #    print key, val.decode('UTF-8')
    dbp.filter_threads(days=10)
    dbp.build_threads_with_names()
    pprint(dbp.threads)