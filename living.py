from geneSockets import *

class Living(object):
    def __init__(self, name, x, y0, y1, sockets):
        self.name = name
        self.x = x
        self.y0 = y0
        self.y1 = y1
        self.sockets = sockets
        self.initial = []
        for socket in self.sockets:
            self.initial.append([x, y0 + (y1 - y0) * socket.y])
        self.reset()

    def reset(self):
        for i in range(len(self.sockets)):
            x, y = self.initial[i]
            self.sockets[i] = GeneSocket(self.sockets[i].socketType, "Empty", "", x, y)

    def render(self, canvas, r):
        canvas.create_line(self.x, self.y0, self.x, self.y1, fill="#333333", width=12)
        canvas.create_line(self.x, self.y0, self.x, self.y1, fill="#dddddd", width=10)
        canvas.create_line(self.x, self.y0, self.x, self.y1, fill="#333333", width=8)
        for socket in self.sockets:
            socket.render(canvas, r)
        canvas.create_rectangle(self.x - 2 * r, self.y0, self.x + 2 * r, self.y0 + r,
        fill="#333333", width=0)
        canvas.create_rectangle(self.x - 2 * r + 6, self.y0 + 6, self.x + 2 * r - 6, self.y0 + r - 6,
        fill="#333333", outline="#dddddd", width=3)
        canvas.create_text(self.x, self.y0 + r / 2, text=self.name, font = "Futura 40",
        fill="#dddddd")