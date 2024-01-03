from src.Classes.Rectangle import Point, Rectangle

def calcDistanceBetween(Rectangle_upper,Rectangle_lower):
    distance = int(Rectangle_lower.pointUL.top)-int(Rectangle_upper.pointLL.top) 
    return distance

def calcDistancebetweenStart(Rectangle1,Rectangle2):
    distance = int(Rectangle1.pointUL.left)-int(Rectangle2.pointUL.left) 
    return abs(distance)


def combineRectangles(listRecangles):
    """
    Create a new rectangle that have the max size out of all rectangles
    """
    newRectangle = listRecangles[0]
    for rectangle in listRecangles:

        if int(newRectangle.pointUL.left) > int(rectangle.pointUL.left):
            newRectangle.pointUL.left = rectangle.pointUL.left
        if int(newRectangle.pointUL.top) > int(rectangle.pointUL.top):
            newRectangle.pointUL.top = rectangle.pointUL.top

        if int(newRectangle.pointUR.left) < int(rectangle.pointUR.left):
            newRectangle.pointUR.left = rectangle.pointUR.left
        if int(newRectangle.pointUR.top) > int(rectangle.pointUR.top):
            newRectangle.pointUR.top = rectangle.pointUR.top

        if int(newRectangle.pointLL.left) > int(rectangle.pointLL.left):
            newRectangle.pointLL.left = rectangle.pointLL.left
        if int(newRectangle.pointLL.top) < int(rectangle.pointLL.top):
            newRectangle.pointLL.top = rectangle.pointLL.top

        if int(newRectangle.pointLR.left) < int(rectangle.pointLR.left):
            newRectangle.pointLR.left = rectangle.pointLR.left
        if int(newRectangle.pointLR.top) < int(rectangle.pointLR.top):
            newRectangle.pointLR.top = rectangle.pointLR.top


    return Rectangle(Point(left=newRectangle.pointUL.left,top=newRectangle.pointUL.top),Point(left=newRectangle.pointUR.left,top=newRectangle.pointUR.top),
                    Point(left=newRectangle.pointLL.left,top=newRectangle.pointLL.top),Point(left=newRectangle.pointLR.left,top=newRectangle.pointLR.top))