
import taichi as ti

from . import FieldManager as fm

@ti.data_oriented
class FieldBase():

    def __init__(self) -> None:
        self.__addr__ =fm.malloc(self)

    def getAddr(self):
        return self.__addr__    


    
    def __del__(self):
        fm.free(self)    