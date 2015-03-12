from pprint import pprint
import simplejson
import traceback

def ReadDB():
    with open("commands/drama/userlist.json", "r") as f:
        jsonres = simplejson.loads(f.read().encode("utf-8"), strict = False )
        return jsonres


def SaveDB(db):
    with open("commands/drama/userlist.json", "w") as f:
        f.write(simplejson.dumps(db, sort_keys=True, indent=4 * ' ').encode("utf-8"))


def remove(self, user, userdata, channel=None, name=None, i=None):
    # note: Subscriberlist should be the full dataset, so the bot can store it from here
    if not name:
        name = user
    # if there is no channel give, we perform that on all channels
    # recursive as hell, but nice nonetheless
    if not channel:
        for channels in userlist:
            i = remove(self, user, userdata, channel=channels)
        if i:
            return True
        else:
            return


    subscriberlist = ReadDB()
    copylist = subscriberlist
    for userlist in subscriberlist[channel]:
        if all(x in userlist for x in [user, userdata]):
            copylist[channel].remove([user, userdata])
            self.sendNotice(name, "You're now unsubscribed from the Drama-feature in {0}.".format(channel))
            SaveDB(copylist)
            return True
        else:
            continue


def add(self, user, userdata, channel, name=None):
    if not name:
        name = user

    # check if it that guy is already in the list - if so, ignore him
    subscriberlist = ReadDB()

    for channellist in subscriberlist[channel]:
        if all(x in channellist for x in [user, userdata[0]]):
            # So, we catched that mofo already
            self.sendNotice(name, "You're already subscribed with nickname '{0}'.".format(user))
            return
    # or else we store him
    if channel in subscriberlist:        
        subscriberlist[channel].append([user, userdata[0]])
    else:
        subscriberlist[channel] = [[user, userdata[0]]]
    SaveDB(subscriberlist)
    self.sendNotice(name, "You're now subscribed to the drama in {0} with {1}.".format(channel, user))
    return


ID = 'drama'
permission = 0

bold = chr(2)
green = chr(3)+'3'
red = chr(3)+'4'
yellow = chr(3)+'8'
normal = chr(15)


def execute(self, name, params, channel, userdata, rank):
    userlist = ReadDB()
    print userlist
#    if len(params) == 0:
#        self.sendMessage(channel, "I will now notify all subscribed people in this channel.")
#        self.sendNotice(name, "Good job!")
#        
#        
    try:
        if len(params) > 0:
            if params[0].lower() in ('subscribe', 'follow', 'add', ):
                # params: subscribe
                if len(params) == 1 and channel in userlist:
                    add(self, name, userdata[0], channel=channel)

                # params: subscribe var1 var2 var3
                elif len(params) > 1 and channel in userlist:
                    a = 1
                    while (a < len(params)):
                        add(self, params[a], userdata[0], channel=channel, name=name)
                        a += 1


            elif params[0].lower() in ('remove'):
                i = None
                # params: remove
                if len(params) == 1 and channel in userlist:
                    remove(self, name, userdata[0], channel=channel)
                    

                # params: remove [all] [var1 var2 var3]
                elif len(params) > 1 and channel in userlist:
                    # params: remove >all< var1 var2 var3
                    if params[1] == 'all':
                        # params: remove all 
                        if len(params) == 2:
                            # this removes his nicknames everywhere
                            i = remove(self, name, userdata[0])

                        # params: remove all var1 var2 var3
                        else:
                            # he wants to remove (multiple) nicknames
                            # so we iterate through all the params
                            a = 2
                            while (a < len(params)):
                                i = remove(self, params[a], userdata[0], name=name)
                                a += 1

                    # params: remove var1
                    else:    
                        i = remove(self, params[1], userdata[0], channel=channel, name=name)

                # params: remove
                elif channel in userlist:
                    i = remove(self, name, userdata[0], channel=channel)

                if not i:
                    self.sendNotice(name, "You're now unsubscribed from the drama-plugin.")

            elif params[0].lower() in ('help', '?', 'man', 'info'):
                self.sendNotice(name, "Congrats, you've found the manual for the glorious Drama Plugin!")
                self.sendNotice(name, "You have following commands you can execute:")
                self.sendNotice(name, bold+self.cmdprefix+"drama add [nickname]"+bold+": This subscribes you to the drama-feature in this channel. You can add your sub-nicknames aswell, so you definitly will be notified.")
                self.sendNotice(name, bold+self.cmdprefix+"drama [Reason]"+bold+": You will notify all online users that drama is happening at the moment. Also you're able to give a reason, so people might catch up to it faster.")
                self.sendNotice(name, bold+self.cmdprefix+"drama remove [all]"+bold+": This allows you to remove yourself from the Dramalist. This only works with your account. You can use the additional "+bold+"'all'"+bold+" to unsubscribe from all channels.")

            else:
                onlinelist = []
                for usr in self.channelData[channel]['Userlist']:
                    onlinelist.append(usr[0])
                for usr in userlist[channel]:
                    usr = usr[0]
                    if usr in onlinelist:
                        if len(params) > 0:
                            self.sendNotice(usr, 'There is currently drama happening in {0}. Reason: {1}'.format(channel, ' '.join(params)))
                        else:
                            self.sendNotice(usr, 'There is currently drama happening in {0}.'.format(channel))
                return
    except:
        traceback.print_exc()


