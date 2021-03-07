from cmu_112_graphics import *
from geneSockets import *
from living import *
import math, random, numpy

class Editor(Mode):
    def appStarted(app):
        app.genome = app.app.currentGenome
        app.resetSockets()
        app.r = 40
        app.t = 0
        app.buttonWidth = app.width * 0.15
        app.buttonHeight = app.width * 0.075
        app.mx, app.my = 0, 0
        app.holding = None
        app.initBases()

    def modeActivated(app):
        app.genome = app.app.currentGenome
        app.resetSockets()
        app.initBases()

    def getBuiltinSequence(app, name):
        return "ACTGN" * 10

    def resetSockets(app):
        app.sockets = [
            GeneSocket("Light", "Red", app.getBuiltinSequence("Red Biolum"), 525, 100),
            GeneSocket("Light", "Orange", app.getBuiltinSequence("Orange Biolum"), 625, 100),
            GeneSocket("Light", "Yellow", app.getBuiltinSequence("Yellow Biolum"), 725, 100),
            GeneSocket("Light", "Green", app.getBuiltinSequence("Green Biolum"), 825, 100),
            GeneSocket("Light", "Cyan", app.getBuiltinSequence("Cyan Biolum"), 925, 100),
            GeneSocket("Milk", "Spider", app.getBuiltinSequence("Spider Milk"), 625, 200),
            GeneSocket("Milk", "Lactase", app.getBuiltinSequence("Lactase Milk"), 725, 200),
            GeneSocket("Milk", "Insulin", app.getBuiltinSequence("Insulin Milk"), 825, 200),
            GeneSocket("Blood", "AB", app.getBuiltinSequence("AB Blood"), 575, 300),
            GeneSocket("Blood", "A", app.getBuiltinSequence("A Blood"), 675, 300),
            GeneSocket("Blood", "B", app.getBuiltinSequence("B Blood"), 775, 300),
            GeneSocket("Blood", "O", app.getBuiltinSequence("O Blood"), 875, 300),
            GeneSocket("Flower", "Yellow", app.getBuiltinSequence("Yellow Flower"), 675, 400),
            GeneSocket("Flower", "Purple", app.getBuiltinSequence("Purple Flower"), 775, 400),
            GeneSocket("Stem", "Tall", app.getBuiltinSequence("Tall Stem"), 675, 500),
            GeneSocket("Stem", "Dwarf", app.getBuiltinSequence("Dwarf Stem"), 775, 500),
            GeneSocket("Pod", "Yellow", app.getBuiltinSequence("Yellow Pod"), 675, 600),
            GeneSocket("Pod", "Green", app.getBuiltinSequence("Green Pod"), 775, 600)]
        
    def initBases(app):
        app.jellyfish = Living("Jellyfish", 200, 0, app.height,
            [GeneSocket("Light", "Empty", "", None, 0.5)])
        app.goat = Living("Goat", 200, 0, app.height,
            [GeneSocket("Milk", "Empty", "", None, 0.3),
             GeneSocket("Light", "Empty", "", None, 0.5),
             GeneSocket("Blood", "Empty", "", None, 0.7)])
        app.pea = Living("Pea Plant", 200, 0, app.height,
            [GeneSocket("Flower", "Empty", "", None, 0.3),
             GeneSocket("Stem", "Empty", "", None, 0.5),
             GeneSocket("Pod", "Empty", "", None, 0.7)])
        app.bases = [app.jellyfish, app.goat, app.pea]

    def mousePressed(app, event):
        app.mx, app.my = event.x, event.y
        for socket in app.sockets:
            if ((event.x - socket.x)**2 + (event.y - socket.y)**2)**0.5 < app.r:
                app.holding = socket
                return
        for socket in app.bases[0].sockets:
            if ((event.x - socket.x)**2 + (event.y - socket.y)**2)**0.5 < 2 * app.r:
                if socket.phenotype == "Empty": continue
                app.app.currentGenome.sequence = socket.sequence
                app.app.prevMode = "Editor"
                app.app.setActiveMode(app.app.genome3D)
                return

    def mouseDragged(app, event):
        app.mx, app.my = event.x, event.y
        if app.holding != None:
            app.holding.x, app.holding.y = event.x, event.y

    def mouseMoved(app, event):
        app.mx, app.my = event.x, event.y

    def mouseReleased(app, event):
        app.mx, app.my = event.x, event.y
        if app.holding != None:
            for i, socket in enumerate(app.bases[0].sockets):
                if app.bases[0].sockets[i].socketType != app.holding.socketType:
                    continue
                if ((event.x - socket.x)**2 + (event.y - socket.y)**2)**0.5 < 1.5 * app.r:
                    app.holding.x = app.bases[0].sockets[i].x
                    app.holding.y = app.bases[0].sockets[i].y
                    app.bases[0].sockets[i] = app.holding
                    app.resetSockets()
                    break
            app.holding = None
        

    def timerFired(app):
        app.t += 0.1

    def keyPressed(app, event):
        if event.key == "Right":
            app.bases[0].reset()
            app.resetSockets()
            app.bases.append(app.bases.pop(0))
        elif event.key == "Left":
            app.bases[0].reset()
            app.resetSockets()
            app.bases.insert(0, app.bases.pop(-1))

    def renderButtons(app, canvas):
        canvas.create_rectangle(app.width - app.buttonWidth, app.height - app.buttonHeight,
        app.width, app.height, fill="#dd6666", width=0)
        poly = [app.width - app.buttonWidth * 0.65, app.height - app.buttonHeight * 0.5,
                app.width - app.buttonWidth * 0.35, app.height - app.buttonHeight * 0.7,
                app.width - app.buttonWidth * 0.35, app.height - app.buttonHeight * 0.3]
        if app.width - app.buttonWidth < app.mx:
            if app.height - app.buttonHeight < app.my:
                for i in range(0, len(poly), 2):
                    poly[i] += 10 * math.sin(3*app.t)
        canvas.create_polygon(*poly, fill="White", width=0)

    def redrawAll(app, canvas):
        app.bases[0].render(canvas, 2 * app.r)
        for socket in app.sockets:
            socket.render(canvas, app.r)
        app.renderButtons(canvas)