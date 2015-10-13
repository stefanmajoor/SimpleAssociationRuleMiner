from Tkinter import *
from sets import Set

class App:
    def __init__(self, master):
        self.rows = 15
        self.columns = 4
        self.master = master
        self.update()
        self.matrixlabels = []


    '''
    Display all items
    '''
    def update(self):
        self.frame = Frame(self.master)
        ## How many values
        Label(self.master, text="Amount of Columns:").grid(row=0, column=0, columnspan=3)

        ## No idea why this works. But it does
        var = StringVar(root)
        var.set(str(self.columns))
        self.columnBox = Spinbox(self.master, from_=1, to=10, textvariable=str(var))
        self.columnBox.grid(row=0, column=3, columnspan=3)


        Button(self.master, text="Update", command=self.setFormat).grid(row=0, column=6)

        Label(self.master, text="Support").grid(row=1, column=0)
        self.support = Spinbox(self.master, from_=0.01, to=1, increment=0.01)
        self.support.grid(row=1, column=3, columnspan=3)

        Label(self.master, text="Confidence").grid(row=2, column=0)
        self.confidence = Spinbox(self.master, from_=0.01, to=1, increment=0.01)
        self.confidence.grid(row=2, column=3, columnspan=3)


        ## Display rows and columns

        self.entries = [[0. for i in range(self.columns)] for j in range(self.rows)]
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                self.entries[i][j] = Entry(self.master, width=15)
                self.entries[i][j].grid(row=i+3, column = j+2)

        Button(self.master, text="Find rules", command=self.findRules).grid(row=2, column=6, columnspan = 3)


    def setFormat(self):
        self.columns = int(self.columnBox.get())
        self.update()

    def findRules(self):
        words = dict()
        rows = Set()

        ## insert all commands
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                value = self.entries[i][j].get()
                values = value.split(',')

                for v in values:
                    if len(v) == 0:
                        continue
                    if v.strip() not in words:
                        words[v.strip()] = Set()
                    words[v.strip()].add(i)
                    rows.add(i)

        ## Make integers to make sure no floating point errors occur
        sup = round(100*float(self.support.get()))
        conf = round(100*float(self.confidence.get()))


        matches = self.getMatches([], words, rows, sup, conf, '')
        matchSet = Set(matches)


        print "====="
        for m in matchSet:
            print m


    def getMatches(self, wordsChecked, words, rows, sup, conf, sort):
        matches = []

        # check if we have the support and confidence
        if len(wordsChecked) > 1:
            actualSupport = self.calcSupport(wordsChecked, words, rows)
            if actualSupport >= sup:
                matches += self.getConfidence([], wordsChecked,  words, rows, conf)

        for w in words.keys():
            if w not in wordsChecked and w > sort:
                wordsChecked.append(w)
                matches += self.getMatches(wordsChecked, words, rows, sup, conf, w)
                wordsChecked.remove(w)

        return matches

    def getConfidence(self, left, universe, words, rows, conf):
        matches = []
        if len(left) > 0:
            matches += self.getConficenceRight(left, [], universe, words, rows, conf)

        for u in universe:
            if u not in left:
                left.append(u)
                matches += self.getConfidence(left, universe, words, rows, conf)
                left.remove(u)

        return matches


    def getConficenceRight(self, left, right, universe, words, rows, conf):
        matches = []
        if len(right) > 0:
            actualConf = self.calcSupport(left+right, words, rows) * 100
            actualConf /= self.calcSupport(left, words, rows)

            if actualConf >= conf:
                matches +=  [ ",".join(left) + ' => ' + ",".join(right)]

        for u in universe:
            if u not in left and u not in right:
                right.append(u)
                matches += self.getConficenceRight(left, right, universe, words, rows, conf)
                right.remove(u)

        return matches



    def calcSupport(self, wordsChecked, words, rows):
        allWords = rows
        for w in wordsChecked:
            allWords = allWords & words[w]

        print wordsChecked, len(allWords) * float(100) / len(rows)

        return len(allWords) * float(100) / len(rows)




root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below