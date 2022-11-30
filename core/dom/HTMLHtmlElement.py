from .DOMObject import DOMObject

class HTMLHtmlElement(DOMObject):

    def __init__(self, tag, attrs):
        super().__init__(tag, attrs)
        