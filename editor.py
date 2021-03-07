from cmu_112_graphics import *
import math, random, numpy

class Editor(Mode):
    def appStarted(app):
        app.genome = app.app.currentGenome

    def modeActivated(app):
        app.genome = app.app.currentGenome

    def mousePressed(app, event):
        if event.x < app.width / 2:
            app.app.setActiveMode(app.app.ioPage)
        if event.x > app.width / 2:
            app.app.prevMode = "Editor"
            app.app.setActiveMode(app.app.genome3D)

    def redrawAll(app, canvas):
        canvas.create_text(app.width * 0.25, app.height * 0.5, text="To Selector")
        canvas.create_text(app.width * 0.75, app.height * 0.5, text="To Visualizer")