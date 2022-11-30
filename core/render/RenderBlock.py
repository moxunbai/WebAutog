from .RenderBox import RenderBox


class RenderBlock(RenderBox):

    def __init__(self,dom) -> None:
        super().__init__()
        self.dom=dom
        def onFrameRectChange(name,oldVal,newValue):
            # print('frameRect change',self.dom.tag,name,newValue)
            self.fillInFieldFrameRect()

        for k in self.frameRect:
            self.frameRect.addListener(k,onFrameRectChange)

    def caclWidth(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        cssw = self.style.cssWidth(parentContentWidth)
        logicWidth = self.style.cssWidth(parentContentWidth)+self.borderLeft()+self.borderRight()+self.paddingLeft()+self.paddingRight()
        self.frameRect['width']=  min(parentContentWidth,logicWidth) 

    def caclLogicHeight(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        cssh = self.style.cssHeight(parentContentWidth)
        logicHeight = cssh+self.borderTop()+self.borderBottom()+self.paddingTop()+self.paddingBottom()
        self.frameRect['height']=logicHeight

    def computeTop(self):
        t=0.
        if previous := self.previousSibling(): 
            # print('computeTop==previous==',self.dom.tag,self.dom.id,previous.dom.tag,previous.dom.id)
            t = previous.logicalTop()+previous.logicHeight() + self.marginTop()   
        else: 
           

            t=p.logicalTop()+p.paddingTop()+ self.marginTop()   if (p := self.containerBlock()) else 0
        self.frameRect['y']=t    
        # print('self top===:',self.dom.tag,self.dom.id,t,self.marginTop(),self.frameRect['y'],self.logicalTop() )

    def computeLeft(self):
        l=p.logicalLeft()+p.paddingLeft()+ self.marginLeft()   if (p := self.containerBlock()) else 0
        self.frameRect['x']=l

    def layout(self):
        self.caclWidth()
        self.computeTop()
        self.computeLeft()
        self.caclLogicHeight()
        child = self.firstChild()
        while child: 
           child.layout()
           if not self.style.isIntrinsicHeight():
              self.setLogicalHeight(self.logicHeight() + child.logicHeight()+child.marginTop())
           child = child.nextSibling()

         
