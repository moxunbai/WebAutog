
from .Event import Event,EventType
import time

class UIEvent(Event):

    def __init__(self) -> None:
        super().__init__()
        self.altKey=False
        self.ctrlKey=False
        self.shiftKey=False
        self.metaKey=False
        self.timeStamp=time.time()
 