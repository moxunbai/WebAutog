from .UIEvent import UIEvent


class MouseEvent(UIEvent):

    def __init__(self) -> None:
        super().__init__()

    def clone(self):
        newObj = MouseEvent() 
        newObj.type=self.type   
        newObj.clientX=self.clientX
        newObj.clientY=self.clientY
        newObj.altKey=self.altKey
        newObj.ctrlKey=self.ctrlKey
        newObj.shiftKey=self.shiftKey
        newObj.metaKey=self.metaKey
        newObj.timeStamp=self.timeStamp
        return newObj