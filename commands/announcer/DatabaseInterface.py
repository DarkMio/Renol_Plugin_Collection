import MySQLdb as mysql

from pkg_resources import resource_filename
from ConfigParser import ConfigParser
from pprint import pprint


class DatabaseInterface(object):
    con = None      # holds the DB session
    cur = None      # holds the DB session cursor

    def __init__(self):
        config = ConfigParser()
        config.read(resource_filename("commands.announcer", "config.ini"))

        host = config.get('DATABASE', 'host')
        user = config.get('DATABASE', 'user')
        pwd = config.get('DATABASE', 'pwd')
        db = config.get('DATABASE', 'db')

        self.con = mysql.connect(host, user, pwd, db)
        self.cur = self.con.cursor()
        self.con.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8')
        self.cur.execute('SET CHARACTER SET utf8')
        self.cur.execute('SET character_set_connection=utf8')

    def readtest(self):
        self.cur.execute('SELECT CategoryID, Name FROM GDN_Category')
        data = self.cur.fetchall()
        for line in data:

            pprint(line[0])
            pprint(line[1])

        pprint(data)

    def query_categories(self):
        self.cur.execute('SELECT CategoryID, Name FROM GDN_Category')
        return self.cur.fetchall()

    def query_users(self):
        self.cur.execute('SELECT UserID, Name from GDN_User')
        return self.cur.fetchall()

    # @TODO: Change time-interval back to 1 hour after getting live / getting new database.
    def query_threads(self, timeframe):
        self.cur.execute('SELECT DiscussionID, CategoryID, InsertUserID, Name, DateInserted FROM GDN_Discussion WHERE DateInserted >= DATE_SUB(NOW(),INTERVAL %s HOUR);', (timeframe,))
        return self.cur.fetchall()



if __name__ == '__main__':
    dbi = DatabaseInterface()
    dbi.readtest()
