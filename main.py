import turtle as t
from CONFIGS import *
import pandas
import numpy as np
from CONFIGS import *

# small project to learn python from "Apprendre à coder avec Python on fun mooc"


minx = ZONE_PLAN_MINI[0]
miny = ZONE_PLAN_MINI[1]
maxx = ZONE_PLAN_MAXI[0]
maxy = ZONE_PLAN_MAXI[1]
poianx = POINT_AFFICHAGE_ANNONCES[0]
poiany = POINT_AFFICHAGE_ANNONCES[1]
poiinx = POINT_AFFICHAGE_INVENTAIRE[0]
poiiny = POINT_AFFICHAGE_INVENTAIRE[1]

xLen = maxx - minx
yLen = maxy - miny


def util_calculer_pas(matrix):
    ret = 0
    nCOL = np.size(matrix, 0)
    nLIG = np.size(matrix, 1)
    print(nCOL, "x", nLIG)
    x = minx
    y = miny
    sizeX = xLen / nLIG
    sizeY = yLen / nCOL
    print("taille <---> X vs Y : ", str(xLen), yLen)
    print("Nb Cases X et Y     : ", str(nCOL), nLIG)
    if sizeX < sizeY:
        ret = int(sizeX)
    else:
        ret = int(sizeY)
    print("size of a square   :", str(sizeX), "x", str(sizeY), " == keeping ", ret)
    return ret


def util_getCoordonnees(case, pas):
    realX = minx + pas * case[1]  # col
    realY = maxy - pas * case[0] - pas  # ligne
    return (realX, realY)


def util_tracer_carre(dimension):
    t.pen(pendown=True)
    for i in range(4):
        t.forward(dimension)
        t.right(-90)
    t.pen(pendown=False)


def util_tracer_case(case, couleur, pas, disableTracer=True):
    if disableTracer:
        t.tracer(False)
    t.penup()
    realcoord = util_getCoordonnees(case, pas)
    t.setx(realcoord[0])
    t.sety(realcoord[1])
    t.pendown()
    t.fillcolor(couleur)
    t.begin_fill()
    util_tracer_carre(pas)
    t.end_fill()
    t.penup()
    if disableTracer:
        t.tracer(True)
        t.update()


def util_printLine(x1, y1, x2, y2):
    #  print ("printing", x1 ,".", y1 , "--", x2, ".", y2)
    t.setx(x1)
    t.sety(y1)
    t.pen(pendown=True)
    t.setx(x2)
    t.sety(y2)
    t.pen(pendown=False)


def util_afficher_matrix(matrix):
    t.tracer(False)
    pas = util_calculer_pas(matrix)
    [[util_tracer_case((iLig, iCol), COULEURS[int(matrix[iLig][iCol])], pas, False) for iCol in
      range(len(matrix[iLig]))] for iLig
     in range(len(matrix))]
    t.tracer(True)
    t.update()


def util_textAMessage(x1, y1, x2, y2, xt, yt, m, c):
    t.tracer(False)
    oldpos = t.pos()
    t.fillcolor(c)
    util_printLine(x1, y1, x2, y1)
    t.begin_fill()
    util_printLine(x2, y1, x2, y2)
    util_printLine(x2, y2, x1, y2)
    util_printLine(x1, y2, x1, y1)
    t.end_fill()
    t.setx(xt)
    t.sety(yt)
    t.write(m)
    t.setpos(oldpos)
    t.tracer(True)
    t.update()


class movementMgr:
    def __init__(self, abs, ord, matrix, pas, objectDict, questionsDict):
        self.x = abs
        self.y = ord
        self.m = matrix
        self.p = pas
        self.inv = ["-", "_"]
        self.annonce = "ANNONCE"
        self.oDict = objectDict
        self.qDict = questionsDict
        self.textInventaire()
        self.textAnnonce()
        self.updateTurtlePos()

    def getPos(self):
        return (x, y)

    def getX(self):
        return minx + self.p * self.x + self.p / 2

    def getY(self):
        realY = maxy - self.p * self.y - self.p / 2
        return realY

    def printCurrentPos(self):
        realX = minx + self.p * self.x + self.p / 2
        realY = maxy - self.p * self.y - self.p / 2
        print(self.x, self.y, realX, realY)

    def checkPos(self, x, y):
        print("current=", self.x, self.y, "query", x, y)
        if x >= 0 and y >= 0 and x < len(matrix[0]) and y < len(matrix):
            print("in ", x, y, "we have", matrix[y][x])
            return matrix[y][x]
        else:
            print("bad position")
            return 1

    def up(self):
        self.checkNextPosAndUpdate(self.x, self.y - 1)

    def down(self):
        self.checkNextPosAndUpdate(self.x, self.y + 1)

    def left(self):
        self.checkNextPosAndUpdate(self.x - 1, self.y)

    def right(self):
        self.checkNextPosAndUpdate(self.x + 1, self.y)

    def checkNextPosAndUpdate(self, x, y):
        if self.checkPos(x, y) == 3:
            if not self.processQuestion(x, y):
                return

        if self.checkPos(x, y) != 1:
            self.x = x
            self.y = y

    def util_getCoordonnees(case, pas):
        realX = minx + pas * case[1]  # col
        realY = maxy - pas * case[0] - pas  # ligne

        # print ("ligne" ,case[0], " col:" , case[1], " reverse ", realX , realY  )
        return (realX, realY)


    def processQuestion(self, x, y):
        ret = False
        if ((y, x) in questionsDict):
            q = questionsDict[(y, x)][0]
            r = questionsDict[(y, x)][1]
            self.annonce = "PORTE FERMEE new question on " + str(x) + str(y) + q + "r=" + r
            self.textAnnonce()

            answer = t.simpledialog.askstring("QUESTION FOR A DOOR", q)
            if answer == r:
                self.annonce = "BONNE REP : PORTE OUVERTE"
                self.m[y][x] = 0
                util_tracer_case((y, x), 'white', self.p)
                ret = True
            else:
                self.annonce = "MAUVAISE REP : LA PORTE RESTE FERMEE"
        else:
            self.annonce = " ! NOT FOUND new question on " + str(self.x) + str(self.y)
        self.textAnnonce()

        return ret

    def processPosition(self):
        """ valeur 0 pour une case vide,
            valeur 1 pour un mur (infranchissable),
            valeur 2 pour la case de sortie/victoire,
            valeur 3 pour une porte qui sera franchissable en répondant à une question,
            valeur 4 pour une case contenant un objet à collecter."""

        typeCase = self.checkPos(self.x, self.y)
        print(" we are on ", (self.y, self.x), " type case =", typeCase)
        if typeCase == 2:
            print("gagné")
            self.annonce = "GAGNE !! BRAVO !! YOUPIII "
            self.textAnnonce()

        if typeCase == 4:
            if ((self.y, self.x) in objectDict):

                self.m[self.y][self.x] = 0
                util_tracer_case((self.y, self.x), 'white', self.p)
                self.updateTurtlePos()
                self.inv.append(objectDict[(self.y, self.x)])
                self.textInventaire()
            else:
                print("/!\ NOT FOUND new object.....")

    def updateTurtlePos(self):
        t.sety(self.getY())
        t.setx(self.getX())

    def textAnnonce(self):
        util_textAMessage(poianx, poiany, maxx + 100, poiany + 20, poianx, poiany, "   " + self.annonce, 'yellow')

    def textInventaire(self):
        util_textAMessage(poiinx - 5, poiiny, maxx + 100, poiiny - 200, poiinx, poiiny - 100,
                          "INVENTAIRE" + '\n'.join(self.inv), 'green')


def doTheGame(matrix, pas, objectDict, questionsDict):
    posA = POSITION_DEPART[1]
    posB = POSITION_DEPART[0]

    mg = movementMgr(posA, posB, matrix, pas, objectDict, questionsDict)

    def up():
        mg.up()
        mg.updateTurtlePos()
        mg.processPosition()

    def down():
        mg.down()
        mg.updateTurtlePos()
        mg.processPosition()

    def left():
        mg.left()
        mg.updateTurtlePos()
        mg.processPosition()

    def right():
        mg.right()
        mg.updateTurtlePos()
        mg.processPosition()

    wn = t.Screen()
    wn.listen()

    wn.onkey(up, 'Up')
    wn.onkey(down, 'Down')
    wn.onkey(left, 'Left')
    wn.onkey(right, 'Right')


def readConfig(file):
    print("reafing", file)
    f = open(file)
    d = {}
    for line in f:
        a, b = eval(line)
        d[a] = b
    f.close()
    return d


if __name__ == '__main__':
    t.speed(0)
    matrix = [list(map(int, a)) for a in [line.strip().split(" ") for line in open(fichier_plan)]]
    objectDict = readConfig(fichier_objets)
    questionsDict = readConfig(fichier_questions)
    print(matrix)
    pas = util_calculer_pas(matrix)
    util_afficher_matrix(matrix)
    doTheGame(matrix, pas, objectDict, questionsDict)

    t.done()
