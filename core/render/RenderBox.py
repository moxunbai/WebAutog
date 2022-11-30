
from .RenderObject import RenderObject,LayoutRect
import math
 
class RenderBox(RenderObject):

    def __init__(self) -> None:
        super().__init__()
        

    def clientWidth(self):   
       
        base_width = self.frameRect['width']
        if base_width>0:
            return max(0,base_width-self.borderLeft()-self.borderRight())
        return 0

    def paddingLeft(self):
        pd = self.style.padding[3]
        p= self.containerBlock()
        if self.style.isPercentValue(pd) and p:
            return pd[0]*p.contentWidth()
        
        return pd[0]
        
    def paddingRight(self):
        pd = self.style.padding[1]
        p= self.containerBlock()
        if self.style.isPercentValue(pd) and p:
            return pd[0]*p.contentWidth()
        
        return pd[0]

    def paddingTop(self):
        pd = self.style.padding[0]
        p= self.containerBlock()
        if self.style.isPercentValue(pd) and p:
            return pd[0]*p.contentWidth()
        
        return pd[0]

    def paddingBottom(self):
        pd = self.style.padding[2]
        p= self.containerBlock()
        if self.style.isPercentValue(pd) and p:
            return pd[0]*p.contentWidth()
        
        return pd[0]

    def marginTop(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        return self.style.marginTop(parentContentWidth)
    def marginRight(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        return self.style.marginRight(parentContentWidth)
    def marginBottom(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        return self.style.marginBottom(parentContentWidth)
    def marginLeft(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        return self.style.marginLeft(parentContentWidth)

    def borderLeft(self):
        return self.style.borderLeftWidth()
        
    def borderRight(self):
        return self.style.borderRightWidth()

    def borderTop(self):
        return self.style.borderTopWidth()

    def borderBottom(self):
        return self.style.borderBottomWidth()

    def contentWidth(self):
        return self.clientWidth()-self.paddingLeft()-self.paddingRight()

    def logicHeight(self):
        return self.frameRect['height']

    def logicalTop(self):
        return self.frameRect['y']
        
    def logicalLeft(self):
        return self.frameRect['x']

    def setLogicalHeight(self,h) :
        self.frameRect['height']=h   

    def setLogicalWidth(self,w) :
        self.frameRect['width']=w   

    def isIntrinsicHeight(self):
        return self.style.isIntrinsicHeight()
