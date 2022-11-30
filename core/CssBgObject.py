

import core.FieldManager as fm
import taichi as ti

vec3 = ti.math.vec3

@ti.dataclass
class CssBgStruct:
    color: vec3
    opacity: float
    use: int

class  CssBgFields:
    
    def __init__(self) -> None:
        self.fields = CssBgStruct.field() 

    def setup_data_cpu(self,size):
        ti.root.dense(ti.i,8).place(self.fields)
        self.size = size

    def setItem(self,i,name,value):
        if name == 'color':
            self.fields[i].color = vec3(value)    
    def getItem(self,i,name):
        if name == 'color':  
            return  self.fields[i].color

class CssBgObject():
    
    __addr__=-1
    fields = None
    props = {}
    field_max_len=0

    def __init__(self,fields:CssBgFields) -> None:
        self.fields=fields
        self.field_max_len=fields.size
        self.__addr__=fm.malloc(self)
        

    def fillFields(self,pos):
        pass


    def setProperty(self,name,value):
        self.props[name]=value
        if self.__addr__<0:
            return
        
        self.fields.setItem(self.__addr__,name,value)

    def getProperty(self,name):
        print('=====getProperty',self.props)
        if name in self.props:
           v = self.fields.getItem(self.__addr__,name) 
           print(name,v)
           return self.props[name]
        else:
            return

    def getAddr(self):
        return self.__addr__

    def __del__(self):
        fm.free(self)