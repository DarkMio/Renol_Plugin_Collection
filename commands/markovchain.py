from collections import defaultdict
import random
import os


ID = "markov"
permission = 3
markov = defaultdict(list)
STOP_WORD = "\n"

def __initialize__(self, Startup):
    if self.events["chat"].doesExist("markov"):
        self.events["chat"].removeEvent("markov")
    self.events["chat"].addEvent("markov", onPrivmsg)


def onPrivmsg(self, channels, userdata, message, currChannel):
    if u"SQL" in userdata['name'] and random.random() <= 0.01:
        with open(os.path.dirname(__file__) + '/data/brain_bible.txt', 'r') as f:
            for line in f:
                add_to_brain(line, chain_length=4)
            f.close()

        string = "example"
        if message:
           string = ' '.join(message)
        self.sendMessage(currChannel, "{0}".format(
                                   generate_sentence(string, random.randint(8, 30)).replace("\n", "")))


def add_to_brain(msg, chain_length, write_to_file=False):
    buf = [STOP_WORD] * chain_length
    for word in msg.split():
        markov[tuple(buf)].append(word)
        del buf[0]
        buf.append(word)
    markov[tuple(buf)].append(STOP_WORD)


def generate_sentence(msg, chain_length, max_words=10000):
    buf = msg.split()[:chain_length]
#    if len(msg.split()) > chain_length:
#        message = buf[:]
#    else:
    message = []
    for i in xrange(chain_length):
        message.append(random.choice(markov[random.choice(markov.keys())]))
    for i in xrange(max_words):
        try:
            next_word = random.choice(markov[tuple(buf)])
        except IndexError:
            continue
        if next_word == STOP_WORD:
            break
        message.append(next_word)
        del buf[0]
        buf.append(next_word)
    return ' '.join(message)


def execute(self, name, params, channel, userdata, rank):
    with open(os.path.dirname(__file__) + '/data/brain_bible.txt', 'r') as f:
        for line in f:
            add_to_brain(line, chain_length=5)
        f.close()

    string = "example"
    if params:
       string = ' '.join(params)
    self.sendMessage(channel, "{0}".format(
                               generate_sentence(string, random.randint(8, 30)).replace("\n", "")))



if __name__ == "__main__":
    with open(os.path.dirname(__file__) + '/data/brain_bible.txt', 'r') as f:
        for line in f:
            add_to_brain(line, chain_length=3)
        f.close()

    sentence = "there's a thread on /r/REMath from a guy asking for help reverse engineering a dota 2 hack program"
    for i in xrange(0, 100):
        print generate_sentence(sentence, random.randint(8, 30)).replace("\n", "")
        print " "