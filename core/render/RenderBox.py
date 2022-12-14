
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

    def contentTop(self):
        return max(0.,self.logicalTop()-self.paddingTop())    

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

    def logicalWidth(self) :
        return self.frameRect['width']
    def logicalHeight(self) :
        return self.frameRect['height']

    def isIntrinsicHeight(self):
        return self.style.isIntrinsicHeight()

    def previousFloatLeft(self):
        pre = self.previousSibling()
        while pre :
            if   pre.isFloat() and   pre.floatLeft():
                break
            else:
                pre = pre.previousSibling()
        return pre  

    def previousFloatRight(self):
        pre = self.previousSibling()
        while pre :
            if   pre.isFloat() and   pre.floatRight():
                break
            else:
                pre = pre.previousSibling()
        return pre    

    def isDomLeaf(self):
        return self.dom and self.dom.isLeaf()
    def hitTest(self,event):
        if event is None:
            return None
        target = None
        posInClientX=event.clientX
        posInClientY=event.clientY
        rangeX=(self.logicalLeft(),self.logicalLeft()+self.logicalWidth())
        rangeY=(self.logicalTop(),self.logicalTop()+self.logicalHeight())
        
        if posInClientX>=rangeX[0] and posInClientX<=rangeX[1] and posInClientY>=rangeY[0] and posInClientY<=rangeY[1]:
            # print(posInClientX,posInClientY,rangeX,rangeY,self.dom.tag)
            if self.isDomLeaf():
                # print(posInClientX,posInClientY,rangeX,rangeY,self.dom.tag)
                # print('hit self',self.dom.tag,self.dom.id)
                return self
            for child in self.children:
                target= child.hitTest(event)
                if target:
                    #  print('hit child',target.dom.tag,target.dom.id)
                     break
            if target is None:
                target=self
        return target                
