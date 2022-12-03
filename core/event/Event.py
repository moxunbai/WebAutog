class EventType():
    CLICK='click'
    MOUSE_ENTER='mouseenter'
    MOUSE_MOVE='mousemove'
    MOUSE_LEAVE='mouseleave'
    MOUSE_DOWN='mousedown'
    MOUSE_UP='mouseup'


class Event():

    def __init__(self) -> None:
        self.type=""
        self.target=None
        self.currentTarget=None
        self.path=[]
        self.clientX=0
        self.clientY=0


    def preventDefault(self):
        pass

    def stopPropagation(self):
        pass    

    def clone(self):
        pass