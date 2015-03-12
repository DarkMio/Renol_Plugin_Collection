import commands.linkpreview.filters as filters
import logging
import pkgutil
import commands.linkpreview.urlmarker as url_marker
import re
import requests

from bs4 import BeautifulSoup


class FilterObject(object):
    filters = None         # holds all filters as modules
    logger = None          # Logging Instance
    url_finder = None      # compiled version of an regex that hopefully finds all urls.

    def __init__(self):
        self.logger = logging.getLogger("FilterObject")
        self.load_filters()
        self.url_finder = re.compile(url_marker.URL_REGEX)

    def debug_test(self):
        for module in self.filters:
            module.print_debug()

    def prefilter_text(self, string):
        return self.url_finder.findall(string)

    # filters and executes
    # returns false when nothing could've been loaded
    def filter_text(self, string):
        for module in self.filters:
            # control via variable - quick an easy
            result = module.execute(string)
            if result:
                return result
            else:
                continue

        # so - nothing in our filters actually qualified for that link, we want to load just the title:
        return False
        # return self.standard_loader(string)

    def load_filters(self):
        # cleaning of the list
        self.filters = list()

        package = filters
        prefix = package.__name__ + "."

        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            self.logger.info("Found submodule {0} (is a package: {1})".format(modname, ispkg))
            module = __import__(modname, fromlist="dummy")
            self.filters.append(module)

    def standard_loader(self, string):
        if not "http" in string:
            string = "http://{0}".format(string)
        r = requests.get(string)

        result = BeautifulSoup(r.text.encode('UTF-8', 'ignore')).title
        if result:
            return u"URL Title: {}".format(result.string)
        else:
            return False

    def return_string_from_url(self, string):
        # get all urls in one string
        urls = self.prefilter_text(string)
        if urls:
            # we only care about the first link, otherwise it gets spammy
            return self.filter_text(urls[0])

if __name__ == '__main__':
    fo = FilterObject()
    print fo.return_string_from_url("http://steamdb.info/")