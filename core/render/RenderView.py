
from .RenderBlock import RenderBlock
from .RenderInline import RenderInline

class RenderView(RenderBlock):

    def __init__(self,dom) -> None:
        super().__init__(dom)
        # self.dom=dom
        # self.doc=doc
        

    def setDocument(self, doc):
        super().setDocument(doc)
        winOption =self.doc.option
        self.setLogicalWidth(winOption['viewportWidth'])
        self.setLogicalHeight(winOption['viewportHeight'])

    def caclWidth(self):
        pass
        # self.frameRect['width']=self.logicWidth()+logicWidth 
    def isIntrinsicHeight(self):
        return True    
    @staticmethod
    def genObj(dom,style):
        if dom is None or not RenderView.is_view(dom):
            return None
        if dom.tag == 'html':
            return  RenderView(dom)
        d = style['display']
        if d=='block':
            return RenderBlock(dom)
        elif d=='inline':
            return RenderInline(dom) 
        else :
             return None
             
           