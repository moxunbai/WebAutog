
from .RenderBox import RenderBox

class RenderInline(RenderBox):

    def __init__(self,dom) -> None:
        super().__init__()
        self.dom=dom

    
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
            t = previous.logicalTop()   
        else: 
           

            t=p.logicalTop()+p.paddingTop()   if (p := self.containerBlock()) else 0
        self.frameRect['y']=t    
        # print('self top===:',self.dom.tag,self.dom.id,t,self.marginTop(),self.frameRect['y'],self.logicalTop() )

    def computeLeft(self):
        l=p.logicalLeft()+p.paddingLeft()+ self.marginLeft()   if (p := self.containerBlock()) else 0
        self.frameRect['x']=l
    

    # def layout(self):
    #     # 生成 line box(行框) list 
    #     # 行框最宽是block containing box 决定
