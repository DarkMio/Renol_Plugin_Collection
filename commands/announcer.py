import time
import logging
import traceback

from commands.announcer.Announcer import Announcer
from commands.announcer.DatabaseProcess import DatabaseProcess
from commands.announcer.DatabaseStorage import DatabaseStorage


ID = "announcer"
permission = 3


def announcer_process(self, pipe):
    # while self.signal != True:
    announcer = self.base[1]
    cmdhdlr = self.base[0]
    channel = self.base[2]

    normal = chr(15)
    blue = chr(3) + '02'
    green = chr(3) + '03'
    orange = chr(3) + '07'
    purple = chr(3) + '13'

    while self.signal is not True:
        try:
            thread = announcer.get_filtered_threads()
            if thread:
                shortlink = "http://d2md.me/d/" + str(thread['threadID'])
                category = thread['categoryID']
                user = thread['userID'].decode('UTF-8')
                title = thread['title'].decode('UTF-8')
                
                cmdhdlr.sendMessage(channel,
                    (u"[{blue}{category}{normal}] {orange}{user}{normal} posted: {green}{title}{normal} | {purple}{shortlink}{normal}".format(
                                               category=category, user=user, title=title, shortlink=shortlink,
                                               normal=normal, blue=blue, green=green, orange=orange, purple=purple)))

            time.sleep(30)
        except Exception as e:
            logger = logging.getLogger("AnnouncerProcess")
            logger.error("Something gone wrong:")
            logger.error(e)
            traceback.print_exc()


def execute(self, name, params, channel, userdata, rank):
    """Commandchain:
        +announce start : append thread to announce
        +announce ignore [id OR name] : ignore certain forum category
        +announce subscribe username : subscribe to replies of (your) account
        +announce help : displays helpfile
        +announce reset : resets the announce-storage
        +announce delete : clears the complete storage
    """
    dbp = DatabaseProcess()
    dbs = DatabaseStorage()
    announcer = Announcer(channel, dbp, dbs)

    if len(params) == 1 and "start" in params:
        if self.threading.checkStatus("forum_announcer_" + channel)[0]:
            self.threading.sigquitThread("forum_announcer_" + channel)
            self.sendNotice(name, "Announcer will be restarted.")
        else:
            self.sendNotice(name, "Announcer started.")
        self.threading.addThread("forum_announcer_" + channel, announcer_process, [self, announcer, channel])
        return


    if len(params) >= 1 and "ignore" in params:
        if params > 1:
            ignore = announcer.add_ignored_category(str(params[1]))
            self.sendNotice(name, 'Ignoring from now on this category: ' + dbp.categories[ignore])
        else:
            self.sendNotice(name, "Invalid use of commandchain.")

    if len(params) == 1 and "reset" in params:
        # @TODO: Change timeframe back on deploy
        threads = dbp.get_latest_threads(timeframe=1000)
        for line in threads:
            dbs.write_DiscussionID(line['threadID'], channel)

    if len(params) == 1 and "delete" in params:
        announcer.delete_storage()

    if len(params) == 1 and "help" in params:
        self.sendNotice(name, "This is the Moddota Forum Announcer, usage as following:")
        self.sendNotice(name, self.cmdprefix + "announce start : append thread to announce")
        self.sendNotice(name, self.cmdprefix + "announce ignore [id OR name] : ignore certain forum category")
        self.sendNotice(name, self.cmdprefix + "announce subscribe username : subscribe to replies of (your) account")
        self.sendNotice(name, self.cmdprefix + "announce help : displays this helpfile")
        self.sendNotice(name, self.cmdprefix + "announce reset : resets the announce-storage")
        self.sendNotice(name, self.cmdprefix + "announce delete : clears the complete storage")
        self.sendNotice(name, self.cmdprefix + "announce info : prints out status of channel")


if __name__ == '__main__':
    # announcer_process('self', 'pipe', '#dota2mods')
    dbp = DatabaseProcess()
    dbs = DatabaseStorage()
    a = Announcer('#dota2mods', dbp, dbs)
    print a.add_ignored_category('Tutorials')
    print dbp.categories[2]
#    threads = dbp.get_latest_threads(timeframe=1000)
#    for line in threads:
#        print line
#        dbs.write_DiscussionID(line['threadID'], '#dota2mods')