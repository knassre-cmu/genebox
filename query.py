from cmu_112_graphics import *
import math
import requests
import bs4

# requires bs4 and lxml pip installs

def searchGenes(searchTerm):
    searchArgs = {"db": "Gene", "term": searchTerm, "sort": "relevance"}
    apiSearch = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi', params=searchArgs)
    searchSoup = bs4.BeautifulSoup(apiSearch.content, "xml")
    idList = searchSoup.find("IdList")
    ids = idList.find_all("Id")

    allResults = []
    for ID in ids:
        allResults.append(ID.text)

    # Get the top result from your search query and extract the Gene ID
    topResultID = allResults[0]
    return topResultID, allResults

def getGeneSeqIDAndRange(resultID):
    # use the Gene ID in a fetch request
    geneEntryArgs = {"db": "Gene", "id": resultID, "retmode": "xml"}
    apiGeneEntry = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params=geneEntryArgs)

    # And get the ID for the gene sequence from the db entry
    geneSoup = bs4.BeautifulSoup(apiGeneEntry.content, "xml")
    # the last listing on the xml file corresponds to the gene location
    geneSeqID = geneSoup.find_all("Gene-commentary_accession")[-1].text
    lineanName = geneSoup.find("Org-ref_taxname").text
    orgName = geneSoup.find("Org-ref_common").text if geneSoup.find("Org-ref_common") else ""
    locusName = geneSoup.find("Gene-ref_locus").text

    # then find that actual sequence positions (we'll use these in a minute)
    # assuming it's the last listed sequence range in the xml file
    seqIntervalFrom = int(geneSoup.find_all("Seq-interval_from")[-1].text)
    seqIntervalTo = int(geneSoup.find_all("Seq-interval_to")[-1].text)
    if orgName == "":
        return locusName, lineanName, geneSeqID, seqIntervalFrom, seqIntervalTo
    return locusName, orgName, geneSeqID, seqIntervalFrom, seqIntervalTo

def getAssemblySeq(geneSeqID):
    geneEntryArgs = {"db": "nuccore", "id": geneSeqID, "rettype": "fasta", 
        "retmode": "text"}
    apiAssemblyEntry = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params=geneEntryArgs)
    assemblyFasta = apiAssemblyEntry.text
    # there's the fasta label at the top of the file that we need to ignore
    assemblyFastaAnnotEnd = assemblyFasta.find('\n') 
    assemblySeq = assemblyFasta[(assemblyFastaAnnotEnd + 1):]
    # newline characters mess up the indexing so we need to remove those
    assemblySeq = assemblySeq.replace("\n", "")
    return assemblySeq

def getGeneSeq(assemblySeq, seqIntervalFrom, seqIntervalTo):
    geneSeq = assemblySeq[seqIntervalFrom:seqIntervalTo + 1]
    return geneSeq

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
        app.searchResults = []

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
        topResultID, allResults = searchGenes(app.qString)
        app.searchResults = []
        for result in allResults:
            try: app.searchResults.append(getGeneSeqIDAndRange(result))
            except: pass

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
                    name, org, geneSeqID, seqIntervalFrom, seqIntervalTo = app.searchResults[i]
                    assemblySeq = getAssemblySeq(geneSeqID)
                    geneSeq = getGeneSeq(assemblySeq, seqIntervalFrom, seqIntervalTo)
                    app.app.selectName = f"{name} ({org})"
                    app.app.currentGenome.sequence = geneSeq + "N" * 25
                    app.app.prevMode = "Query"
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
        text = f"{len(app.searchResults)} results found", font="Futura 16 bold")
        x0 = app.width - app.sx
        y0 = app.sy + 2 * app.r
        w = 8 * app.r
        for i in range(min(len(app.searchResults), app.maxSearches)):
            color1, color2 = "#333333", "#dddddd"
            if x0 <= app.mx <= x0 + w and y0 <= app.my <= y0 + app.r:
                color1, color2 = color2, color1
            canvas.create_rectangle(x0, y0, x0 + w, y0 + app.r,
            fill=color1, width=0)
            text = f"{app.searchResults[i][0]} ({app.searchResults[i][1]})"
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