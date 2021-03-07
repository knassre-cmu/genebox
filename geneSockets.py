class GeneSocket(object):
    def __init__(self, socketType, phenotype, sequence, x, y):
        self.socketType = socketType
        self.phenotype = phenotype
        self.sequence = sequence
        self.x, self.y = x, y

    def render(self, canvas, r):
        if self.socketType == "Light":
            if self.phenotype == "Red":
                color = "#b52b1f"
            elif self.phenotype == "Orange":
                color = "#edad4c"
            elif self.phenotype == "Yellow":
                color = "#dad541"
            elif self.phenotype == "Green":
                color = "#67f065"
            if self.phenotype == "Cyan":
                color = "#47acf5"
            canvas.create_polygon(self.x, self.y - r, self.x + r, self.y + r * 0.8,
            self.x - r, self.y + r * 0.8, fill=color, width=0)
            canvas.create_text(self.x, self.y + 5, fill="#eeeeee", text=self.phenotype,
            font="Futura 10 bold")