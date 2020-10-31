import cv2 
import numpy as np 
import matplotlib.pyplot as plt 

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
def x1x2(file_name):
    img = grab_cut(file_name) 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    corners = cv2.goodFeaturesToTrack(gray_img, 300, 0.1, 10) 
    corners = np.int0(corners) 
    #=============================key point ====================================
    xL = []
    yL = []
    for each in corners: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    ######
            x, y = i.ravel() 
            cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
    plt.imshow(img) 
    plt.show()
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows() 
    ######
    #copyright, GeeksforGeeks @hachiman_20
    minyL = sorted(yL)[0:5]
    upperBound = []; slopeL = []; slope2L = []; tempL = []; temp2L = []; innerUpperBound = []
    for each in minyL:
        upperBound.append([xL[yL.index(each)], each])
        xL.remove(xL[yL.index(each)])
        yL.remove(each)
    indicationLine = max(yL[xL.index(min(xL))], yL[xL.index(max(xL))])
    for each in yL:
        if each < indicationLine and len(tempL) <= 7:
            tempL.append(each)
    for each in tempL:
        temp2L.append([xL[yL.index(each)], each])
        xL.remove(xL[yL.index(each)])
        yL.remove(each)
    for each in upperBound[1:5]:
        slopeL.append((each[1]-upperBound[0][1])/(each[0]-upperBound[0][0]))
    for each in upperBound:
        if each in [upperBound[0], upperBound[slopeL.index(min(slopeL))+1]]:
            pass
        else:
            innerUpperBound.append(each)
    tempL = temp2L
    for each in temp2L:
        if each in innerUpperBound or each in upperBound:
            temp2L.remove(each)
        else:
            if each[1]-innerUpperBound[0][1] > 50:
                slope2L.append((each[1]-innerUpperBound[0][1])/(each[0]-innerUpperBound[0][0]))
            else:
                temp2L.remove(each)
    slopeL = []
    for each in tempL:
        if each in innerUpperBound or each in upperBound:
            tempL.remove(each)
        else:
            if each[1]-innerUpperBound[1][1] > 50:
                slopeL.append((each[1]-innerUpperBound[1][1])/(each[0]-innerUpperBound[1][0]))
            else:
                tempL.remove(each)
    innerLowerBoundaries = [temp2L[slope2L.index(max(slope2L))], tempL[slopeL.index(min(slopeL))]]
    #innerLowerL = ((innerLowerBoundaries[0][0]-innerLowerBoundaries[1][0])**2+(innerLowerBoundaries[0][1]-innerLowerBoundaries[1][1])**2)**(1/2)
    innerUpperL = ((innerUpperBound[0][0]-innerUpperBound[1][0])**2+(innerUpperBound[0][1]-innerUpperBound[1][1])**2)**(1/2)
    #meanL = (innerLowerL+innerUpperL)/2#unneeded because innerUpper != innerLower
    cmDivPixB = 26/innerUpperL# extremely important!!
    #Use pythagoras to calculate the len of pixel of the height!((innerUpperbound[0][0]-innerLowerBoundaries[0][0])**2 + (innerUpperbound[0][1]-innerLowerBoundaries[0][1])**2)**(1/2)
    bl = ((innerUpperBound[0][0]-innerLowerBoundaries[0][0])**2 + (innerUpperBound[0][1]-innerLowerBoundaries[0][1])**2)**(1/2) * cmDivPixB
    br = ((innerUpperBound[1][0]-innerLowerBoundaries[1][0])**2 + (innerUpperBound[1][1]-innerLowerBoundaries[1][1])**2)**(1/2) * cmDivPixB #여기에는 실제 길이/픽셀 비를 곱한다.
    xL = []; yL = []; slopeL = []
    for each in corners: 
        for i in each:
            xL.append(i[0])
            yL.append(i[1])
    outerUpperBound = [[sorted(xL)[0], yL[xL.index(sorted(xL)[0])]], [sorted(xL)[-1], yL[xL.index(sorted(xL)[-1])]]]
    outerLowerBound = [[xL[yL.index(sorted(yL)[-1])], sorted(yL)[-1]], [xL[yL.index(sorted(yL)[-2])], sorted(yL)[-2]]]
    for each in outerLowerBound:
        slopeL.append((each[1]-outerUpperBound[0][1])/(each[0]-outerUpperBound[0][0]))
    outerLowerBound[slopeL.index(max(slopeL))]
    outerLowerBound[slopeL.index(min(slopeL))]
    lowerL = ((outerLowerBound[0][0]-outerLowerBound[1][0])**2 + (outerLowerBound[0][1]-outerLowerBound[1][1])**2)**(1/2)
    upperL = ((outerUpperBound[0][0]-outerUpperBound[1][0])**2 + (outerUpperBound[0][1]-outerUpperBound[1][1])**2)**(1/2)
    cmDivPixF = 30/((lowerL+upperL)/2)
    fl = ((outerUpperBound[0][0]-outerLowerBound[slopeL.index(max(slopeL))][0])**2 + (outerUpperBound[0][1]-outerLowerBound[slopeL.index(max(slopeL))][1])**2)**(1/2)
    fr = ((outerUpperBound[1][0]-outerLowerBound[slopeL.index(min(slopeL))][0])**2 + (outerUpperBound[1][1]-outerLowerBound[slopeL.index(min(slopeL))][1])**2)**(1/2)
    fl *= cmDivPixF
    fr *= cmDivPixF
    return bl, br
print(x1x2(str(input())))