from cmu_112_graphics import *
import math, random, numpy

class Genome3D(Mode):
    def appStarted(app):
        app.nucleotides = app.app.currentGenome.sequence
        app.index = 0
        app.maxPairs = 22
        app.t = 0
        app.polygons = []
        app.text = []
        
        app.x0 = app.width * 0.3
        app.y0 = app.height * -0.05
        app.r = app.width * 0.4
        app.dt = 0.1
        app.lw = 0.01
        
        app.location = [0.0, 10.0, 5.0]
        app.lookAt = [0.0, 0.0, 0.0]
        app.setupProjection()
        
        app.scrollX = app.width * 0.9
        app.buttonWidth = app.width * 0.15
        app.buttonHeight = app.width * 0.075
        app.mx, app.my = 0, 0

    def modeActivated(app):
        app.mx, app.my = 0, 0

    def modeActivated(app):
        app.nucleotides = app.app.currentGenome.sequence

    def setupProjection(app):
        forwardVector = numpy.array(app.location) - numpy.array(app.lookAt)
        forwardVector /= numpy.linalg.norm(forwardVector)
        rightVector = numpy.cross(forwardVector, numpy.array([0, 1, 0]))
        upVector = numpy.cross(forwardVector, rightVector)
        app.M = numpy.array([
        [  rightVector[0],   rightVector[1],   rightVector[2], 0],
        [     upVector[0],      upVector[1],      upVector[2], 0],
        [forwardVector[0], forwardVector[1], forwardVector[2], 0],
        [ app.location[0],  app.location[1],  app.location[2], 1]])

    def timerFired(app):
        app.t += 0.1 
        app.calculatePositions()

    def mouseDragged(app, event):
        if event.x > app.scrollX:
            i = int((event.y / app.height) * (len(app.nucleotides) - app.maxPairs))
            app.t += (i - app.index) * 0.37
            app.index = i
        app.mx, app.my = event.x, event.y

    def mouseMoved(app, event):
        app.mx, app.my = event.x, event.y

    def mousePressed(app, event):
        app.mx, app.my = event.x, event.y
        if app.scrollX - app.buttonWidth < app.mx < app.scrollX:
            if app.height - app.buttonHeight < app.my:
                if app.app.prevMode == "Editor":
                    app.app.setActiveMode(app.app.editor)
                elif app.app.prevMode == "Query":
                    app.app.setActiveMode(app.app.query)

    def keyPressed(app, event):
        if event.key == "Up" and app.index > 0:
            app.index -= 1
            app.t -= 0.37
        elif event.key == "Down" and app.index < len(app.nucleotides) - app.maxPairs:
            app.index += 1
            app.t += 0.37
        elif event.key == "Left" and app.x0 > app.width * 0.2:
            app.x0 -= 5
        elif event.key == "Right" and app.x0 < app.width * 0.8:
            app.x0 += 5

    def getColors(app, i):
        base = app.nucleotides[app.index + i]
        if base == "C":
            return "#880000", "#CC0000", "#BB2200", "#885500", "#CC9900", "#CC9966"
        elif base == "G":
            return "#885500", "#CC9900", "#CC9966", "#880000", "#CC0000", "#BB2200"
        elif base == "T":
            return "#008855", "#00BB99", "#44CC88", "#005588", "#0099CC", "#4488BB"
        elif base == "A":
            return "#005588", "#0099CC", "#4488BB", "#008855", "#00CC99", "#44BB88"
        else:
            return "#550088", "#9900CC", "#8844BB", "#550088", "#8844BB", "#9900CC"

    def calculatePositions(app):
        app.polygons = []
        app.text = []
        for i in range(app.maxPairs-1, -1, -1):
            t = app.t + i * 0.37
            x1, y1 = math.cos(t), math.sin(t)
            x1L, y1L = 0.1*math.cos(t-math.pi/2), 0.1*math.sin(t-math.pi/2)
            x1R, y1R = 0.1*math.cos(t+math.pi/2), 0.1*math.sin(t+math.pi/2)
            x2, y2 = math.cos(t-app.dt), math.sin(t-app.dt)
            x3, y3 = math.cos(t+app.dt), math.sin(t+app.dt)
            x4, y4 = math.cos(t+math.pi), math.sin(t+math.pi)
            x5, y5 = math.cos(t-app.dt+math.pi), math.sin(t-app.dt+math.pi)
            x6, y6 = math.cos(t+app.dt+math.pi), math.sin(t+app.dt+math.pi)
            xpL, ypL = math.cos(t+math.pi-0.37), math.sin(t+math.pi-0.37)
            xpR, ypR = math.cos(t-0.37), math.sin(t-0.37)
            z1 = 0.1 - i / 3
            z2 = - i / 3
            z3 = -0.1 - i / 3
            
            xcT, ycT = app.project(0, 0, z1)
            xcB, ycB = app.project(0, 0, z3)
            xcL, ycL = app.project(x1L, y1L, z2)
            xcR, ycR = app.project(x1R, y1R, z2)

            xlT, ylT = app.project(x1, y1, z1)
            xlB, ylB = app.project(x1, y1, z3)
            xlL, ylL = app.project(x2, y2, z2)
            xlR, ylR = app.project(x3, y3, z2)

            xrT, yrT = app.project(x4, y4, z1)
            xrB, yrB = app.project(x4, y4, z3)
            xrL, yrL = app.project(x6, y6, z2)
            xrR, yrR = app.project(x5, y5, z2)

            xpL, ypL = app.project(xpL, ypL, z2 + 1/3)
            xpR, ypR = app.project(xpR, ypR, z2 + 1/3)

            bColor1, lColor1, rColor1, bColor2, lColor2, rColor2 = app.getColors(i)

            if yrT < ylT:
                if xlT < xcT:
                    app.polygons.append([xlB, ylB, xlR, ylR, xcR, ycR, xcB, ycB, bColor1])
                else:
                    app.polygons.append([xlB, ylB, xlL, ylL, xcL, ycL, xcB, ycB, bColor1])
                if xlT < xrT:
                    app.polygons.append([xlT, ylT, xlL, ylL, xcL, ycL, xcT, ycT, rColor1])
                    app.polygons.append([xlT, ylT, xlR, ylR, xcR, ycR, xcT, ycT, lColor1])
                else:
                    app.polygons.append([xlT, ylT, xlR, ylR, xcR, ycR, xcT, ycT, lColor1])
                    app.polygons.append([xlT, ylT, xlL, ylL, xcL, ycL, xcT, ycT, rColor1])
                app.polygons.append([-app.lw, ycB, app.lw, ycB, app.lw, ycT+0.1, -app.lw, ycT+0.1, "Black"])
                app.polygons.append([xlT, ylT, xlL, ylL, xpR+0.02, ypR, xpR-0.02, ypR, "Black"])
            else:
                app.polygons.append([xrB, yrB, xrL, yrL, xpL-0.02, ypL, xpL+0.02, ypL, "Black"])
            
            app.polygons.append([xrB, yrB, xrR, yrR, xcR, ycR, xcB, ycB, bColor2])
            app.polygons.append([xrB, yrB, xrL, yrL, xcL, ycL, xcB, ycB, bColor2])
            if xlT < xrT:
                app.polygons.append([xrT, yrT, xrL, yrL, xcL, ycL, xcT, ycT, rColor2])
                app.polygons.append([xrT, yrT, xrR, yrR, xcR, ycR, xcT, ycT, lColor2])
            else:
                app.polygons.append([xrT, yrT, xrR, yrR, xcR, ycR, xcT, ycT, lColor2])
                app.polygons.append([xrT, yrT, xrL, yrL, xcL, ycL, xcT, ycT, rColor2])
            if ylT > ycT:
                app.polygons.append([xrT, yrT, xrL, yrL, xrB, yrB, xrR, yrR, "Black"])
                if ylT > ycT + 0.13:
                    x = app.x0 + app.r * xrT
                    y = app.y0 - app.r * yrL
                    app.text.append((x, y, app.nucleotides[app.index + i]))
                app.polygons.append([xrB, yrB, xrL, yrL, xpL+0.02, ypL, xpL-0.02, ypL, "Black"])

            if yrT > ylT:
                app.polygons.append([-app.lw, ycB, app.lw, ycB, app.lw, ycT+0.1, -app.lw, ycT+0.1, "Black"])
                app.polygons.append([xlB, ylB, xlR, ylR, xcR, ycR, xcB, ycB, bColor1])
                app.polygons.append([xlB, ylB, xlL, ylL, xcL, ycL, xcB, ycB, bColor1])
                if xlT < xrT:
                    app.polygons.append([xlT, ylT, xlL, ylL, xcL, ycL, xcT, ycT, rColor1])
                    app.polygons.append([xlT, ylT, xlR, ylR, xcR, ycR, xcT, ycT, lColor1])
                else:
                    app.polygons.append([xlT, ylT, xlR, ylR, xcR, ycR, xcT, ycT, lColor1])
                    app.polygons.append([xlT, ylT, xlL, ylL, xcL, ycL, xcT, ycT, rColor1])
                if yrT > ycT:
                    app.polygons.append([xlT, ylT, xlL, ylL, xlB, ylB, xlR, ylR, "Black"])
                    if yrT > ycT + 0.13:
                        x = app.x0 + app.r * xlT
                        y = app.y0 - app.r * ylL
                        app.text.append((x, y, app.nucleotides[app.index + i]))
                app.polygons.append([xlT, ylT, xlL, ylL, xpR-0.02, ypR, xpR+0.02, ypR, "Black"])

        for i in range(len(app.polygons)):
            for j in range(0, len(app.polygons[i])-1, 2):
                app.polygons[i][j] = app.x0 + app.r * app.polygons[i][j] 
                app.polygons[i][j+1] = app.y0 - app.r * app.polygons[i][j+1] 

    def project(app, x, y, z):
        projection = app.M @ numpy.array([x, y, z, 1])
        return projection[0], projection[1]

    def renderNucleotides(app, canvas):
        for poly in app.polygons:
            canvas.create_polygon(*poly[:-1], fill=poly[-1])
        for x, y, t in app.text:
            canvas.create_text(x, y, text=t, fill="White", font="Times 8")

    def renderScrollbar(app, canvas):
        canvas.create_rectangle(app.scrollX, 0, app.width, app.height, fill="#dddddd", width=0)
        yC = (app.index / (len(app.nucleotides) - app.maxPairs)) * app.height
        x0 = app.scrollX + app.width * 0.02
        y0 = yC - (app.width - app.scrollX) / 2 + app.width * 0.02
        x1 = app.width - app.width * 0.02
        y1 = yC + (app.width - app.scrollX) / 2 - app.width * 0.02
        canvas.create_oval(x0, y0, x1, y1, fill="#bbbbbb", width=0)

    def renderButtons(app, canvas):
        canvas.create_rectangle(app.scrollX - app.buttonWidth, app.height - app.buttonHeight,
        app.scrollX, app.height, fill="#dd6666", width=0)
        poly = [app.scrollX - app.buttonWidth * 0.65, app.height - app.buttonHeight * 0.5,
                app.scrollX - app.buttonWidth * 0.35, app.height - app.buttonHeight * 0.7,
                app.scrollX - app.buttonWidth * 0.35, app.height - app.buttonHeight * 0.3]
        if app.scrollX - app.buttonWidth < app.mx < app.scrollX:
            if app.height - app.buttonHeight < app.my:
                for i in range(0, len(poly), 2):
                    poly[i] += 10 * math.sin(3*app.t)
        canvas.create_polygon(*poly, fill="White", width=0)

    def redrawAll(app, canvas):
        app.renderNucleotides(canvas)
        app.renderScrollbar(canvas)
        app.renderButtons(canvas)