import json
import os
from src.Classes.Rectangle_helper import calcDistanceBetween, calcDistancebetweenStart, combineRectangles

from src.Classes.Rectangle import Point, Rectangle, deserialize_rectangles, serialize_rectangles




def refineRegions(filepath):
    if os.path.exists(filepath):
            allRectangles =loadRawRectangle(filepath)
            refinedRectangles=[]
            tempRectangleGroup =[]
            refinedRectangles = combineRowRectangles(allRectangles)
            refinedRectangles = combineColumRectangles(refinedRectangles)
            #ToDo: Speichern in die Folder 
            if  len(tempRectangleGroup)>0:
                refinedRectangles.append(combineRectangles(tempRectangleGroup))

            return  json.dumps(serialize_rectangles(refinedRectangles), indent=2)
    else:
        print("Filepath empty")

def combineRowRectangles(allRectangles):
    refinedRectangles=[]
    tempRectangleGroup =[]
    for i in (range(len(allRectangles))):
        tempRectangleGroup.append(allRectangles[i])
        if i!=len(allRectangles)-1:
            if abs(int(allRectangles[i].pointUR.top)-int(allRectangles[i+1].pointUL.top))<20 &abs(int(allRectangles[i].pointLR.top)-int(allRectangles[i+1].pointLL.top))<20 &abs(int(allRectangles[i].pointUR.left)-int(allRectangles[i+1].pointUL.left))<400 :
                tempRectangleGroup.append(allRectangles[i+1])
            elif len(tempRectangleGroup)>0:
                refinedRectangles.append(combineRectangles(tempRectangleGroup))
                tempRectangleGroup=[]
    return refinedRectangles


def combineColumRectangles(allRectangles):
    refinedRectangles=[]
    tempRectangleGroup =[]
    for i in (range(len(allRectangles))):
        tempRectangleGroup.append(allRectangles[i])
        if i!=len(allRectangles)-1:
            if (calcDistancebetweenStart(allRectangles[i],allRectangles[i+1])<20)&(calcDistanceBetween(allRectangles[i],allRectangles[i+1]) < round(allRectangles[i].hight()/2)):
                tempRectangleGroup.append(allRectangles[i+1])
            elif len(tempRectangleGroup)>0:
                refinedRectangles.append(combineRectangles(tempRectangleGroup))
                tempRectangleGroup=[]
    return refinedRectangles

def loadRawRectangle(filepath):
    allRectangles=[]
    dateien = [element for element in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, element))]
    # Ausgabe der Dateien
    for datei in dateien:
        datei_pfad =  os.path.join(filepath, datei)
        if  datei_pfad.lower().endswith(".txt".lower()):
            with open(datei_pfad, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    splitlist =(line.replace('\n','').split(','))
                    if len(splitlist)==8:
                        rededRectangle=Rectangle(Point(left=splitlist[0],top=splitlist[1]),Point(left=splitlist[2],top=splitlist[3]),Point(left=splitlist[6],top=splitlist[7]),Point(left=splitlist[4],top=splitlist[5]))
                        allRectangles.append(rededRectangle)
    return allRectangles  

def loadRefinedRectangle(filepath):
    allRectangles=[]
    dateien = [element for element in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, element))]
    # Ausgabe der Dateien
    for datei in dateien:
        datei_pfad =  os.path.join(filepath, datei)
        if  datei_pfad.lower().endswith(".json".lower()):
            with open(datei_pfad, "r") as read_file:
                decoded_data = json.load(read_file)
                allRectangles = deserialize_rectangles(decoded_data)
    return allRectangles   
    
def cretaFolderIfNeeded(folder_path):
    if os.path.exists(folder_path)== False:
        os.makedirs(folder_path)
