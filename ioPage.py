from cmu_112_graphics import *
from genomeObject import *
import math, random, numpy, os

class IOPage(Mode):
    def appStarted(app):
        app.by = app.height * 0.7
        app.xL = app.width * 0.35
        app.xR = app.width * 0.65
        app.bw = app.width * 0.1
        app.bh = app.width * 0.05
        app.sx = app.width * 0.15
        app.sy = app.height * 0.45
        app.sr = app.width * 0.075
        app.selectedGenome = ""
        app.makeGenome = False
        app.selecting = False
        app.editGenome = False
        app.gfiles = []

    def getSelection(app):
        app.gfiles = [f for f in os.listdir("gfiles") if f.endswith("txt")]
        app.gfiles.sort()

    def mousePressed(app, event):
        if app.selecting:
            if abs(event.x - app.sx) < app.sr:
                if abs(event.y - app.sy) < app.sr:
                    return
                if abs(event.y - app.sy + app.sr * 1.25) < app.sr * 0.5:
                    app.gfiles.insert(0, app.gfiles.pop())
                    return
                if abs(event.y - app.sy - app.sr * 1.25) < app.sr * 0.5:
                    app.gfiles.append(app.gfiles.pop(0))
                    return
        if abs(event.x - app.width / 2) < 2.5 * app.bw:
            if abs(event.y - app.height * 0.3) < app.height * 0.05:
                app.makeGenome = True
                app.selecting = False
                app.editGenome = False
                return
            elif abs(event.y - app.height * 0.45) < app.height * 0.05:
                app.makeGenome = False
                app.selecting = True
                app.getSelection()
                if app.gfiles != []: app.editGenome = True
                return
        if abs(event.x - app.xL) < app.bw / 2 and abs(event.y - app.by) < app.bh / 2:
            app.app.setActiveMode(app.app.home)
        if abs(event.x - app.xR) < app.bw / 2 and abs(event.y - app.by) < app.bh / 2:
            if app.editGenome:
                app.app.currentGenome = GenomeObject.fromFile(app.gfiles[0])
                app.app.setActiveMode(app.app.editor)
            elif app.makeGenome:
                app.app.currentGenome = GenomeObject()
                app.app.setActiveMode(app.app.editor)
        app.makeGenome = False
        app.selecting = False
        app.editGenome = False

    def drawButtons(app, canvas):
        makeColor = "#cccccc" if app.makeGenome else "#777777"
        canvas.create_rectangle(app.width / 2 - 2.5 * app.bw, app.height * 0.25,
        app.width / 2 + 2.5 * app.bw, app.height * 0.35, fill=makeColor, width=0)
        canvas.create_text(app.width / 2, app.height * 0.3, text="Make New Genome",
        font="Futura 32 bold", fill="White")

        editColor = "#cccccc" if app.editGenome else "#777777"
        canvas.create_rectangle(app.width / 2 - 2.5 * app.bw, app.height * 0.4,
        app.width / 2 + 2.5 * app.bw, app.height * 0.5, fill=editColor, width=0)
        canvas.create_text(app.width / 2, app.height * 0.45, text="Load Saved Genome",
        font="Futura 32 bold", fill="White")

        canvas.create_rectangle(app.xL - app.bw / 2, app.by - app.bh / 2,
        app.xL + app.bw / 2, app.by + app.bh / 2, fill="#333333")
        canvas.create_polygon(app.xL - app.bw / 5, app.by, app.xL + app.bw / 5,
        app.by - app.bh / 4, app.xL + app.bw / 5, app.by + app.bh / 4, fill="#cccccc")

        rightColor = "#cccccc" if app.editGenome or app.makeGenome else "#777777"
        canvas.create_rectangle(app.xR - app.bw / 2, app.by - app.bh / 2,
        app.xR + app.bw / 2, app.by + app.bh / 2, fill="#333333")
        canvas.create_polygon(app.xR + app.bw / 5, app.by, app.xR - app.bw / 5,
        app.by - app.bh / 4, app.xR - app.bw / 5, app.by + app.bh / 4, fill=rightColor)

    def drawSelections(app, canvas):
        canvas.create_rectangle(app.sx - app.sr, app.sy - app.sr, app.sx + app.sr,
        app.sy + app.sr, fill="#333333", width=0)
        text = "N/A" if app.gfiles == [] else app.gfiles[0][:-4]
        canvas.create_text(app.sx, app.sy, text=text, fill="#cccccc", font="Futura 32 bold")

        canvas.create_rectangle(app.sx - app.sr, app.sy - app.sr * 1.5, app.sx + app.sr,
        app.sy - app.sr * 1.1, fill="#333333", width=0)
        canvas.create_text(app.sx, app.sy - app.sr * 1.3, text="Scroll Up",
        fill="#cccccc", font="Futura 16 bold")

        canvas.create_rectangle(app.sx - app.sr, app.sy + app.sr * 1.5, app.sx + app.sr,
        app.sy + app.sr * 1.1, fill="#333333", width=0)
        canvas.create_text(app.sx, app.sy + app.sr * 1.3, text="Scroll Down",
        fill="#cccccc", font="Futura 16 bold")

    def redrawAll(app, canvas):
        app.drawButtons(canvas)
        if app.selecting: app.drawSelections(canvas)