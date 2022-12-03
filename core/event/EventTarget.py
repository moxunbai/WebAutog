


class EventTarget():

    def __init__(self) -> None:
        self._eventlListenerMap={}


    def addEventListener(self,eventType,listener,useCapure=False):
        if eventType not in self._eventlListenerMap:
            self._eventlListenerMap[eventType]=set()  

        self._eventlListenerMap[eventType].add(listener)   

    def removeEventListener(self,eventType,listener,useCapure=False): 
        if eventType  in self._eventlListenerMap:
            self._eventlListenerMap[eventType].remove(listener)     

    def dispatchEvent(self,event):
        eventType = event.type 
        if eventType =='mouseenter':
          print(eventType,self._eventlListenerMap.keys(),event.clientX)
        if eventType and eventType in  self._eventlListenerMap:
            for listener in self._eventlListenerMap[eventType] :
                 event.target=self
                 listener.exec(event)    