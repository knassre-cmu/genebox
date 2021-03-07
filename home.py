from cmu_112_graphics import *
import math, random, numpy

class Home(Mode):
    def appStarted(app):
        app.vDict = {}
        app.granularity = 10
        app.rows = 40
        app.cols = 40
        app.cw = app.width / app.cols
        app.ch = app.height / app.rows
        app.grid = app.perlinNoise(app.rows, app.cols)
        app.t = 0
        app.mx, app.my = 0, 0

    def modeActivated(app):
        app.mx, app.my = 0, 0

    def interpolate(app, a, b, w):
        return (b - a) * (3 - w * 2) * w **2 + a

    def randomGradient(app, x, y):
        if (x, y) not in app.vDict:
            theta0 = random.random() * math.tau
            theta1 = random.random() * math.tau
            theta2 = random.random() * math.tau
            radius1 = 0.9 * random.random() / 5
            radius2 = 0.9 * random.random() / 5
            radius3 = 0.9 * random.random() / 5
            gradient = []
            gradient.append ((radius1 * math.cos(theta0), radius1 * math.sin(theta0)))
            gradient.append ((radius2 * math.cos(theta1), radius2 * math.sin(theta1)))
            gradient.append ((radius3 * math.cos(theta2), radius3 * math.sin(theta2)))
            app.vDict[(x, y)] = numpy.array(gradient)
        return app.vDict[(x, y)]

    def dotGridGradient(app, x0, y0, x, y):
        gradient = app.randomGradient(x0, y0)
        dx = x - x0
        dy = y - y0
        return dx * gradient[:,0] + dy * gradient[:,1]
    
    def perlinNoise(app, rows, cols):
        # Initialize the empty grid, the global min/max of each color, and a dictionary
        # that will be used to store random direction vectors for each location
        A = numpy.array([[[0.0, 0.0, 0.0] for c in range(cols)] for r in range(rows)])
        rMin, rMax = float("inf"), float("-inf")
        gMin, gMax = float("inf"), float("-inf")
        bMin, bMax = float("inf"), float("-inf")
        vDict = {}
        
        # Loop over each cell
        for r in range(rows):
            for c in range(cols):
                # Repeating the process with 3 different scales
                for scale in [0.7, 0.8, 0.9]:
                    
                    # Scale down the cell to a float value then extract the (x, y)
                    # values reprsenting the 4 nearest tiles
                    x, y = c / (cols ** scale), r / (rows ** scale)
                    x0, y0 = int(x), int(y)
                    x1, y1 = x0 + 1, y0 + 1
                    dx = x - x0
                    dy = y - y0

                    # Use the dot product of the scaled cell with each of the four
                    # points' direction vectors to create the interpolated value
                    n0 = app.dotGridGradient(x0, y0, x, y)
                    n1 = app.dotGridGradient(x1, y0, x, y)
                    ix0 = app.interpolate(n0, n1, dx)

                    n0 = app.dotGridGradient(x0, y1, x, y)
                    n1 = app.dotGridGradient(x1, y1, x, y)
                    ix1 = app.interpolate(n0, n1, dx)

                    value = app.interpolate(ix0, ix1, dy)
                    A[r, c] += value
                
        # Calculate the global min/max of each color
        rMin = numpy.min(A[:, :, 0])
        rMax = numpy.max(A[:, :, 0])
        gMin = numpy.min(A[:, :, 1])
        gMax = numpy.max(A[:, :, 1])
        bMin = numpy.min(A[:, :, 2])
        bMax = numpy.max(A[:, :, 2])
            
        # Adjust each color so that it is between 0 and 1 based on the global min/max
        for i in range(rows):
            for j in range(cols):
                A[i, j, 0] -= rMin - abs(rMin / 10)
                A[i, j, 0] /= (rMax - rMin) * 1.1
                A[i, j, 1] -= gMin - abs(gMin / 10)
                A[i, j, 1] /= (gMax - gMin) * 1.1
                A[i, j, 2] -= bMin - abs(bMin / 10)
                A[i, j, 2] /= (bMax - bMin) * 1.1
                    
        return A

    def timerFired(app):
        app.t += 0.05

    def mouseMoved(app, event):
        app.mx, app.my = event.x, event.y

    def mousePressed(app, event):
        app.mx, app.my = event.x, event.y
        if app.mouseInsideDiamond1():
            app.app.setActiveMode(app.app.ioPage)
        elif app.mouseInsideDiamond2():
            app.app.setActiveMode(app.app.query)

    def mouseInsideDiamond1(app):
        if app.mx < app.width * 0.55: return False
        if app.mx > app.width * 0.65: return False
        if app.my < app.height * 0.65: return False
        if app.my > app.height * 0.75: return False
        if app.height * 0.7 - app.my > app.mx - app.width * 0.55: return False
        if app.height * 0.7 - app.my < app.mx - app.width * 0.65: return False
        if app.my - app.height * 0.7 > app.mx - app.width * 0.55: return False
        if app.my - app.height * 0.7 < app.mx - app.width * 0.65: return False
        return True

    def mouseInsideDiamond2(app):
        if app.mx < app.width * 0.35: return False
        if app.mx > app.width * 0.45: return False
        if app.my < app.height * 0.65: return False
        if app.my > app.height * 0.75: return False
        if app.height * 0.7 - app.my > app.mx - app.width * 0.35: return False
        if app.height * 0.7 - app.my < app.mx - app.width * 0.45: return False
        if app.my - app.height * 0.7 > app.mx - app.width * 0.35: return False
        if app.my - app.height * 0.7 < app.mx - app.width * 0.45: return False
        return True

    def shiftColor(app, r, g, b):
        r = 0.4 * (1.25 + math.sin(math.tau * r + app.t))
        g = 0.4 * (1.25 + math.sin(math.tau * g + app.t))
        b = 0.4 * (1.25 + math.sin(math.tau * b + app.t))
        return int(255 * r), int(255 * g), int(255 * b)

    def drawGrid(app, canvas):
        for row in range(app.rows):
            for col in range(app.cols):
                x0, y0 = col * app.cw, row * app.ch
                x1, y1 = x0 + app.cw, y0 + app.ch
                r, g, b = app.shiftColor(*app.grid[row, col])
                color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
                canvas.create_line(x0, y0, x1, y1, fill=color, width=app.ch)

    def drawButtons(app, canvas):
        xl, xr, y0 = app.width * 0.4, app.width * 0.6, app.height * 0.7
        r1 = app.width * 0.05
        r2 = app.width * 0.045
        r3 = app.width * 0.04
        color1A, color1B = "#333333", "#eeeeee"
        color2A, color2B = "#333333", "#eeeeee"
        if app.mouseInsideDiamond1(): color1A, color1B = color1B, color1A
        if app.mouseInsideDiamond2(): color2A, color2B = color2B, color2A
        canvas.create_polygon(xr-r1, y0, xr, y0-r1, xr+r1, y0, xr, y0+r1, fill=color1A)
        canvas.create_polygon(xr-r2, y0, xr, y0-r2, xr+r2, y0, xr, y0+r2, fill=color1B)
        canvas.create_polygon(xr-r3, y0, xr, y0-r3, xr+r3, y0, xr, y0+r3, fill=color1A)
        canvas.create_polygon(xl-r1, y0, xl, y0-r1, xl+r1, y0, xl, y0+r1, fill=color2A)
        canvas.create_polygon(xl-r2, y0, xl, y0-r2, xl+r2, y0, xl, y0+r2, fill=color2B)
        canvas.create_polygon(xl-r3, y0, xl, y0-r3, xl+r3, y0, xl, y0+r3, fill=color2A)
        canvas.create_text(xl, y0, text="Search", font="Futura 8 bold", fill=color2B)
        canvas.create_text(xr, y0, text="Create", font="Futura 8 bold", fill=color1B)

    def drawHeader(app, canvas):
        canvas.create_text(app.width * 0.5, app.height * 0.4, text="GENEBOX",
        fill="#eeeeee", font="Futura 128 bold")

    def redrawAll(app, canvas):
        app.drawGrid(canvas)
        app.drawButtons(canvas)
        app.drawHeader(canvas)