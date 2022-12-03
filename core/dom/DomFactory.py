
from .DOMObject import DOMObject
from .HTMLHtmlElement import HTMLHtmlElement
from .HTMLCanvasElement import HTMLCanvasElement
from .HTMLScriptElement import HTMLScriptElement 

def createDomObject(tag,attrs):
    if tag == 'script':
        return HTMLScriptElement(tag,attrs)
    elif tag == 'canvas':
        return HTMLCanvasElement(tag,attrs)  
    else:
        return DOMObject(tag,attrs)