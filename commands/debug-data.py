ID = 'debugdata'
permission = 0
def execute(self, name, params, channel, userdata, rank):
    self.sendMessage(channel, "Name: {0}, Params: {1}, Channel: {2}, Userdata: {3}, Rank: {4}".format(name, params, channel, userdata, rank))