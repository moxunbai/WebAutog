
from .RenderBox import RenderBox


class RenderText(RenderBox):

    def __init__(self,text) -> None:
        super().__init__()
        self.isText =True
        self.text=text

    def setDocument(self, doc):
        super().setDocument(doc)
        self.parseText()

    def parseText(self):
        if self.doc:
            fontColor = self.style.fontColor()
            fontSize = int(self.style.fontSize())
            # print('===='+self.text+'=======')
            self.textBitmaps = self.doc.ttfLoader.genTextBitmap(self.text,fontSize,fontColor)  
            # print(self.textBitmaps)  

    def paintText(self):
        self.text=self.parent.dom.data
        x =int( self.logicalLeft())
        y = int(self.logicalTop())
        self.parseText()
        for bitmap in self.textBitmaps:
            # print(type(bitmap))
           self.renserChar(bitmap,x,y,self.getAddr())  
           x+= bitmap.shape[0]     

    
    def caclWidth(self):
        parentContentWidth = p.contentWidth() if (p := self.containerBlock()) else 0
        w = sum(bitmap.shape[0] for bitmap in self.textBitmaps)
        self.frameRect['width']=  min(parentContentWidth,w) 

    def caclLogicHeight(self):
        h=0
        for bitmap in self.textBitmaps:
            h=max(h,bitmap.shape[1] ) 
          
        self.frameRect['height']=h

    def computeTop(self):
        t=0.
        if p := self.parent:  
            t=p.logicalTop()+p.paddingTop()+p.borderTop() 
         
        self.frameRect['y']=t    
        
    def computeLeft(self):
        
        l=0  
        if p := self.parent: 
            l= p.logicalLeft()+p.paddingLeft()
                       
        self.frameRect['x']=l

    def layout(self):
        self.caclWidth()
        self.computeTop()
        self.computeLeft()
        self.caclLogicHeight()       