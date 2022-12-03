
from .DOMObject import DOMObject

class HTMLCanvasElement(DOMObject):

    def __init__(self, tag, attrs):
       
        super().__init__(tag, attrs)
        

    def width(self):
       return  self.render.style.cssWidth(0)    
    def height(self):
       return  self.render.style.cssHeight(0)    

    def setPaintCallback(self,callback):
        self.render.setPaintCallback(callback)   

    def paint(self):
        self.render.paint()
