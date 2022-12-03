
from .Event import EventType
from .MouseEvent import MouseEvent

import taichi as ti

mouseEnterDoms=[]
lastMouseEnterDom = None
def generateFromTaichiEvent( tiEvent,clientSize):
        # print()
        event=None
        pos=tiEvent.pos
        
        if tiEvent.key == ti.GUI.LMB:
            event=MouseEvent()
            if tiEvent.type ==  ti.GUI.PRESS:
                event.type=EventType.MOUSE_DOWN
            elif tiEvent.type ==  ti.GUI.RELEASE:   
                event.type=EventType.MOUSE_UP    

        elif  tiEvent.key == ti.GUI.MOVE:
             event=MouseEvent()
             event.type= EventType.MOUSE_MOVE  
        if event:
            event.clientX=int(pos[0]*clientSize[0])
            event.clientY=int(clientSize[1]-clientSize[1]*pos[1]) 

        return event    


def dispatchEvent(targetDom,event):
    if isinstance(event,MouseEvent) and event.type==EventType.MOUSE_MOVE:
        global mouseEnterDoms

        if targetDom in mouseEnterDoms:
            if mouseEnterDoms.index(targetDom) <len(mouseEnterDoms)-1:
                outDom = mouseEnterDoms.pop()
                newEvent = event.clone()
                newEvent.type =EventType.MOUSE_LEAVE
                outDom.dispatchEvent(newEvent)
        else:
                event.type =EventType.MOUSE_ENTER  
                mouseEnterDoms.append(targetDom)   

  
    targetDom.dispatchEvent(event)
