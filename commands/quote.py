import traceback
import logging
import os
import re
import requests

from datetime import datetime
from commands.quoteDB.QuoteService import quoteService
from commands.quoteDB.HTMLrenderer import HTMLrenderer


def debugBuilder(quote, debugInfo):
    if debugInfo:
        return " | submitted by {0} on {1}".format(quote[2], datetime.fromtimestamp(quote[3]).strftime('%d. %B %Y'))
    return ""


def CallForHelp(self, channel):
    self.sendMessage(channel, "=memo DarkMio The bot couldn't write into the DB. Can you please fix it? Sincerely, the Bot.")


ID = "quote"
permission = 0
filepath = "commands/quoteDB/"
logger = logging.getLogger("Quote")


def execute(self, name, params, channel, userdata, rank):
    try:
        #init of DB
        quoteOBJ = quoteService()
        debugInfo = False
        statsLen, statsUsercnt, statsTextlen = quoteOBJ.ReturnStats()

        if len(params) > 0:
            if "--info" in params[-1]:
                debugInfo = True
                params.remove(params[-1])

        # giff random quote
        if not params:
            if statsLen:
                quote = quoteOBJ.ReturnRandomQuote()
                debugString = debugBuilder(quote, debugInfo)
                self.sendMessage(channel, u"{0}: {1}{2}".format(quote[0] + 1, quote[1], debugString))
                return
            else:
                self.sendMessage(channel, "As there are no quotes in the database, I can't quote anything.")
                return

        # !quote 3 == Someone wants the quote with the index of 3.
        if len(params) >= 1 and params[0].isdigit():
            quote = quoteOBJ.ReturnIndexQuote(int(params[0]) - 1)
            logger.debug("Quote Data: {0}".format(str(quote)))
            if quote:
                debugString = debugBuilder(quote, debugInfo)
                self.sendMessage(channel, u"{0}: {1}{2}".format(quote[0] + 1, quote[1], debugString))
                return
            self.sendMessage(channel, "There doesn't exist a quote with index {0}.".format(params[0]))
            return

        # helpfile
        if len(params) == 1 and "help" in params[0]:
            self.sendNotice(name, "You have following options now:")
            self.sendNotice(name, self.cmdprefix+"quote: Prints out a random quote.")
            self.sendNotice(name, self.cmdprefix+"quote [index]: Prints out a certain quote.")
            self.sendNotice(name, self.cmdprefix+"quote delete [index]: Deletes the quote at this index. ")
            self.sendNotice(name, self.cmdprefix+"quote <some Quote>: Adds <some quote> to the collection.")
            self.sendNotice(name, self.cmdprefix+"quote status: Shows how many quotes there are and how many people contributed to it.")
            self.sendNotice(name, self.cmdprefix+"quote index: Throws out the link to the index website with all quotes.")
            self.sendNotice(name, self.cmdprefix+"quote defrag: Defrags the index-numbers of every quote out there. Operators only.")
            self.sendNotice(name, self.cmdprefix+"quote render: Rerenders the index-HTML. Operators only.")
            return

        # status about the entire thing
        if len(params) == 1 and "index" in params[0]:
            self.sendMessage(channel, "Here you go, buddy, a website with all quotes! http://moddota.com/rabscuttle/")
            return

        # status about the entire thing
        if len(params) == 1 and "status" in params[0]:
            self.sendMessage(channel, "Good news everyone! I've got exactly {0} quotes from a total of {1} shitposters. The average quote length currently is {2} characters.".format(statsLen, statsUsercnt, statsTextlen))
            return

        # force a html-render of the quote-html.
        if len(params) == 1 and "render" in params[0]:
            if rank == '@@':
                HTMLrenderer('/var/www/rabscuttle/', quoteOBJ)
                self.sendNotice(name, "Rerendered HTML successfully.")
                return
            else:
                self.sendNotice(name, "You're not allowed to do that.")
                return

        # force cloudflare to purge the caches
        if len(params) == 1 and "purge" in params[0]:
            if rank == '@@':
                urlAPI = "https://www.cloudflare.com/api_json.html"
                r_params = {"tkn": "1ff08dd21743913cac4c3b4d0c377a377c593", "email": "dem7yw@virginia.edu", "z": "moddota.com", "a": "zone_file_purge"}
                for root, dirs, files in os.walk('/var/www/rabscuttle/static/'):
                    files = [os.path.join(root, f) for f in files]
                    for name in files:
                        params = dict(r_params)
                        params["url"] = "http://www.moddota.com{0}".format(name[8:])
                        requests.get(urlAPI, params=params)
                        
                    for name in files:
                        params = dict(r_params)
                        params["url"] = "https://www.moddota.com{0}".format(name[8:])
                        requests.get(urlAPI, params=params)

                self.sendNotice(name, "Sent all requests.")
                return

        # defrag the index-nums of the quoteDB
        if len(params) == 1 and "defrag" in params[0]:
            if rank == '@@':
                quoteOBJ.DefragDB()
                HTMLrenderer('/var/www/rabscuttle/', quoteOBJ)
                self.sendNotice(name, "I've defragged the quoteDB.")
                return
            else:
                self.sendNotice(name, "You're not allowed to do that.")
                return

        # !quote delete 3
        if len(params) == 2 and "delete" in params[0]:
            # catch wrong use of command        
            try:
                paramsInt = int(params[1]) - 1
            except:
                self.sendNotice(name, "To delete, you should use this command: {0}quote delete [INTEGER]".format(self.cmdprefix))
                return

            quote = quoteOBJ.ReturnIndexQuote(paramsInt)
            if quote[2] == name or rank == '@@':
                try:
                    # returns true if deleted
                    if quoteOBJ.DeleteIndexQuote(paramsInt):
                        self.sendMessage(channel, u"Deleted this precious quote: {0}".format(quote[1]))
                        HTMLrenderer('/var/www/rabscuttle/', quoteOBJ)
                        return
                    self.sendNotice(name, "I couldn't find the quote you were asking me to delete for.")
                    return
                except:
                    logger.error("Something unexpected happened:")
                    traceback.print_exc()
                    CallForHelp(self, channel)
                    return

            else:
                    self.sendNotice(name, "You're not allowed to delete this quote.")
                    return

        # hopefully this is finally a quote to store
        else: 
            try:
                regex = re.compile("\x1f|\x02|\x12|\x0f|\x16|\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)

                for i, entry in enumerate(params):
                    try:
                        params[i] = regex.sub('', entry)
                    except:
                        pass

                string = ' '.join(params)
                quoteOBJ.WriteIndexQuote(string, name)
                quote = quoteOBJ.ReturnLastQuote()
                self.sendMessage(channel, "Your quote has been added, its index is {0}.".format(quote[0]+1))
                HTMLrenderer('/var/www/rabscuttle/', quoteOBJ)
                return
            except:
                logger.error("Something unexpected happened:")
                traceback.print_exc()
                CallForHelp(self, channel)

    except:
        logger.error("Something unexpected happened:")
        traceback.print_exc()


if __name__ == "__main__":
    print "Initializing Quote Object...",
    quote = quoteService(filepath)
    print "success."

    print "Writing a new quote into the DB...",
    debugQuote, debugUser = "This is a test quote.", "Mio"
    quote.WriteIndexQuote(debugQuote, debugUser)
    print "success."

    print "Comparing data in DB with testdata...",
    debugQuoteData = quote.ReturnLastQuote()
    if debugQuote == debugQuoteData[1] and debugUser == debugQuoteData[2]:
        print "success."
    else:
        print "failed!"
    
    print "Deleting new generated dataset ...",
    quote.DeleteIndexQuote(debugQuoteData[0])
    print "success."
    
    print "Returning statistics of current Database...",
    debugLen, debugUser, avgQuoteLen = quote.ReturnStats()
    print "success:",
    print "DB Length: {0} | Amount of Users: {1} | Avg. length of quotes: {2}".format(debugLen, debugUser, avgQuoteLen)
    

    if quote.fileEdit:
        HTMLrenderer('/var/www/rabscuttle/', quote)
