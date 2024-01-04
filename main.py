#Block: Color, n
#Vial: Block[]
#Board: Vial[]

import time
import copy
import cv2 as cv
import numpy as np
import queue

def fixMoves(moves):
    newmoves = []
    for i in range (0,len(moves)):
        if (i < len(moves) - 1 and moves[i][0] == moves[i+1][1] and moves[i+1][0] == moves[i][1]):
            i += 1
        newmoves.append(moves[i])
    return newmoves
def incompletVials (board,vialHeight,depth):
    count = 0
    zeroCount = 0
    for vial in board:
        if (len(vial) == 0):
            zeroCount += 1
        if (len(vial) == 1 and vial[0][1] == vialHeight):
            count += 1
    return len(board) - count - 2
    #return -1 * (len(generateMoves(board,vialHeight)))
def moveLegal(board,start,end,vialHeight):
    if len(board[start]) == 0:
        return False
    n = 0
    for block in board[end]:
      n += block[1]
    return (n == 0 or board[start][0][0] == board[end][0][0]) and n != vialHeight and (not (n == 0 and len(board[start]) == 1))
def makeMove(board,start,end,vialHeight):
    newboard = copy.deepcopy(board)
    if not moveLegal(board,start,end,vialHeight):
        return newboard
    n = 0
    for block in board[end]:
        n += block[1]
    if n == 0:
        newboard[end].append(newboard[start].pop(0))
        return newboard
    if vialHeight - n >= board[start][0][1]:
        newboard[end][0][1] += board[start][0][1]
        newboard[start].pop(0)
        return newboard
    newboard[start][0][1] -= vialHeight - n
    newboard[end][0][1] += vialHeight - n
    return newboard
def checkWin(board,vialHeight):
    for vial in board:
        if not (len(vial) == 0 or (len(vial) == 1 and vial[0][1] == vialHeight)):
            return False
    return True
def generateMoves(board,vialHeight):
    emptys = []
    colors = {}
    for i in range(len(board)):
        if len(board[i]) == 0:
            emptys.append(i)
            continue
        if board[i][0][0] in colors:
            colors[board[i][0][0]].append(i)
        else:
            colors[board[i][0][0]] = [i]
    moves = []
    for color in colors:
        for i in colors[color]:
            for j in colors[color]:
                if i != j and moveLegal(board,i,j,vialHeight):
                    moves.append((i,j))
    for i in range(len(board)):
        if i not in emptys:
            for j in emptys:
                moves.append((i,j))
    return moves
def boardToString(board,vialHeight):
    out = []
    for vial in board:
        out.append(str(vial))
    out = sorted(out)
    return str(out)
def bfs(initial,vialHeight):
    states = queue.Queue()
    states.put((initial,[],0))
    firstDepthState = []
    c = 0
    prevStates = set()
    while not states.empty():
        c += 1
        top = states.get()
        if top[2] > 1:
            firstDepthState.append(top)
            continue
        stringBoard = boardToString(top[0], vialHeight)
        if stringBoard in prevStates:
            continue
        else:
            prevStates.add(stringBoard)
        if checkWin(top[0], vialHeight):
            finalMoves = fixMoves(top[1])
            return finalMoves
        moves = generateMoves(top[0], vialHeight)
        for move in moves:
            moved = makeMove(top[0], move[0], move[1], vialHeight)
            states.put((moved, top[1] + [(move[0] + 1, move[1] + 1)], top[2] + 1))
    states = queue.PriorityQueue()
    for state in firstDepthState:
        states.put((incompletVials(state[0],vialHeight,state[2]),state))
    while not states.empty():
        top = states.get()[1]
        c += 1
        stringBoard = (boardToString((top[0]),vialHeight))
        if stringBoard in prevStates:
            continue
        else:
            prevStates.add(stringBoard)
        if checkWin(top[0],vialHeight):
            finalMoves = fixMoves(top[1])
            print (str(c) + " States Computed")
            return finalMoves
        moves = generateMoves(top[0],vialHeight)
        for move in moves:
            moved = makeMove(top[0],move[0],move[1],vialHeight)
            states.put((incompletVials(moved,vialHeight,top[2]+1),(moved,top[1] + [(move[0] + 1, move[1] + 1)],top[2] + 1)))
    return "NO SOLUTION"

#cv and such
#1170,2532
totalImageSize = (1170,2532)
inputLocation = input("Enter file name of screenshot including extension (must be in same directory as solver):\n")
#read and find vial locations
img_rgb = cv.imread(inputLocation,0)
ow, oh = img_rgb.shape[::-1]
print(ow,oh)
print(int(totalImageSize[1] * ow / totalImageSize[0]))
#img_rgb = img_rgb[0:min(oh,min(oh,int(totalImageSize[1] * ow / totalImageSize[0]))),0:ow]
img_rgb = cv.resize(img_rgb, (totalImageSize[0],int(oh * totalImageSize[0] / ow)))
cv.imwrite("out.png",img_rgb)
template = cv.imread("vial.png",0)
w, h = template.shape[::-1]
print("Image Read Successfully")
loc = []
res = cv.matchTemplate(img_rgb,template,cv.TM_CCOEFF_NORMED)
threshold = 0.9
loc = np.where(res >= threshold)
vialLocations = []
for pt in zip(*loc[::-1]):
    vialLocations.append((pt[0],pt[1]))
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
vialPositions = []
for vial in vialLocations:
    bad = False
    for i in range(len(vialPositions)-1,-1,-1):
        if abs(vial[0] - vialPositions[i][0]) < 150 and abs(vial[1] - vialPositions[i][1]) < 150:
            bad = True
            break
    if not bad:
        vialPositions.append(vial)
for i in range(0,len(vialPositions)):
    vialPositions[i] = (vialPositions[i][0] + 76,vialPositions[i][1] + 130)
print(str(len(vialPositions)) + " Vials Found")
a = time.time()
#color detection
rows,cols = img_rgb.shape
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
colorSize = 106
boardInitial = []
for i in range(len(vialPositions)-2):
    vial = []
    for j in range(4):
        vial.append(img_rgb[j * colorSize + vialPositions[i][1],vialPositions[i][0]])
    boardInitial.append(vial)
totalColors = set()
for vial in boardInitial:
    for color in vial:
        totalColors.add(color)
totalColors = sorted(list(totalColors))
print(str(len(totalColors)) + " Unique Colors Found.")
print("Read initial board state:")
transferDict = {}
for i in range(len(totalColors)):
    transferDict[totalColors[i]] = i
for i in range(len(boardInitial)):
    for j in range(4):
        boardInitial[i][j] = alphabet[transferDict[boardInitial[i][j]]]
finalBoard = []
for vial in boardInitial:
    out = []
    current = vial[0]
    count = 1
    for i in range(1,len(vial)):
        if current == vial[i]:
            count += 1
        else:
            out.append([current,count])
            count = 1
            current = vial[i]
    out.append([current,count])
    finalBoard.append(out)
finalBoard.append([])
finalBoard.append([])
j = 1
for vial in finalBoard:
    print("Vial " + str(j) + ": " + str(vial))
    j += 1
solved = bfs(finalBoard,4)
print(str(len(solved)) + " Moves")
print(str(time.time() - a) + " Seconds Spent")
print("Moves (from vial, to vial):")
print(solved)
print()
input("Click Enter to close solver")