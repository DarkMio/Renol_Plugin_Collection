import logging
import simplejson
import re

from os import path, makedirs
from traceback import print_exc


def read(filename):
    if not path.exists(path.dirname(__file__) + "/karma/"):
        makedirs(path.dirname(__file__) + "/karma/")
        with open(path.dirname(__file__) + "/karma/" + filename + '.json', 'w') as f:
            f.write('{}')
    with open(path.dirname(__file__) + "/karma/" + filename + ".json", "r") as f:
        jsonres = simplejson.loads(f.read().encode("utf-8"), strict=False)
        return jsonres


def write(filename, db):
    with open(path.dirname(__file__) + "/karma/" + filename + ".json", "w") as f:
        f.write(simplejson.dumps(db, sort_keys=True, indent=4 * ' ').encode("utf-8"))


def process(type, user):
    db = read(type)
    if user in db:
        db[user] += 1
    else:
        db[user] = 1
    write(type, db)
    return db[user]


def karmacalc(user):
    commends = read("commend")
    reports = read("report")

    if user in commends and user in reports:
        return commends[user] - reports[user]
    elif user in commends:
        return commends[user]
    elif user in reports:
        return -reports[user]


def make_username(username):
    user = ""
    for char in username.encode('UTF-8').lower():
        if char.isalpha() or char.isalnum():
            user += char
    return user

ID = "karma"
permission = 0
logger = logging.getLogger("Karma")


def execute(self, name, params, channel, userdata, rank):
    try:

        if len(params) == 2:
            user = make_username(params[1])

            if "commend" in params[0]:
                action = process("commend", user)
                string = (action > 1 and "commends") or "commend"
            else:
                action = process("report", user)
                string = (action > 1 and "reports") or "report"

            karma = karmacalc(user)
            self.sendMessage(channel, u"Thank you for helping to improve the Dota 2 community. "
                                      u"{0} ({3} Karma) is currently at {1} {2}.".format(params[1], action, string, karma))

        if len(params) == 1:
            karma = karmacalc(make_username(params[0]))
            self.sendMessage(channel, u"{0} is currently at {1} Karma.".format(params[0], karma))

    except Exception as e:
        logger.error("Something unexpected happened:")
        print_exc()


if __name__ == "__main__":
    execute('self', 'DarkMio', [u'commend', u'Yoshi2'], '#w3x-to-vmf', (u'~moto', u'DarkMio.user.gamesurge'), '@@')