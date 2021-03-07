from cmu_112_graphics import *

class Select(Mode):
    def appStarted(app):
        pass

    def modeActivated(app):
        app.mx, app.my = 0, 0

    def mousePressed(app, event):
        if event.x < app.width / 2:
            app.app.setActiveMode(app.app.query)
        if event.x > app.width / 2:
            app.app.prevMode = "Select"
            app.app.setActiveMode(app.app.genome3D)

    def redrawAll(app, canvas):
        canvas.create_text(app.width * 0.50, app.height * 0.3, text=app.app.selectName)
        canvas.create_text(app.width * 0.50, app.height * 0.35, text=app.app.selectId)
        canvas.create_text(app.width * 0.25, app.height * 0.5, text="To Query")
        canvas.create_text(app.width * 0.75, app.height * 0.5, text="To Visualizer")