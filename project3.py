import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
import math
import time
def doubleSort(A, B):
    for i in range(0, len(A)):
        minIndex = i
        for j in range(i+1, len(A)):
            if A[j] < A[minIndex]:
                A[j], A[minIndex] = A[minIndex], A[j]
                B[j], B[minIndex] = B[minIndex], B[j]
    return [A, B]
'''
def doubleSort(A, B):
    for each in range(0, len(A)): 
        for i in range(0, len(A)): 
            if A[each] < A[i]: 
                A[each], A[i] = A[i], A[each]
                B[each], B[i] = B[i], B[each]
    return [A, B]
'''
'''
def grab_cut(inpDir):
    img = cv2.imread(inpDir)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (50,50,600,500)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    return img
    '''
def x1x2(file_name):
    start_time = time.time()
    img = cv2.imread(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners2 = cv2.goodFeaturesToTrack(gray_img, 300, 0.0001, 10) 
    corners2 = np.int0(corners2) 
    corners = cv2.goodFeaturesToTrack(gray_img, 50, 0.1, 10) 
    corners = np.int0(corners) 
    #=============================key point ====================================
    xL = []; yL = []
    for each in corners: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    ######====make it unproceeding if you only want the data.=========
    '''
            x, y = i.ravel() 
            cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    plt.imshow(img) 
    plt.show()
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows() 
        '''
    ######============================================================

    ######====make it unproceeding if you only want the data.=========
    '''
    for each in corners2:
        for i in each:
            x, y = i.ravel() 
            cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    plt.imshow(img) 
    plt.show()
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows() 
        '''
    ######============================================================
    #copyright, GeeksforGeeks @hachiman_20
    #================making lists for required information/sorted list using an axis as the base=================
    yLStandardSortL = doubleSort(yL, xL)#index 0 is yL
    xL = []; yL = []
    #============================raw list is required for sorting again!, so reset the list======================
    for each in corners: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    #===========================doubleSort the list again with x as its standardL================================
    xLStandardSortL = doubleSort(xL, yL)#index 0 is xL
    #========================================All normal variables are ready now!=================================
    FourErrorCoordinL = [[yLStandardSortL[1][each], yLStandardSortL[0][each]] for each in range(4)]
    slopeL = []; lengthL = []; angleL = []; justifyL = []

    #=========================================4 general points lists=============================================
    backOuterCoorL = []
    FrontOuterL = [[xLStandardSortL[0][0], xLStandardSortL[1][0]], [xLStandardSortL[0][-1], xLStandardSortL[1][-1]]]

    #=============================================================================================================================================================================
    #===================================================backOuter points are decided from 55-78(enhanced)=========================================================================
    #=============================================================================================================================================================================

    if FourErrorCoordinL[0][1] == FourErrorCoordinL[1][1] and FourErrorCoordinL[1][0] > gray_img.shape[1]/2:
        FourErrorCoordinL[0], FourErrorCoordinL[1] = FourErrorCoordinL[1], FourErrorCoordinL[0]
    #==============================================appending required informations such as length and slope==================
    for each in FourErrorCoordinL[1:]:
        slopeL.append((FourErrorCoordinL[0][1]-each[1])/(FourErrorCoordinL[0][0]-each[0]))
        lengthL.append(((FourErrorCoordinL[0][1]-each[1])**2+(FourErrorCoordinL[0][0]-each[0])**2)**(1/2))
    #=============================================slope to angle============================================================= 
    for each in slopeL:
        if each == 'inf':
            angleL.append(90)
        else:
            angleL.append(math.atan(each)*(180/math.pi))
    #=============================================sorting things using length and angle======================================
    for each in range(3):
        if lengthL[each] > gray_img.shape[1]/4 and -20 <= angleL[each] <= 20:
            justifyL.append(FourErrorCoordinL[each+1])
        elif lengthL[each] > gray_img.shape[1]/4 and 340 <= angleL[each] <= 0:
            justifyL.append(FourErrorCoordinL[each+1])
        if lengthL[each] > gray_img.shape[1]/4 and 160 <= angleL[each] <= 200:
            justifyL.append(FourErrorCoordinL[each+1])
    del lengthL[:]#reset the list!
    #===========================================sortings using only length===================================================
    for each in justifyL:
        lengthL.append(((FourErrorCoordinL[0][1]-each[1])**2+(FourErrorCoordinL[0][0]-each[0])**2)**(1/2))
    backOuterCoorL.append([FourErrorCoordinL[0][0], FourErrorCoordinL[0][1]])
    backOuterCoorL.append(justifyL[lengthL.index(max(lengthL))])

    #=============================================================================================================================================================================
    #==========================================================backBottom Coordinates!============================================================================================
    #=============================================================================================================================================================================

    #==========================Declare the list for backBottomCoordinates and the other required lists=======================
    backBottomL = []; tempL = []; slopeL = []; slope2L = []; angleL = []
    #===================================create the equation for the indication line!=========================================
    slopeOfIndicationLine = (FrontOuterL[0][1]-FrontOuterL[1][1])/(FrontOuterL[0][0]-FrontOuterL[1][0])
    c = FrontOuterL[0][1]-slopeOfIndicationLine*FrontOuterL[0][0]
    #function can be called by saying: y = slopeOfIndicationLine * x + c
    #====================use the equation of the indication line for determining the backBottom point========================
    for each in range(len(yLStandardSortL[0])):
        if yLStandardSortL[0][each] < slopeOfIndicationLine * yLStandardSortL[1][each] + c and min(backOuterCoorL[0][0], backOuterCoorL[1][0])<= yLStandardSortL[1][each] <=max(backOuterCoorL[0][0], backOuterCoorL[1][0]):
            if [yLStandardSortL[1][each], yLStandardSortL[0][each]] not in backOuterCoorL:
                tempL.append([yLStandardSortL[1][each], yLStandardSortL[0][each]])
    for each in tempL:
        if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
            slopeL.append((backOuterCoorL[0][1]-each[1])/(backOuterCoorL[0][0]-each[0]))
            slope2L.append((backOuterCoorL[1][1]-each[1])/(backOuterCoorL[1][0]-each[0]))
        elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
            slope2L.append((backOuterCoorL[0][1]-each[1])/(backOuterCoorL[0][0]-each[0]))
            slopeL.append((backOuterCoorL[1][1]-each[1])/(backOuterCoorL[1][0]-each[0]))
    for each in slopeL:
        if each == 'inf':
            angleL.append(90)
        else:
            angleL.append(math.atan(each)*(180/math.pi))
    backBottomL.append(tempL[angleL.index(max(angleL))])
    del angleL[:]#reset the list before recycling
    for each in slope2L:
        if each == 'inf':
            angleL.append(90)
        else:
            angleL.append(math.atan(each)*(180/math.pi))
    backBottomL.append(tempL[angleL.index(min(angleL))])

    #=============================================================================================================================================================================
    #=====================================================determining the bl and br using the backBottomL=========================================================================
    #=============================================================================================================================================================================

    outerUpperLen = ((backOuterCoorL[0][0]-backOuterCoorL[1][0])**2+(backOuterCoorL[0][1]-backOuterCoorL[1][1])**2)**(1/2)
    #meanL = (innerLowerL+innerUpperL)/2#unneeded because innerUpper != innerLower
    cmDivPixB = 30/outerUpperLen# extremely important!!
    if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
        if backBottomL[0][0] < backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[0], backBottomL[0]]
            backrighttTwoCoorInd = [backOuterCoorL[1], backBottomL[1]]
        elif backBottomL[0][0] > backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[0], backBottomL[1]]
            backrighttTwoCoorInd = [backOuterCoorL[1], backBottomL[0]]
    elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
        if backBottomL[0][0] < backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[1], backBottomL[0]]
            backrighttTwoCoorInd = [backOuterCoorL[0], backBottomL[1]]
        elif backBottomL[0][0] > backBottomL[1][0]:
            backleftTwoCoorInd = [backOuterCoorL[1], backBottomL[1]]
            backrighttTwoCoorInd = [backOuterCoorL[0], backBottomL[0]]

    #=============================================================================================================================================================================
    #===========================================================Now, front len part of the whole code!============================================================================
    #=============================================================================================================================================================================

    if backOuterCoorL[0][0] < backOuterCoorL[1][0]:
        backleftOuterCoor = backOuterCoorL[0]
        backrightOuterCoor = backOuterCoorL[1]
    elif backOuterCoorL[0][0] > backOuterCoorL[1][0]:
        backleftOuterCoor = backOuterCoorL[1]
        backrightOuterCoor = backOuterCoorL[0]
    print(backleftOuterCoor, backrightOuterCoor)
    #============================declare the lists that will be used to determine fl and fr==================================
    pointsForFl = []; pointsForFr = []
    #==================reset the xL & yL to the low quality corners in order to determine the fl and fr======================
    xL = []; yL = []
    for each in corners2: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    xLStandardSortL = doubleSort(xL, yL)
    for each in range(len(xLStandardSortL[0])):
        if xLStandardSortL[0][each] <= backleftOuterCoor[0]:
            pointsForFl.append([xLStandardSortL[0][each], xLStandardSortL[1][each]])
        if xLStandardSortL[0][each] >= backrightOuterCoor[0]:
            pointsForFr.append([xLStandardSortL[0][each], xLStandardSortL[1][each]])
    bl = math.sqrt((((backleftTwoCoorInd[0][0]-backleftTwoCoorInd[1][0])**2 + (backleftTwoCoorInd[0][1]-backleftTwoCoorInd[1][1])**2)**(1/2)*cmDivPixB)**2-5)
    br = math.sqrt((((backrighttTwoCoorInd[0][0]-backrighttTwoCoorInd[1][0])**2 + (backrighttTwoCoorInd[0][1]-backrighttTwoCoorInd[1][1])**2)**(1/2)*cmDivPixB)**2-5)
    print("--- %s seconds ---" % (time.time() - start_time))
    return bl, br
print(x1x2('processed_img/processed2.png'))