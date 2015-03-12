from os import listdir, path
from jinja2 import Environment, FileSystemLoader
from random import randint


class HTMLrenderer(object):
    quotes = None       # Stores quotes.
    wwwdir = None       # Directory of the final html
    libdir = None       # Where the renderer actually works.
    quoteOBJ = None     # Stores quoteService

    def __init__(self, wwwdir, quoteOBJ):
        self.quoteOBJ = quoteOBJ
        self.quoteOBJ.returnStringForJS()
        self.libdir = path.dirname(__file__)
        self.wwwdir = path.abspath(wwwdir)
        self.env = Environment(loader=FileSystemLoader(self.libdir+"/templates"), autoescape=True)
        self.render_multiple_js()
        self.render_html()

    def render_multiple_js(self):
        quoteOBJ = self.quoteOBJ
        self.render_js("chart01.js", data=quoteOBJ.quotesPerDay(), avg=quoteOBJ.avg)
        self.render_js("chart02.js", data=quoteOBJ.quotesPerHours(), avg=str(float(quoteOBJ.DBlen)/24))
        self.render_js("chart03.js", data=quoteOBJ.percentPerSubmitter(), avg=quoteOBJ.avgPPS, len=quoteOBJ.DBlen)

    def render_js(self, filename, avg=0, data=None, len=1):
        template = self.env.get_template(filename)
        output = template.render(data=data, avg=avg, len=len)
        with open(self.wwwdir+'/js/'+filename, 'w') as f:
            f.write(output.encode('utf-8'))

    def render_html(self):
        template = self.env.get_template('base.html')
        random = randint(100000000, 999999999)
        carelist = list()
        for file in listdir(self.libdir+"/templates"):
            if file.endswith(".js"):
                    carelist.append(file)

        output = template.render(randint=random, js=carelist, quotes=self.quoteOBJ.quoteDB)
        with open(self.wwwdir+'/index.html', 'w') as f:
            f.write(output.encode('utf-8'))
            f.close()
