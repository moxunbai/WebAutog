
from .RenderBlock import RenderBlock
from .RenderInline import RenderInline
from .RenderText import RenderText

class RenderCanvas(RenderBlock):

    def __init__(self,dom) -> None:
        super().__init__(dom)
         
        