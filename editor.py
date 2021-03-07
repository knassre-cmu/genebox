from cmu_112_graphics import *
from geneSockets import *
import math, random, numpy

class Editor(Mode):
    def appStarted(app):
        app.genome = app.app.currentGenome
        app.sockets = [
            GeneSocket("Light", "Red", "", 525, 100),
            GeneSocket("Light", "Orange", "", 625, 100),
            GeneSocket("Light", "Yellow", "", 725, 100),
            GeneSocket("Light", "Green", "", 825, 100),
            GeneSocket("Light", "Cyan", "", 925, 100)]
        app.r = 40
        app.holding = None

    def modeActivated(app):
        app.genome = app.app.currentGenome

    def mousePressed(app, event):
        for socket in app.sockets:
            if ((event.x - socket.x)**2 + (event.y - socket.y)**2)**0.5 < app.r
        if event.x < app.width / 2:
            app.app.setActiveMode(app.app.ioPage)
        if event.x > app.width / 2:
            app.app.prevMode = "Editor"
            app.app.setActiveMode(app.app.genome3D)

    def redrawAll(app, canvas):
        canvas.create_text(app.width * 0.25, app.height * 0.5, text="To Selector")
        canvas.create_text(app.width * 0.75, app.height * 0.5, text="To Visualizer")
        for socket in app.sockets:
            socket.render(canvas, app.r)