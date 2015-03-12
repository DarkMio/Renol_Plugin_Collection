from commands.linkpreview.FilterObject import FilterObject
import logging
import traceback

ID = "linkpreview"
permission = 3

logger = logging.getLogger("LinkPreview")


def __initialize__(self, Startup):
    if self.events["chat"].doesExist("Youtube_Check"):
        self.events["chat"].removeEvent("Youtube_Check")
    if not hasattr(self, 'FilterObject'):
        logger.info("Creating FilterObject for the first time.")
        self.FilterObject = FilterObject()
    self.events["chat"].addEvent("Youtube_Check", onPrivmsg)


def onPrivmsg(self, channels, userdata, message, currChannel):
    if userdata['name'] == "idler2":
        return
    try:
        result = self.FilterObject.return_string_from_url(message)
    except Exception as e:
        traceback.print_exc()
        return
    if result:
        self.sendMessage(currChannel, result)


def execute(self, name, params, channel, userdata, rank):
    self.sendNotice(name, "Reloading stuff.")
    if params and "reload" in params[0]:
        self.FilterObject.load_filters()
        self.sendNotice(name, "FilterObjects and its filters successfully reloaded.")