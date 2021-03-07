class GenomeObject(object):
    def fromFile(path):
        with open("gfiles/" + path, "r") as f:
            text = f.read()
        G = GenomeObject()
        for line in text.splitlines():
            feature, value = line.split(": ")
            if feature == "TITLE": G.title = value
            elif feature == "BASEGENOME": G.base = value
            elif feature == "LIGHT_SPLICE": G.light = value
            elif feature == "MILK_SPLICE": G.milk = value
            elif feature == "SEQUENCE": G.sequence = value
        return G

    def __init__(self):
        self.title = "?"
        self.base = "?"
        self.light = "?"
        self.milk = "?"
        self.sequence = "AAAACCCCTTTTGGGG" * 5

    def __repr__(self):
        s = ""
        s += f"TITLE: {self.title}\n"
        s += f"BASEGENOME: {self.base}\n"
        s += f"LIGHT_SPLICE: {self.light}\n"
        s += f"MILK_SPLICE: {self.milk}\n"
        s += f"SEQUENCE: {self.sequence}"
        return s