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
            elif feature == "BLOOD_SPLICE": G.blood = value
            elif feature == "FLOWER_SPLICE": G.flower = value
            elif feature == "POD_SPLICE": G.pod = value
            elif feature == "STEM_SPLICE": G.stem = value
            elif feature == "SEQUENCE": G.sequence = value
        return G

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.base = kwargs.get("base", "")
        self.light = kwargs.get("light", "")
        self.milk = kwargs.get("milk", "")
        self.milk = kwargs.get("blood", "")
        self.milk = kwargs.get("flower", "")
        self.milk = kwargs.get("pod", "")
        self.milk = kwargs.get("stem", "")
        self.sequence = "AAAACCCCTTTTGGGGNNNN" * 5

    def setSequence(self, sequence):
        self.sequence = sequence

    def __repr__(self):
        s = ""
        s += f"TITLE: {self.title}\n"
        s += f"BASEGENOME: {self.base}\n"
        s += f"LIGHT_SPLICE: {self.light}\n"
        s += f"MILK_SPLICE: {self.milk}\n"
        s += f"BLOOD_SPLICE: {self.blood}\n"
        s += f"FLOWER_SPLICE: {self.milk}\n"
        s += f"POD_SPLICE: {self.milk}\n"
        s += f"STEM_SPLICE: {self.milk}\n"
        s += f"SEQUENCE: {self.sequence}"
        return s