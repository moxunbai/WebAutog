
from .render import RenderObjectStruct,RenderObject
from .StyleObject import StyleStruct,StyleObject
import taichi as ti
from . import FieldManager as fm
import importlib
import os
import sys

field_max_len=6

@ti.data_oriented
class HTMLDocument():

    f_render_objects = None
    f_styles = None
    f_layer_frames=None
    classtype_tield={}
    option={}

    def __init__(self, rootDom, option=None) -> None:
        if option is None:
            option = {'viewportWidth':900,'viewportHeight':800}
        self.children = [rootDom]
        HTMLDocument.option=option
        fm.addFieldDeclare(HTMLDocument.__declare_field__)
        fm.addFieldPlaced(HTMLDocument.__place_field__)

    @staticmethod
    def __declare_field__():
        HTMLDocument.f_render_objects=RenderObjectStruct.field()
        HTMLDocument.f_styles=StyleStruct.field()
        HTMLDocument.f_layer_frames=ti.Vector.field(3,ti.f32)
        fm.registFields(RenderObject.getBaseName(),HTMLDocument.f_render_objects)
        fm.registFields(StyleObject.getBaseName(),HTMLDocument.f_styles)
        
        
    @staticmethod
    def __place_field__():
        ti.root.dense(ti.i,field_max_len).place(HTMLDocument.f_render_objects,HTMLDocument.f_styles)
        print(HTMLDocument.option['viewportWidth'])
        ti.root.dense(ti.ij,(HTMLDocument.option['viewportWidth'],HTMLDocument.option['viewportHeight'])).place(HTMLDocument.f_layer_frames)
        
        
    @staticmethod
    def getObjStructField(obj):
        classname = obj.getBaseName()
        # if classname in HTMLDocument.classtype_tield:
        #     fa = obj.getAddr()
        #     return HTMLDocument.classtype_tield[classname][fa]
        if fd := fm.findFieldByName(classname):
           fa = obj.getAddr()
           return fd[fa]    
 
    # def getElementById(self,domId):
    #     return self.
    def initScripts(self):
        scripts = []

        def findScripts(node):
            print('node',node.tag)
            if node.tag == 'script':
                scripts.append(node)
            else:
                if node.children:
                    for c in node.children:
                        findScripts(c)    

        for dom in self.children:
            findScripts(dom)   

        path = os.path.abspath('.')
        print('cur path',path, os.path.realpath(sys.argv[0]) )
        global document 
        document = self
        for scriptDom in scripts:
            if scriptDom.src:
                moduleName =  scriptDom.src.split('.')[0]     
                moduleScope = importlib.__import__( moduleName,globals() )       
                print('moduleName',moduleName,moduleScope)   
                moduleScope.onClick({'ssss':112})


