
from .render import RenderObjectStruct,RenderObject
from .StyleObject import StyleStruct,StyleObject
import taichi as ti
from . import FieldManager as fm
import importlib
import os
import sys
from .FontUtil import TureTypeLoader
from .event.ScriptEventListener import ScriptEventListener

field_max_len=6

@ti.data_oriented
class HTMLDocument():

    f_render_objects = None
    f_styles = None
    f_layer_frames=None
    tonemapped_buffer=None
    classtype_tield={}
    option={}
    idMapNde={}

    AnimationFrames=[]

    ttfLoader=None

    def __init__(self, rootDom, option=None) -> None:
        if option is None:
            option = {'viewportWidth':900,'viewportHeight':800}
        self.children = [rootDom]
        HTMLDocument.option=option
        fm.addFieldDeclare(HTMLDocument.__declare_field__)
        fm.addFieldPlaced(HTMLDocument.__place_field__)

        ttfPath = os.path.abspath('.')+os.sep+__package__+os.sep+'assets'+os.sep
        self.ttfLoader = TureTypeLoader(f'{ttfPath}Source_Han_Serif_CN_VF_Regular.ttf')

    @staticmethod
    def __declare_field__():
        HTMLDocument.f_render_objects=RenderObjectStruct.field()
        HTMLDocument.f_styles=StyleStruct.field()
        HTMLDocument.f_layer_frames=ti.Vector.field(3,ti.f32)
        HTMLDocument.tonemapped_buffer=ti.Vector.field(3,ti.f32)
        fm.registFields(RenderObject.getBaseName(),HTMLDocument.f_render_objects)
        fm.registFields(StyleObject.getBaseName(),HTMLDocument.f_styles)
        
        
    @staticmethod
    def __place_field__():
        ti.root.dense(ti.i,field_max_len).place(HTMLDocument.f_render_objects,HTMLDocument.f_styles)
        print(HTMLDocument.option['viewportWidth'])
        ti.root.dense(ti.ij,(HTMLDocument.option['viewportWidth'],HTMLDocument.option['viewportHeight'])).place(HTMLDocument.f_layer_frames,HTMLDocument.tonemapped_buffer)
        
        
    @staticmethod
    def getObjStructField(obj):
        classname = obj.getBaseName()
        # if classname in HTMLDocument.classtype_tield:
        #     fa = obj.getAddr()
        #     return HTMLDocument.classtype_tield[classname][fa]
        if fd := fm.findFieldByName(classname):
           fa = obj.getAddr()
           return fd[fa]    
 
    @staticmethod
    def setInIdMap(id,dom):
        HTMLDocument.idMapNde[id]=dom

    @staticmethod
    def getElementById(id):
        return HTMLDocument.idMapNde[id] if id in HTMLDocument.idMapNde else None

    @staticmethod
    def requestAnimationFrame(func):
        HTMLDocument.AnimationFrames.append(func)

    @staticmethod
    def handleAnimationFrames():
        if (HTMLDocument.AnimationFrames) and (func := HTMLDocument.AnimationFrames.pop()):
            if callable(func):
                func()
        
   
    def initScripts(self):
        scripts = []

        def findScripts(node):
            if node.tag == 'script':
                scripts.append(node)
            else:
                if node.children:
                    for c in node.children:
                        findScripts(c)    

        for dom in self.children:
            findScripts(dom)   

        
        global document 
        document = self
        for scriptDom in scripts:
            if scriptDom.src:
                moduleName =  scriptDom.src.split('.')[0]     
                moduleScope = importlib.__import__( moduleName,globals() )  
                ScriptEventListener.registScriptScope(moduleScope)     
                # print('moduleName',moduleName,moduleScope)   
                # moduleScope.onClick({'ssss':112})


