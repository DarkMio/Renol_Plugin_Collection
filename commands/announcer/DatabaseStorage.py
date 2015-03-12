import sqlite3
import logging
from pkg_resources import resource_filename


class DatabaseStorage(object):
    db = None       # Stores db session
    cur = None      # Stores db cursor
    logger = logging.getLogger("DatabaseStorage")

    def __init__(self):
        self.db = sqlite3.connect(
            resource_filename("commands.announcer", "announcer_storage.db"),
            check_same_thread=False,
            isolation_level=None)
        self.cur = self.db.cursor()
        self.database_init()

    """Inits the Database and generates if not generated"""
    def database_init(self):
        if not self.database_check_if_exists('storage'):
            self.cur.execute(
                'CREATE TABLE IF NOT EXISTS storage (DiscussionID LONG, Channel STR(50), DateTime datetime)')
            self.logger.debug("Table 'storage' is generated and ready.")
        else:
            self.logger.debug("Table 'storage' was already generated and is ready.")

        if not self.database_check_if_exists('meta'):
            self.cur.execute(
                'CREATE TABLE IF NOT EXISTS meta (Channel STR(50), CategoryIDs TEXT)')
            self.logger.debug("Table 'meta' is generated and ready.")
        else:
            self.logger.debug("Table 'meta' was already generated and is ready.")

    def database_check_if_exists(self, channel):
        self.cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=(?)', (channel,))
        return self.cur.fetchone()

    def get_ids_per_channel(self, channel):
        self.cur.execute('SELECT * FROM storage WHERE Channel=(?)', (channel,))
        return self.cur.fetchall()

    def get_ignores_per_channel(self, channel):
        self.cur.execute('SELECT CategoryIDs FROM meta WHERE Channel=(?)', (channel,))
        return self.cur.fetchall()

    def write_DiscussionID(self, ident, channel):
        self.cur.execute('INSERT INTO storage VALUES ((?), (?), CURRENT_TIMESTAMP)', (ident, channel,))

    def write_ignorelist(self, ignores, channel):
        self.cur.execute('SELECT * FROM meta WHERE Channel=(?)', (channel,))
        if self.cur.fetchone():
            self.cur.execute('UPDATE meta SET CategoryIDs=(?) WHERE Channel=(?)', (ignores, channel,))
        else:
            self.cur.execute('INSERT INTO meta (Channel, CategoryIDs) VALUES ((?), (?))', (channel, ignores,))

    def cleaner_rover(self):
        print "Ronald rover and the database, " \
              "needs actual data selection methods."

    def delete_for_channel(self, channel):
        self.cur.execute('DELETE FROM storage WHERE Channel=(?)', (channel,))



if __name__ == '__main__':
    dbs = DatabaseStorage()
    dbs.write_DiscussionID(93, '#dota2mods')