
class EventType():
    CLICK:'click'
    MOUSE_ENTER:'mouseenter'
    MOUSE_MOVE:'mousemove'
    MOUSE_LEAVE:'mouseleave'
    MOUSE_DOWN:'mousedown'
    MOUSE_UP:'mouseup'


class EventTarget():

    def __init__(self) -> None:
        self._eventlListenerMap={}


    def addEventListener(self,eventType,listener,useCapure=False):
        if eventType not in self._eventlListenerMap:
            self._eventlListenerMap[eventType]=[]    