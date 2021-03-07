from cmu_112_graphics import *
from genomeObject import *
from genome3D import *
from ioPage import *
from editor import *
from query import *
from home import *

class GenomeRenderer(ModalApp):
    def appStarted(app):
        app.currentGenome = GenomeObject()
        app.home = Home()
        app.query = Query()
        # app.ioPage = IOPage()
        app.editor = Editor()
        app.genome3D = Genome3D()
        app.setActiveMode(app.home)

    def appStopped(app):
        os._exit(0)

GenomeRenderer(width=1000, height=1000)