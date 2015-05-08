from pprint import pprint
import requests
import simplejson


ID = 'steamstatus'
permission = 0

bold = chr(2)
green = chr(3)+'3'
red = chr(3)+'4'
yellow = chr(3)+'8'
normal = chr(15)

def status_mapper(key, status):
    if status == 'major':
        key = bold+red+" "+key+bold
    elif status == 'minor':
        key = bold+yellow+" "+key+bold
    elif status == 'good':
        key = bold+green+" "+key+bold

    return key

def execute(self, name, params, channel, userdata, rank):
    generalbox = []
    carebox = []
    string_dictionary = {
        'cm-SG': 'Singapore', 'cm-US': 'United States', 'cm-NL':'Netherlands',
        'cm-EU':'Europe', 'cm-CN':'China', 'cm-AU':'Australia', 'steam':'Steam',
        'store':'Store', 'community':'Community', 'webapi':'Web API',
        'online':'Online', 'dota2':'Dota2 GC', 'tf2':'TF2 GC', 'csgo':'CSGO GC',
        'dota_mm_average':'Average Wait Time', 'dota_mm_regions':'Online Regions',
        'dota_mm_searching':'Players Searching'}
    
    relevant_ouput = ['webapi', 'tf2', 'store', 'online', 'dota2', 'csgo', 'community', 'cm-AU', 'cm-CN', 'cm-EU', 'cm-NL', 'cm-SG', 'cm-US']
    outage = None

    colors_dictionary = {}
    try:
        headers = {'User-Agent': 'Renol IRC Bot on GameSurge as "Rabscuttle"',}
        request = requests.get('https://steamdb.info/api/SteamRailgun/', headers=headers)
        data = simplejson.loads(request.text, encoding = "utf-8")
        services = data["services"]
    except:
        self.sendMessage(channel, "I can't receive any data from steamstat.us - so even that might be down. Retry in a few.")
        return

    params.append('')

    if params[0] in ('', 'status'):
        for key, value in services.iteritems():
            if key in relevant_ouput:
                if 'cm' in key:
                    if value['status'] == 'major' and outage > 1:
                        outage = 2
                    elif value['status'] == 'minor' and not outage > 0:
                        outage = 1
                else:
                    for short_str, long_str in string_dictionary.iteritems():
                        key = key.replace(short_str, long_str)

                    value['title'] = status_mapper(value['title'], value['status'])
                    generalbox.append(key+":"+value['title']+normal)
        
        if outage == 2:
            outage_string = 'Currently Steam Servers experience'+bold+red+'major outages'+normal+'.'
        elif outage == 1:
            outage_string = 'Currently Steam Servers experience'+bold+yellow+'minor outages'+normal+'.'
            outage = None
        else:
            outage_string = 'All Steam Servers are '+bold+green+'working'+normal+' as intended.'
        outage_string

        generalbox.sort()
        carestring = " | ".join(generalbox)
        self.sendMessage(channel, "{0} | {1}".format(outage_string, carestring))
        

    elif outage or params[0] in ('servers', 'server', 'serv', 's',):
        for key, value in services.iteritems():
            #map status to something new we can use more easily as a final string
            if 'cm' in key:
            #if value['status'] != 'good':

                
                for short_str, long_str in string_dictionary.iteritems():
                    key = key.replace(short_str, long_str)

                key = status_mapper(key, value['status'])

                carebox.append(key+": "+value['title']+normal)

        carebox.sort()
        carestring = " | ".join(carebox)
        self.sendMessage(channel, "Steam Outage Status: {0}".format(carestring))


    elif params[0] in ('dota2gc', 'dota2', 'dota', 'd', 'gc'):
        pprint(data)
        for key, value in services.iteritems():
            if 'dota' in key:
                for short_str, long_str in string_dictionary.iteritems():
                    key = key.replace(short_str, long_str)

                key = status_mapper(key, value['status'])

                carebox.append(key+": "+value['title']+normal)

        carestring = " | ".join(carebox)
        self.sendMessage(channel, "Dota 2 GC Status: {0}".format(carestring))
    elif params[0] in ('h', 'help', 'commands', 'c'):
        self.sendNotice(name, self.cmdprefix+'steamstatus has following commands:')
        self.sendNotice(name, bold+'status'+normal+': Outputs the current status of the entire SteamNetwork.')
        self.sendNotice(name, bold+'servers'+normal+': Outputs the current status of all Steam Servers.')
        self.sendNotice(name, bold+'dota2gc'+normal+' / '+bold+'dota2'+normal+' / '+bold+'gc'+normal+': Displays the current state of the Dota 2 GameCoordinator.')
    else:
        self.sendNotice(name, "Your parameters don't match any command. Check "+bold+self.cmdprefix+"steamstatus help"+normal+" for further information.")




#execute('self', 'DarkMio', ['gc'], 'dota2mods', 'userdata', '0')
