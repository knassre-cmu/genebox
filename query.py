from cmu_112_graphics import *
import math

class Query(Mode):
    def appStarted(app):
        app.buttonWidth = app.width * 0.15
        app.buttonHeight = app.width * 0.075
        app.mx, app.my = 0, 0
        app.t = 0
        app.sx, app.sy = app.width * 0.8, app.height * 0.3
        app.r = app.width * 0.035
        app.qString = ""
        app.maxSearches = 22
        app.searchResults = [(chr(i)*(i%40), 1000+i) for i in range(97, 117)]

    def modeActivated(app):
        app.mx, app.my = 0, 0

    def keyPressed(app, event):
        if event.key == "Delete":
            app.qString = app.qString[:-1]
        elif event.key == "Space":
            app.qString += " "
        elif len(event.key) == 1:
            app.qString += event.key

    def timerFired(app):
        app.t += 0.1
        
    def mouseMoved(app, event):
        app.mx, app.my = event.x, event.y

    def search(app):
        pass

    def mousePressed(app, event):
        app.mx, app.my = event.x, event.y
        if app.width - app.buttonWidth < app.mx:
            if app.height - app.buttonHeight < app.my:
                app.app.setActiveMode(app.app.home)
                return
        elif ((app.mx-app.sx)**2 + (app.my-app.sy)**2)**0.5 < app.r:
            if app.qString != "":
                app.search()
                return
        x0 = app.width - app.sx
        y0 = app.sy + 2 * app.r
        w = 8 * app.r
        for i in range(len(app.searchResults)):
            if x0 <= app.mx <= x0 + w:
                if y0 <= app.my <= y0 + app.r:
                    app.app.selectName, app.app.selectId = app.searchResults[i]
                    print(f"SELECT: {app.searchResults[i]}")
                    app.app.prevMode = "query"
                    app.app.setActiveMode(app.app.genome3D)
            y0 += 1.5 * app.r
            if i == app.maxSearches // 2 - 1:
                x0 = app.width - app.sx + w + 2 * app.r
                y0 = app.sy + 2 * app.r

    def renderSearchbar(app, canvas):
        canvas.create_rectangle(app.sx, app.sy - app.r, app.width - app.sx, app.sy + app.r,
        fill="#dddddd", width=0)
        i = 30
        while True:
            textID = canvas.create_text(app.width - app.sx + app.r / 2, app.sy, text=app.qString[-i+1:],
            fill="#dddddd", font = "Futura 20", anchor="w")
            bounds = canvas.bbox(textID) 
            width = bounds[2] - bounds[0]
            if i > len(app.qString) or width > 2 * app.sx - app.width - 2.5 * app.r:
                break
            canvas.delete(textID)
            i += 1

        canvas.create_text(app.width - app.sx + app.r / 2, app.sy, text=app.qString[-i:],
        fill="#333333", font = "Futura 20", anchor="w")

    def renderResults(app, canvas):
        canvas.create_text(app.width / 2, app.height * 0.25, fill="#333333",
        text = f"{len(app.searchResults)} resuts found", font="Futura 16 bold")
        x0 = app.width - app.sx
        y0 = app.sy + 2 * app.r
        w = 8 * app.r
        for i in range(min(len(app.searchResults), app.maxSearches)):
            color1, color2 = "#333333", "#dddddd"
            if x0 <= app.mx <= x0 + w and y0 <= app.my <= y0 + app.r:
                color1, color2 = color2, color1
            canvas.create_rectangle(x0, y0, x0 + w, y0 + app.r,
            fill=color1, width=0)
            text = app.searchResults[i][0]
            while True:
                textID = canvas.create_text(x0 + w / 2, y0 + app.r / 2, text=text,
                fill=color1, font = "Futura 16")
                bounds = canvas.bbox(textID) 
                width = bounds[2] - bounds[0]
                if width < w - app.r:
                    break
                canvas.delete(textID)
                text = text[:-1]
            if len(text) < len(app.searchResults[i][0]):
                text += "..."
            canvas.create_text(x0 + w / 2, y0 + app.r / 2, text=text,
            fill=color2, font="Futura 16")
            y0 += 1.5 * app.r
            if i == app.maxSearches // 2 - 1:
                x0 = app.width - app.sx + w + 2 * app.r
                y0 = app.sy + 2 * app.r

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
        color1, color2 = "#333333", "#dddddd"
        if ((app.mx-app.sx)**2 + (app.my-app.sy)**2)**0.5 < app.r:
            color1, color2, = color2, color1
        canvas.create_oval(app.sx - app.r, app.sy - app.r, app.sx + app.r, app.sy + app.r,
        fill=color2, width=0)
        canvas.create_line(app.sx - app.r*0.1, app.sy - app.r*0.1, app.sx + app.r*0.5, app.sy + app.r*0.5,
        fill=color1, width=4)
        canvas.create_oval(app.sx - app.r*0.6, app.sy - app.r*0.6, app.sx + app.r*0.1, app.sy + app.r*0.1,
        outline=color1, fill=color2, width=4)

    def redrawAll(app, canvas):
        app.renderSearchbar(canvas)
        app.renderResults(canvas)
        app.renderButtons(canvas)