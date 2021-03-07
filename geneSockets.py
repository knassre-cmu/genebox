class GeneSocket(object):
    def __init__(self, socketType, phenotype, sequence, x, y):
        self.socketType = socketType
        self.phenotype = phenotype
        self.sequence = sequence
        self.x, self.y = x, y

    def renderLight(self, canvas, r):
        if self.phenotype == "Red":
            color = "#b52b1f"
        elif self.phenotype == "Orange":
            color = "#edad4c"
        elif self.phenotype == "Yellow":
            color = "#dad541"
        elif self.phenotype == "Green":
            color = "#67d065"
        elif self.phenotype == "Cyan":
            color = "#47acf5"
        else:
            color = "#4f5969"
        canvas.create_polygon(self.x, self.y - r, self.x + r, self.y + r * 0.8,
        self.x - r, self.y + r * 0.8, fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y + 5, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def renderMilk(self, canvas, r):
        if self.phenotype == "Spider":
            color = "#919fb5"
        elif self.phenotype == "Lactase":
            color = "#91b593"
        elif self.phenotype == "Insulin":
            color = "#b09878"
        else:
            color = "#4f5969"
        canvas.create_polygon(self.x, self.y + r, self.x + r, self.y - r * 0.8,
        self.x - r, self.y - r * 0.8, fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y - 5, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def renderBlood(self, canvas, r):
        if self.phenotype == "AB":
            color = "#cf0f08"
        elif self.phenotype == "A":
            color = "#ab0903"
        elif self.phenotype == "B":
            color = "#ad2b0e"
        elif self.phenotype == "O":
            color = "#962006"
        else:
            color = "#4f5969"
        canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r,
        fill=color, width=0)
        canvas.create_rectangle(self.x - r, self.y + r, self.x, self.y,
        fill=color, width=0)
        canvas.create_rectangle(self.x + r, self.y - r, self.x, self.y,
        fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def renderFlower(self, canvas, r):
        if self.phenotype == "Yellow":
            color = "#dad541"
        elif self.phenotype == "Purple":
            color = "#9a1ac4"
        else:
            color = "#4f5969"
        canvas.create_polygon(self.x, self.y-r, self.x+r/5, self.y-r/5, self.x+r, self.y,
        self.x+r/5, self.y+r/5, self.x, self.y+r, self.x-r/5, self.y+r/5, self.x-r, self.y,
        self.x-r/5, self.y-r/5, fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def renderStem(self, canvas, r):
        if self.phenotype == "Tall":
            color = "#79d7d9"
        elif self.phenotype == "Dwarf":
            color = "#d779d9"
        else:
            color = "#4f5969"
        canvas.create_polygon(self.x-r/5, self.y-r, self.x+r/5, self.y-r,
        self.x+r/5, self.y-r/5, self.x+r, self.y-r/5, self.x+r, self.y+r/5,
        self.x+r/5, self.y+r/5, self.x+r/5, self.y+r/5, self.x+r/5, self.y+r,
        self.x-r/5, self.y+r, self.x-r/5, self.y+r/5, self.x-r, self.y+r/5,
        self.x-r, self.y-r/5, self.x-r/5, self.y-r/5, fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def renderPod(self, canvas, r):
        if self.phenotype == "Yellow":
            color = "#ccbe3d"
        elif self.phenotype == "Green":
            color = "#269146"
        else:
            color = "#4f5969"
        canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r,
        fill=color, width=0)
        if color == "#4f5969": return
        canvas.create_text(self.x, self.y, fill="#eeeeee", text=self.phenotype,
        font="Futura 10 bold")

    def render(self, canvas, r):
        if self.socketType == "Light":
            self.renderLight(canvas, r)
        elif self.socketType == "Milk":
            self.renderMilk(canvas, r)
        elif self.socketType == "Blood":
            self.renderBlood(canvas, r)
        elif self.socketType == "Flower":
            self.renderFlower(canvas, r)
        elif self.socketType == "Pod":
            self.renderPod(canvas, r)
        elif self.socketType == "Stem":
            self.renderStem(canvas, r)