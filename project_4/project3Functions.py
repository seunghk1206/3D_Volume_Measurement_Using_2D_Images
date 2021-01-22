import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Special mathematical functions
def pythagorasTheorem(x1, x2, y1, y2):
    a = x1-x2
    b = y1-y2
    return math.sqrt(a**2+b**2)

def slope(x1, x2, y1, y2):
    a = x1-x2
    b = y1-y2
    return b/a

def slope2Angle(slope):
    if slope == "inf":
        return 90
    else:
        return math.atan(slope) * (180/math.pi)

# Special sorting algorithm
def doubleSort(A, B):
    for i in range(0, len(A)):
        minIndex = i
        for j in range(i+1, len(A)):
            if A[j] < A[minIndex]:
                A[j], A[minIndex] = A[minIndex], A[j]
                B[j], B[minIndex] = B[minIndex], B[j]
    return [A, B]

# Important functions for the main function
def cornerDetection(file_name, quality):
    img = cv2.imread(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners = cv2.goodFeaturesToTrack(gray_img, 300, quality, 10) 
    corners = np.int0(corners) 
    #copyright, GeeksforGeeks @hachiman_20
    return corners

def xLyLCorner(corners):
    xL = []; yL = []
    for each in corners: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    return [xL, yL]

def showCorner(img, corners):
    for each in corners:
        x, y = each.ravel() 
        cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    plt.imshow(img) 
    plt.show()
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows() 
    #copyright, GeeksforGeeks @hachiman_20
    return None

def FourErrSorting(xLStandardSortL, FourErrorCoordinL, divFactor, gray_img):
    slopeL = []
    lengthL = []
    angleL = []
    justifyL = []
    setJustifyL =[]
    backOuterCoorL = []

    # BackOuter points are decided from 66-118

    # Appending required informations such as length and slope
    for each in FourErrorCoordinL:
        for eachInd in range(len(FourErrorCoordinL)):
            if FourErrorCoordinL[eachInd] == each: 
                pass
            else:
                slopeL.append(slope(FourErrorCoordinL[eachInd][0], each[0], FourErrorCoordinL[eachInd][1], each[1]))
                lengthL.append(pythagorasTheorem(FourErrorCoordinL[eachInd][0], each[0], FourErrorCoordinL[eachInd][1], each[1]))
    # Slope to angle 
    for each in slopeL:
        angleL.append(slope2Angle(each))
    # Sorting things using length and angle
    for each in range(len(lengthL)):
        if lengthL[each] > gray_img.shape[1]/4 and -20 <= angleL[each] <= 20:
            if each%divFactor > each//divFactor:
                justifyL.append(FourErrorCoordinL[each%divFactor+1])
            else:
                justifyL.append(FourErrorCoordinL[each%divFactor])
        elif lengthL[each] > gray_img.shape[1]/4 and 340 <= angleL[each] <= 0:
            if each%divFactor > each//divFactor:
                justifyL.append(FourErrorCoordinL[each%divFactor+1])
            else:
                justifyL.append(FourErrorCoordinL[each%divFactor])
        if lengthL[each] > gray_img.shape[1]/4 and 160 <= angleL[each] <= 200:
            if each%divFactor > each//divFactor:
                justifyL.append(FourErrorCoordinL[each%divFactor+1])
            else:
                justifyL.append(FourErrorCoordinL[each%divFactor])
    del lengthL[:]#reset the list!
    # Sortings using only length
    for each in justifyL:
        if each in setJustifyL:
            pass
        else:
            setJustifyL.append(each)
    for each in setJustifyL:
        for eachT in setJustifyL:
            if each == eachT:
                pass
            else:
                lengthL.append(pythagorasTheorem(eachT[0], each[0], eachT[1], each[1]))
    divLen = (len(setJustifyL)-1)
    IndA = (lengthL.index(max(lengthL)))%divLen
    IndB = lengthL.index(max(lengthL))//divLen
    if IndA > IndB:
        IndA += 1
    backOuterCoorL.append(setJustifyL[IndA])
    backOuterCoorL.append(setJustifyL[IndB])
    return backOuterCoorL

def backInnerPointDecision(backOuterCoorL, entirePix):
    if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
        backleftOuterCoor = backOuterCoorL[0]
        backrightOuterCoor = backOuterCoorL[1]
    
    elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
        backleftOuterCoor = backOuterCoorL[1]
        backrightOuterCoor = backOuterCoorL[0]
    cmDivPixB = 30/(pythagorasTheorem(backleftOuterCoor[0], backrightOuterCoor[0], backleftOuterCoor[1], backrightOuterCoor[1]))
    backInnerLeftCoor = [int(backleftOuterCoor[0]+2/cmDivPixB+(2/1118*entirePix))-1, backleftOuterCoor[1]+2/cmDivPixB]
    backInnerRightCoor = [int(backrightOuterCoor[0]-2/cmDivPixB-(2/1118*entirePix)), backrightOuterCoor[1]+2/cmDivPixB]
    return [backInnerLeftCoor, backInnerRightCoor]

def backBottomLDecision(backOuterCoorL, tempL):
    backBottomL = []
    slopeL = []
    slope2L = []
    angleL = []
    for each in tempL:
        if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
            slopeL.append(slope(backOuterCoorL[0][0],each[0],backOuterCoorL[0][1],each[1]))
            slope2L.append(slope(backOuterCoorL[1][0], each[0], backOuterCoorL[1][1], each[1]))

        elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
            slope2L.append(slope(backOuterCoorL[0][0],each[0],backOuterCoorL[0][1],each[1]))
            slopeL.append(slope(backOuterCoorL[1][0], each[0], backOuterCoorL[1][1], each[1]))

    for each in slopeL:
        angleL.append(slope2Angle(each))
    backBottomL.append(tempL[angleL.index(max(angleL))])
    del angleL[:]# Reset the list before recycling

    for each in slope2L:
        angleL.append(slope2Angle(each))
    backBottomL.append(tempL[angleL.index(min(angleL))])
    return backBottomL

def backLeftAndRightTwoCoorL(backOuterCoorL, backBottomL):
    if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
        if backBottomL[0][0] < backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[0], backBottomL[0]]; backrighttTwoCoorInd = [backOuterCoorL[1], backBottomL[1]]
        elif backBottomL[0][0] > backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[0], backBottomL[1]]; backrighttTwoCoorInd = [backOuterCoorL[1], backBottomL[0]]
        
    elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
        if backBottomL[0][0] < backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[1], backBottomL[0]]; backrighttTwoCoorInd = [backOuterCoorL[0], backBottomL[1]]
        elif backBottomL[0][0] > backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[1], backBottomL[1]]; backrighttTwoCoorInd = [backOuterCoorL[0], backBottomL[0]]
    return [backleftTwoCoorInd, backrighttTwoCoorInd]
# ZeroclassLab.corp : Computer Vision
# -> Calculated the length of any cabinets