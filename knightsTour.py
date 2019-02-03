import sys
from graphics import *
import time

#HaltException to stop program
class HaltException(Exception): pass

class KnightsTour:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.xCur = 60
        self.yCur = 60
        self.numberVisit = 0

        self.board = []
        self.generate_board()

    def generate_board(self):
        #Creates a nested list to represent the game board
        for i in range(self.h):
            self.board.append([0]*self.w)

    def printBoard(self):
        print("  \n------\n")
        for elem in self.board:
            print(elem)
        print("  \n------\n")

    def generateLegalMoves(self, curPos):
        #Generates a list of legal moves for the knight to take next
        possiblePos = []
        moveOffsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in moveOffsets:
            newX = curPos[0] + move[0]
            newY = curPos[1] + move[1]

            if (newX >= self.h):
                continue
            elif (newX < 0):
                continue
            elif (newY >= self.w):
                continue
            elif (newY < 0):
                continue
            else:
                possiblePos.append((newX, newY))

        return possiblePos

    def sortLonelyNeighbors(self, toVisit):
        #We seek out the edges of the neighbors, or "lonely neighbors"
        #first because they cannot be easily reached later.
        neighborList = self.generateLegalMoves(toVisit)
        emptyNeighbours = []

        for neighbor in neighborList:
            npValue = self.board[neighbor[0]][neighbor[1]]
            if npValue == 0:
                emptyNeighbours.append(neighbor)

        scores = []
        for empty in emptyNeighbours:
            score = [empty, 0]
            moves = self.generateLegalMoves(empty)
            for m in moves:
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)

        scoresSort = sorted(scores, key = lambda s: s[1])
        sortedNeighbours = [s[0] for s in scoresSort]
        return sortedNeighbours

    def tour(self, n, path, toVisit):
        #n = current depth of search tree
        #path = current path taken
        #toVisit = node to visit
        time.sleep(.3)
        self.board[toVisit[0]][toVisit[1]] = n
        path.append(toVisit) #append the newest vertex to the current point
        print("Visiting: ", toVisit)
        
        #Creates line for graphic
        ln = Line(Point(self.xCur, self.yCur), Point(int((toVisit[0]) * 80) + 50,(int(toVisit[1]) * 80) + 50))
        ln.draw(win)
        #Creates points for graphic
        circ = Circle(Point(int((toVisit[0]) * 80) + 50,(int(toVisit[1]) * 80) + 50),5)
        circ.setFill("white")
        circ.setOutline("white")
        circ.draw(win)
        #Adds current position in pixels
        self.xCur = (int(toVisit[0]) * 80) + 50
        self.yCur = (int(toVisit[1]) * 80) + 50
        self.numberVisit +=1

        if n == self.w * self.h: #if every grid is filled
            self.printBoard()
            print(path)
            print("Knights Tour Successful!")
            raise HaltException("Knights Tour Complete!")

        else:
            sortedNeighbours = self.sortLonelyNeighbors(toVisit)
            for neighbor in sortedNeighbours:
                self.tour(n+1, path, neighbor)

            #If we exit this loop, all neighbours failed so we reset
            self.board[toVisit[0]][toVisit[1]] = 0
            try:
                path.pop()
                print("Going back to: ", path[-1])
            except IndexError:
                print("No path found")
                sys.exit(1)

inputString = input("Please enter a grid size, e.g., 8,8:") #get grid size
size = inputString.split(',')
#set window size based on grid size.
win = GraphWin("KnightsTour", int(size[0])*80+40, int(size[0])*80+40)
win.setBackground('#7F5EBA')
#set border size
xStart = 20
yStart = 20
#get rows for graphic
for x in range(int(size[0])):
    #get columns for graphic
    for y in range(int(size[1])):
        rect = Rectangle(Point(xStart, yStart), Point(xStart+(80*(y+1)), yStart+ 80))
        rect.setOutline("#FF4E00")
        rect.draw(win)
    yStart += 80
        
#Define the size of grid. We are currently solving for an 8x8 grid
kt = KnightsTour(int(size[0]), int(size[1]))
kt.tour(1, [], (0,0))
kt.printBoard()
