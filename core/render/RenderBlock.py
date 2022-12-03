from .RenderBox import RenderBox
from ..event.EventListener import EventListener

class RenderBlock(RenderBox):

    def __init__(self,dom) -> None:
        super().__init__()
        self.dom=dom
        if dom:
            dom.render = self
        def onFrameRectChange(name,oldVal,newValue):
            self.fillInFieldFrameRect()

        for k in self.frameRect:
            self.frameRect.addListener(k,onFrameRectChange)

        self.watchDom()    

    def updateStyles(self,e): 
        newStyles = self.dom.computeStyles(self.dom.cssRules) 
        self.style.setData(newStyles)
        print('newStyles',newStyles['color'],self.style.font_color)
        self.m_needsUpdateField = False
        self.reLayout()
        self.rePaint()
                 

    def watchDom(self):
        if self.dom:
            self.dom.addEventListener('cssChange',EventListener(self.updateStyles))        

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
        isFloat=self.isFloat()
        previous = None
        # if isFloat:
        #    previous = self.previousFloatLeft() if self.floatLeft() else self.previousFloatRight()
        # else:
        #    previous = self.previousSibling()    
        previous = self.previousSibling()    
        if previous : 
            # print('computeTop==previous==',self.dom.tag,self.dom.id,previous.dom.tag,previous.dom.id)
            availableWidth = 0
            # if p := self.containerBlock():
            #     if isFloat:
            #         availableWidth = p.contentWidth()-previous.logicalLeft()-previous.clientWidth() if self.floatLeft() else 
            if not previous.isFloat():        
               t = previous.logicalTop()+previous.logicHeight() + self.marginTop()   
            else:
               if p := self.containerBlock():
                    availableWidth = p.contentWidth()-previous.logicalLeft()-previous.clientWidth() if self.floatLeft()   else p.contentWidth()-previous.logicalLeft() 
               if availableWidth >self.logicalWidth():
                  t = previous.logicalTop() 
               else:
                   t = previous.logicalTop()+previous.logicHeight()                
        else: 
            t=p.logicalTop()+p.paddingTop()+p.borderTop()+ self.marginTop()   if (p := self.containerBlock()) else 0
        self.frameRect['y']=t    
        # print('self top===:',self.dom.tag,self.dom.id,t,self.marginTop(),self.frameRect['y'],self.logicalTop() )

    def computeLeft(self):
        previous = self.previousSibling()   
        l=0 
        p = self.containerBlock()
        if previous : 
            if not previous.isFloat():  
               l=p.logicalLeft()+p.paddingLeft()+ self.marginLeft()   if p else 0
            else:
               availableWidth = 0
               if p := self.containerBlock():
                    availableWidth = p.contentWidth()-previous.logicalLeft()-previous.clientWidth()-self.marginLeft() if self.floatLeft()   else p.contentWidth()-previous.logicalLeft() -self.marginRight()
               if availableWidth >self.logicalWidth():
                  l = previous.logicalLeft()+ previous.logicalWidth()+self.marginLeft()
               else:  
                   if p :
                     l= p.logicalLeft()+p.paddingLeft()+ self.marginLeft() if self.floatLeft() else p.logicalLeft()-p.logicalLeft()-p.paddingRight()- self.marginRight()
        else:
            l= p.logicalLeft()+p.paddingLeft()+ self.marginLeft()  if p else 0.            
        self.frameRect['x']=l

    def layout(self):
        self.caclWidth()
        self.computeTop()
        self.computeLeft()
        self.caclLogicHeight()
        curMaxHeight=0
        curX=0
        baseline=self.paddingTop()
        child = self.firstChild()
        if self.dom.id:
            print(self.dom.id,self.logicalLeft(),self.logicalTop())
        while child: 
           child.layout()
        #    if child.isInline():

           if not self.style.isIntrinsicHeight() and self.dom.tag != 'html':
               
              self.setLogicalHeight(self.logicHeight() + child.logicHeight()+child.marginTop())
           child = child.nextSibling()

         
