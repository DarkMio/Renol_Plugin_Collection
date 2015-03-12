import logging

from datetime import datetime


class Announcer(object):
    dbp = None		# Stores DatabaseProcess object
    dbs = None		# Stores DatabaseStorage object
    channel = None  # Stores session channel
    threadIDs = None  # Stores all thread IDs
    logger = None   # Stores the Logger-Handler

    def __init__(self, channel, dbp, dbs):
        self.dbp = dbp
        self.dbs = dbs
        self.channel = channel
        self.threadIDs = self.get_threads()
        self.logger = logging.getLogger("AnnouncerObject")
        self.logger.debug("Got __init__ call from channel {0}.".format(channel))

    def get_threads(self):
        caredict = dict()
        careval = self.dbs.get_ids_per_channel(self.channel)
        for line in careval:
            caredict[line[0]] = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')
        return caredict

    """Returns one thread to discuss back."""

    def get_filtered_threads(self):
        ignorelist = self.get_ignores_in_list()
        data = self.dbp.get_latest_threads(240)
        for line in data:
            if not line['threadID'] in self.threadIDs.keys() and str(line['categoryID']) not in ignorelist:
                self.logger.debug("Got a new thread: {}".format(line))
                self.dbs.write_DiscussionID(line['threadID'], self.channel)
                self.threadIDs[line['threadID']] = line['datetime']
                self.dbp.build_thread_with_names(line)
                return line

    """Catches up the latest Discussions with the storage, so the  bot doesn't spam."""

    def reset_storage(self):
        data = self.dbp.get_latest_threads(24 * 30)
        for line in data:
            self.dbs.write_DiscussionID(line['threadID'], self.channel)

    """Clears the entire database from one channel. Handle with care."""

    def delete_storage(self):
        self.dbs.delete_for_channel(self.channel)

    """Adds a new ignore into the database."""
    def add_ignored_category(self, category):
        category = str(self.category_to_int(category))
        ignorelist = self.get_ignores_in_list()
        if category not in ignorelist:
            ignorelist.append(str(category))
        ignorestring = ",".join(ignorelist)
        self.dbs.write_ignorelist(ignorestring, self.channel)
        return int(category)

    def get_ignores_in_list(self):
        ignores = self.dbs.get_ignores_per_channel(self.channel)
        if ignores:
            return str(ignores[0][0]).split(',')
        else:
            return []

    """Helps in mapping a category to an int."""

    def category_to_int(self, category):
        try:
            category = int(category)
        except ValueError:
            pass
        if isinstance(category, str):
            category = self.dbp.replace_name_with_categories(category)
        return category