ID = "report"
permission = 0


def execute(self, name, params, channel, userdata, rank):
    self.commands['karma'][0].execute(self, name, [u'report', params[0]], channel, userdata, rank)