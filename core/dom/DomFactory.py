
from .DOMObject import DOMObject
from .HTMLHtmlElement import HTMLHtmlElement
from .HTMLScriptElement import HTMLScriptElement


def createDomObject(tag,attrs):
    if tag == 'script':
        return HTMLScriptElement(tag,attrs)
    else:
        return DOMObject(tag,attrs)