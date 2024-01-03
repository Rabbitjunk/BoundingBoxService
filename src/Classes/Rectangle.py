
import json

import numpy as np
class Point:
    def __init__(self, top, left):
        self.top = top
        self.left = left

    def __str__(self):
        return f"Point(top={self.top}, left={self.left})"

    def to_json(self):
        return {'top': self.top, 'left': self.left}

    @classmethod
    def from_json(cls, data):
        return cls(top=data['top'], left=data['left'])


class Rectangle:
    def __init__(self, pointUL, pointUR, pointLL, pointLR):
        self.pointUL = pointUL
        self.pointUR = pointUR
        self.pointLL = pointLL
        self.pointLR = pointLR
    
    @classmethod
    def init_with_coordinates(cls, pointUL_left, pointUL_top, pointUR_left, pointUR_top, pointLL_left, pointLL_top, pointLR_left, pointLR_top):
        pointUL = Point(left=pointUL_left, top=pointUL_top)
        pointUR = Point(left=pointUR_left, top=pointUR_top)
        pointLL = Point(left=pointLL_left, top=pointLL_top)
        pointLR = Point(left=pointLR_left, top=pointLR_top)
        return cls(pointUL, pointUR, pointLR, pointLL)


    def __str__(self):
        return f"Rectangle with points: {self.pointUL}, {self.pointUR}, {self.pointLL}, {self.pointLR}"

    def to_json(self):
        return {
            'pointUL': self.pointUL.to_json(),
            'pointUR': self.pointUR.to_json(),
            'pointLL': self.pointLL.to_json(),
            'pointLR': self.pointLR.to_json()
        }

    @classmethod
    def from_json(cls, data):
        pointUL = Point.from_json(data['pointUL'])
        pointUR = Point.from_json(data['pointUR'])
        pointLL = Point.from_json(data['pointLL'])
        pointLR = Point.from_json(data['pointLR'])
        return cls(pointUL, pointUR, pointLL, pointLR)
    
    def hight(self):
        middelUp = (int(self.pointUL.top) +int(self.pointUR.top))/2
        middelDown = (int(self.pointLL.top) +int(self.pointLR.top))/2
        return round(middelDown-middelUp)
    
    def width(self):
        middelleft = (self.pointUL.left +self.pointLL.left)/2
        middelright = (self.pointUR.left +self.pointLR.left)/2
        return round(middelleft-middelright)
    
    def __len__(self):
        return 1

def serialize_rectangles(rectangles):
    return [rectangle.to_json() for rectangle in rectangles]

def deserialize_rectangles(json_data):
    return [Rectangle.from_json(data) for data in json_data]

def rectangles_to_array(rectangles):
    # Erstelle ein leeres NumPy-Array mit der passenden Form
    array = np.empty((len(rectangles), 4, 2))

    # Fülle das Array mit den Koordinaten der Punkte der Rechtecke
    for i, rectangle in enumerate(rectangles):
        array[i, 0, :] = [rectangle.pointUL.left, rectangle.pointUL.top]
        array[i, 1, :] = [rectangle.pointUR.left, rectangle.pointUR.top]
        array[i, 2, :] = [rectangle.pointLR.left, rectangle.pointLR.top]
        array[i, 3, :] = [rectangle.pointLL.left, rectangle.pointLL.top]

    return array

