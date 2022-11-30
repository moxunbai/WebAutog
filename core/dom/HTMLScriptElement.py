
from .DOMObject import DOMObject

class HTMLScriptElement(DOMObject):
    
    def __init__(self, tag, attrs):
        super().__init__(tag, attrs)
        print('HTMLScriptElement attrs',attrs)
        if   attrs:
            for (name,val) in attrs:
                if name == 'src':
                   self.src = val