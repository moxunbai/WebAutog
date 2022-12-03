from .ScriptEventListener import ScriptEventListener
class EventListener():

    def __init__(self,funcObject,useCapure=False) -> None:
        
        self.funcObject=funcObject
        self.useCapure=useCapure

    def getFuncCallable(self):

        if type(self.funcObject) == str:
            if scopeAttr := ScriptEventListener.findInScope(self.funcObject):
                return scopeAttr
        return self.funcObject       


    def exec(self,event):
        func = self.getFuncCallable()
        if callable(func):
           func(event)