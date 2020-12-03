import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
import math
import project3Functions as p3F

# Assemble the important functions from project3Functions to the main function
def main(file_name):
    tempL = []
    img = cv2.imread(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners = p3F.cornerDetection(file_name, 0.07) # 0.07, 

    xL = p3F.xLyLCorner(corners)[0]
    yL = p3F.xLyLCorner(corners)[1]

    # Make it unproceeding if you only want the data.
    p3F.showCorner(cv2.imread(file_name), corners)

    # Making lists for required information/sorted list using an axis as the base
    yLStandardSortL = p3F.doubleSort(yL, xL)

    # Raw list is required for sorting again!, so reset the list
    xL = p3F.xLyLCorner(corners)[0]
    yL = p3F.xLyLCorner(corners)[1]

    # DoubleSort the list again with x as its standardL
    xLStandardSortL = p3F.doubleSort(xL, yL)

    # All normal variables are ready now
    DivFactor = 3; fourErrorCoordinL = [[yLStandardSortL[1][each], yLStandardSortL[0][each]] for each in range(DivFactor+1)]
    backOuterCoorL = p3F.FourErrSorting(xLStandardSortL, fourErrorCoordinL, DivFactor, gray_img)
    
    # BackBottom Coordinates
    FrontOuterL = [[xLStandardSortL[0][0], xLStandardSortL[1][0]], [xLStandardSortL[0][-1], xLStandardSortL[1][-1]]]

    # Create the equation for the indication line
    SlopeOfIndicationLine = p3F.slope(FrontOuterL[0][0],FrontOuterL[1][0],FrontOuterL[0][1],FrontOuterL[1][1])
    C = FrontOuterL[0][1]-SlopeOfIndicationLine*FrontOuterL[0][0]# Function can be called by saying: y = slopeOfIndicationLine * x + c

    # Use the equation of the indication line for determining the backBottom point
    for each in range(len(yLStandardSortL[0])):
        if yLStandardSortL[0][each] < SlopeOfIndicationLine * yLStandardSortL[1][each] + C:
            if p3F.backInnerPointDecision(backOuterCoorL, gray_img.shape[1])[0][0] <= yLStandardSortL[1][each] <= p3F.backInnerPointDecision(backOuterCoorL, gray_img.shape[1])[1][0]:
                if [yLStandardSortL[1][each], yLStandardSortL[0][each]] not in backOuterCoorL:
                    tempL.append([yLStandardSortL[1][each], yLStandardSortL[0][each]])

    backBottomL = p3F.backBottomLDecision(backOuterCoorL, tempL)

    # Determining the bl and br using the backBottomL
    backleftTwoCoorInd = p3F.backLeftAndRightTwoCoorL(backOuterCoorL, backBottomL)[0]
    backrighttTwoCoorInd = p3F.backLeftAndRightTwoCoorL(backOuterCoorL, backBottomL)[1]
    
    outerUpperLen = p3F.pythagorasTheorem(backOuterCoorL[0][0], backOuterCoorL[1][0], backOuterCoorL[0][1], backOuterCoorL[1][1])
    cmDivPixB = 30/outerUpperLen
    bl = math.sqrt((p3F.pythagorasTheorem(backleftTwoCoorInd[0][0], backleftTwoCoorInd[1][0], backleftTwoCoorInd[0][1], backleftTwoCoorInd[1][1])*cmDivPixB)**2-8)
    br = math.sqrt((p3F.pythagorasTheorem(backrighttTwoCoorInd[0][0], backrighttTwoCoorInd[1][0], backrighttTwoCoorInd[0][1], backrighttTwoCoorInd[1][1])*cmDivPixB)**2-8)
    return bl, br

print(main("processed_img/processed8.png"))# Possible candidates = 26, 25, 12, 6, 2, 1
# Mid = 9, 10 < 14, 15, 16
# Prob = 3, 4, 5, 7, 8, 11, 13, 17, 18, 19, 20, 21, 22, 23, 24
# 최대 에러 가능 숫자 0.7cm
# 