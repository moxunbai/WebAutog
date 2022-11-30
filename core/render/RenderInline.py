
from .RenderBox import RenderBox

class RenderInline(RenderBox):

    def __init__(self,dom) -> None:
        super().__init__()
        self.dom=dom