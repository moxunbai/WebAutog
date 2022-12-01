

class RenderLineBoxList():

    def __init__(self) -> None:
        self.m_firstLineBox=None
        self.m_lastLineBox=None


    def firstLineBox(self):
        return self.m_firstLineBox

    def lastLineBox(self):
        return self.m_lastLineBox

    def checkConsistency():
        pass

    def appendLineBox(self,inlineFlowBox):
        pass

    def removeLineBox(self,inlineFlowBox):
        pass
    def deleteLineBoxTree(self):
        pass

    def deleteLineBoxes(self):
        pass

    # def extractLineBox(self,inlineFlowBox):
    #     pass
    # def attachLineBox(self,inlineFlowBox):
    #     pass
    
    # def dirtyLineBoxes():
    #     pass
    # def dirtyLinesFromChangedChild(self, parent,   child):
    #     pass
 