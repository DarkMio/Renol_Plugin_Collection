import urllib2
import json
import string
import time
import traceback
import simplejson

ID = "ti4"
permission = 0

goals = [
    { "goal" : "Evolving Battle Point Booster", "prize" : 1.8, "description" : "Grants a new Battle Point Booster that improves as your compendium level increases."},
    { "goal" : "Loading Screen Treasure", "prize" : 2.0, "description" : "Grants three Treasures that contain Loading Screens. Extra Treasures available as rewards based on Compendium levels."},
    { "goal" : "Arcana Vote", "prize" : 2.2, "description" : "Unlocks the ability to vote on which hero should receive the next Arcana."},
    { "goal" : "Special Edition HUD", "prize" : 2.4, "description" : "Grants a new Compendium-themed HUD."},
    { "goal" : "Solo Championship Vote", "prize" : 2.6, "description" : "Unlocks the ability to vote on the participants of an 8 player Solo Championship at The International."},
    { "goal" : "New Game Mode", "prize" : 2.9, "description" : "Unlocks the All Random Deathmatch game modes (available to all players, not just Compendium owners)."},
    { "goal" : "Immortal Treasures", "prize" : 3.2, "description" : "Grants a Treasure containing Valve created Immortal Items. Every 10 compendium levels grants you an extra Treasure."},
    { "goal" : "Chat Emoticons", "prize" : 3.5, "description" : "Grants access to special emoticons that can be used in Dota 2 chat."},
    { "goal" : "Mini-Pudge Courier", "prize" : 4.0, "description" : "Grants a special Mini Pudge Courier. Level 50 compendium owners have an alternate skin."},
    { "goal" : "New Music", "prize" : 4.5, "description" : "Grants a new music pack for Dota 2."},
    { "goal" : "New Matchmaking", "prize" : 5.0, "description" : "Unlocks a 1v1 mid-lane-only Match-making option (available to all players, not just Compendium owners)."},
    { "goal" : "Environmental Effects", "prize" : 5.5, "description" : "Grants new environment effects in the Dota map."},
    { "goal" : "Base Customization", "prize" : 6.0, "description" : "Grants an item that allows Compendium owners to customize a building in their base."},
    { "goal" : "Techies Unusual Taunt", "prize" : 6.4, "description" : "Performs a special Taunt animation with added visual effects. Techies will also taunt enemies in their Death Cam when killed by you. Item will be granted to all Compendium Owners when Techies is released after The International.", "status":0},
    { "goal" : "Daily Hero Challange", "prize" : 6.8, "description" : "Earn 25 compendium points every day by winning a game with the Hero we choose for you.", "status":0},
    { "goal" : "Alternate Voice", "prize" : 7.2, "description" : "Vote for the Hero you'd like to receive a new, alternate voice & dialogue pack. When the recording is complete, you will be granted an item that unlocks the new voice.", "status":0},
    { "goal" : "Favorite Hero Challange", "prize" : 7.6, "description" : "Start training for the next international. Select one of you Least Played heroes and we'll provide a GPM / XPM analysis tool during the game to help you compare your performance with previous games. Win 10 games before July 28th and you'll earn compendium points.", "status":0},
    { "goal" : "Model Update Vote", "prize" : 8.0, "description" : "Vote for the Hero you'd like to receive a reworked model.", "status":0},
    { "goal" : "Multi-Kill Banner", "prize" : 8.4, "description" : "You'll receive an item that customizes your Multi-Kill Banner.", "status":0},
    { "goal" : "Afterparty Broadcast", "prize" : 8.8, "description" : "Live Broadcasting of the after party with special guest Darude.", "status":0},
    { "goal" : "New Upgraded Creeps", "prize" : 9.2, "description" : "Unlocks new models for your creeps after you've killed the enemy barracks. (Available to all players, not just Compendium Owners)", "status":0},
    { "goal" : "A->Z Challenge Support", "prize" : 9.6, "description" : "A new quest system will be added to track your progress, and earn you rewards as you win with all the Dota Heroes. (Available to all players, not just Compendium Owners)", "status":0},
    { "goal" : "Victory Prediction Taunt", "prize" : 10, "description" : "Unlocks the ability for you to perform a voice taunt with your hero in the early stages of the game. Keeps track of how many successful predictions you've made in a row.", "status":0},
    { "goal" : "Half Life 3 confirmed.", "prize" : 33.3, "description" : "We get no communication from Valve, but this confirms Half Life 3.", "status":0},
]

banList = [
    "aderum",
    "kobb",
    "jicyphex",
    "quantum"
]
bold = chr(2)
def execute(self, name, params, channel, userdata, rank):
    print params

    if len(params) > 0:
        params = str(params[0])
    else:
        pass


    try:
        for banned_string in banList:
            for item in (name, userdata[0], userdata[1]):
                if banned_string.lower() in item.lower():
                    self.sendNotice(name, "You have been banned from using this command.")
                    return
            else:
                #Okay, shitturds are not on the banlist.
                pass
    except:
        traceback.print_exc()
        print "Something is going wrong."

        #At least Renol doesn't crash. Then the banlist is broken.
        pass


    try:
        try:
            all = string.maketrans('','')
            nodigits = all.translate(all, string.digits)
            jsonurl = urllib2.urlopen('http://dota2.cyborgmatt.com/prizetracker/overlay.php?leagueid=600')
            text = jsonurl.read()
            money = int(text.translate(all, nodigits))
            moneyhelper = (money // 10**4) / 100.

            jsonurl = urllib2.urlopen('http://dota2.cyborgmatt.com/prizetracker/ti4data.php?type=dailydiff')
            daily = simplejson.load(jsonurl)
            growthnumber = daily[-1]

            daysleft = 72 - int(growthnumber["ID"])
            one, two, three = daily[-1], daily[-2], daily[-3]
            oned, twod, threed = int(one["Difference"]), int(two["Difference"]), int(three["Difference"])
            prediction = ((oned + twod + threed) / 3) * daysleft + money

            # get some vars up
            loadsamoney = '{:,}'.format(money)
            strappedmoney = money - 1600000
            valvesamoney = '{:,}'.format(strappedmoney * 3)
            totalmoney = '{:,}'.format(strappedmoney * 4)
            unixtime = int(time.time()) - 1399701600
            gpmoney = '{:,}'.format((strappedmoney * 3) / (unixtime / 60 ))
            growth = '{:,}'.format(int(growthnumber["Difference"]))
            prediction = '{:,}'.format(prediction)

        except:
            self.sendChatMessage(self.send, channel, "TI4 Prizepool API is down, blame CMatt.")


        try:
            paramsfloat = float(params)
        except:
            pass

        if len(params) > 0:
            if params == "all":
                self.sendChatMessage(self.send, channel, "Sending a private message to %s about all stretch goals so far." % name)
                for line in goals:
                    goalhit = (line["prize"] <= moneyhelper and "X") or " "
                    self.sendChatMessage(self.send, name, "[%s] - $%sM >>> %s" % (goalhit, line["prize"], line["goal"]))
                    # self.sendNotice(name, 'Stretch Goal "%s" at $%sM: %s' % (line["goal"], line["prize"], line["description"]))

            elif params == "next":
                for line in goals:
                    if moneyhelper < line["prize"] and moneyhelper >= line["prize"] - 0.4:
                        leftcount = line["prize"]*10**6 - money
                        leftnumber = '{:,}'.format(int(leftcount))
                        leftstring = (leftcount >= 0 and "($"+leftnumber+" left) " ) or ""
                        self.sendChatMessage(self.send, channel, 'Next stretch goal at $%sM %sis "%s": %s' % (line["prize"], leftstring, line["goal"], line["description"]))

            elif params:
                for line in goals:
                    if paramsfloat <= line["prize"]:
                        leftcount = line["prize"]*10**6 - money
                        leftnumber = '{:,}'.format(int(leftcount))
                        leftstring = (leftcount >= 0 and "($"+leftnumber+" left) " ) or ""
                        self.sendChatMessage(self.send, channel, 'Stretch goal at $%sM %sis "%s": %s' % (line["prize"], leftstring, line["goal"], line["description"]))
                        break
                    else:
                            continue

        else:
            try:
                lastgoal = ""
                lastprize = 1.6
                for line in goals:
                    if line["prize"] > moneyhelper:
                        remaining = '{:,}'.format(int(line["prize"]*(10**6)  - money))
                        leftsmall = int(line["prize"]*(10**6) - lastprize*(10**6))
                        leftvalue = int(money - lastprize*(10**6))
                        percentage = (leftvalue * 100) / leftsmall
                        self.sendChatMessage(self.send, channel, "Ti4 Prizepool Total: $%s | Total Sales Volume: $%s | Yesterday's growth: $%s | GPM: $%s | Next goal in $%s (%s%%): %s | Prizepool prediction: $%s" % (loadsamoney, totalmoney, growth, gpmoney, remaining, percentage, line["goal"], prediction))
                        break
                    else:
                        lastprize = line["prize"]
                        lastgoal = line["goal"]
                        continue
                    break
            except:
                self.sendChatMessage(self.send, channel, "Can't connect to the Ti4 Prizepool tracker. Blame Volvo.")
    except:
        traceback.print_exc()
        self.sendChatMessage(self.send, channel, "Invalid syntax. Try a %sfloating value%s, '%sall%s' or '%snext%s' instead." % (bold, bold, bold, bold, bold, bold))
        pass

    #def __initialize__(self, Startup):
    #    if self.events["chat"].doesExist("ti_4"):
    #        self.events["chat"].removeEvent("ti_4")
    #    self.events["chat"].addEvent("ti_4", execute, False)