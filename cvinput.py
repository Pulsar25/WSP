import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

totalImageSize = (1170,2532)
physicalSize = ()

#read and find vial locations
img_rgb = cv.imread("lvl291.png",0)
cv.imwrite("out.png",img_rgb)
template = cv.imread("vial.png",0)
w, h = template.shape[::-1]
print("read")
sizedImages = []
loc = []
for scale in range(50,510,10):
    imgScaled = cv.resize(img_rgb, None ,fx = (scale / 100),fy = (scale / 100), interpolation = cv.INTER_AREA)
    sizedImages.append(imgScaled)
    res = cv.matchTemplate(imgScaled,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    if len(loc[0]) != 0:
        break
sizeI = 0
for image in sizedImages:
    cv.imwrite("resize" + str(sizeI) + '.png', image)
    sizeI += 1
vialLocations = []
for pt in zip(*loc[::-1]):
    vialLocations.append((pt[0],pt[1]))
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)
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
print(str(len(totalColors)) + " Colors found.")
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
print(finalBoard)
j = 1
for vial in finalBoard:
    print(str(j) + ": " + str(vial))
    j += 1
solved = main.bfs(finalBoard,4)
print(solved)