
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
            print(self.text,fontSize,fontColor) 
            self.textBitmaps = self.doc.ttfLoader.genTextBitmap(self.text,fontSize,fontColor)  
            # print(self.textBitmaps)  

    def paintText(self):
        x =int( self.logicalLeft())
        y = int(self.logicalTop())
        for bitmap in self.textBitmaps:
            # print(type(bitmap))
           self.renserChar(bitmap,x,y,self.getAddr())  
           x+= bitmap.shape[0]     