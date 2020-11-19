import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
import math

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
    #=============================================sorting things using length and angle======================================
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
    #===========================================sortings using only length===================================================
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
    del angleL[:]#reset the list before recycling

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

# Assemble the important functions to the main function
def main(file_name):
    tempL = []
    img = cv2.imread(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners = cornerDetection(file_name, 0.07)

    xL = xLyLCorner(corners)[0]
    yL = xLyLCorner(corners)[1]

    # Make it unproceeding if you only want the data.
    showCorner(cv2.imread(file_name), corners)

    # Making lists for required information/sorted list using an axis as the base
    yLStandardSortL = doubleSort(yL, xL)

    # Raw list is required for sorting again!, so reset the list
    xL = xLyLCorner(corners)[0]
    yL = xLyLCorner(corners)[1]

    # DoubleSort the list again with x as its standardL
    xLStandardSortL = doubleSort(xL, yL)

    # All normal variables are ready now
    DivFactor = 3; fourErrorCoordinL = [[yLStandardSortL[1][each], yLStandardSortL[0][each]] for each in range(DivFactor+1)]
    backOuterCoorL = FourErrSorting(xLStandardSortL, fourErrorCoordinL, DivFactor, gray_img)
    
    # BackBottom Coordinates
    FrontOuterL = [[xLStandardSortL[0][0], xLStandardSortL[1][0]], [xLStandardSortL[0][-1], xLStandardSortL[1][-1]]]

    # Create the equation for the indication line
    SlopeOfIndicationLine = slope(FrontOuterL[0][0],FrontOuterL[1][0],FrontOuterL[0][1],FrontOuterL[1][1])
    C = FrontOuterL[0][1]-SlopeOfIndicationLine*FrontOuterL[0][0]# Function can be called by saying: y = slopeOfIndicationLine * x + c

    # Use the equation of the indication line for determining the backBottom point
    for each in range(len(yLStandardSortL[0])):
        if yLStandardSortL[0][each] < SlopeOfIndicationLine * yLStandardSortL[1][each] + C:
            if backInnerPointDecision(backOuterCoorL, gray_img.shape[1])[0][0] <= yLStandardSortL[1][each] <= backInnerPointDecision(backOuterCoorL, gray_img.shape[1])[1][0]:
                if [yLStandardSortL[1][each], yLStandardSortL[0][each]] not in backOuterCoorL:
                    tempL.append([yLStandardSortL[1][each], yLStandardSortL[0][each]])

    backBottomL = backBottomLDecision(backOuterCoorL, tempL)

    # Determining the bl and br using the backBottomL
    backleftTwoCoorInd = backLeftAndRightTwoCoorL(backOuterCoorL, backBottomL)[0]
    backrighttTwoCoorInd = backLeftAndRightTwoCoorL(backOuterCoorL, backBottomL)[1]
    
    outerUpperLen = pythagorasTheorem(backOuterCoorL[0][0], backOuterCoorL[1][0], backOuterCoorL[0][1], backOuterCoorL[1][1])
    cmDivPixB = 30/outerUpperLen
    bl = math.sqrt((pythagorasTheorem(backleftTwoCoorInd[0][0], backleftTwoCoorInd[1][0], backleftTwoCoorInd[0][1], backleftTwoCoorInd[1][1])*cmDivPixB)**2-8)
    br = math.sqrt((pythagorasTheorem(backrighttTwoCoorInd[0][0], backrighttTwoCoorInd[1][0], backrighttTwoCoorInd[0][1], backrighttTwoCoorInd[1][1])*cmDivPixB)**2-8)
    return bl, br

print(main('processed_img/processed6.png'))# Possible candidates = 6, 2, 1
# Prob = 3, 4, 5, 7, 8