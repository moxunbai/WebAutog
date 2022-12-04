
from .HTMLParser import *
from .CSSParser import CSSParser
from .HTMLDocument import HTMLDocument
from .StyleObject import StyleObject
from .render import RenderView,RenderObject
import re
from functools import cmp_to_key
from  . import FieldManager as fm
import taichi as ti
import numpy as np
from .event.EventManager import generateFromTaichiEvent,dispatchEvent

parser = HTMLParser()
   

global document 
def load(fname,option):
    with open(fname,'r') as f:
        c = f.read()
        global document
        root = parser.parse(c)
        document = HTMLDocument(root,option)
        renderView = buildRenderTree()
        
        document.initScripts()
        fm.fieldsBuild()
        fm.fieldsPlace()
        clientWidth=document.option['viewportWidth']
        clientHeight=document.option['viewportHeight']
        renderView.layout()
        renderView.paint()
        gui = ti.GUI('Hello World!', (clientWidth, clientHeight))
        i = 0
        interval = 10
      
        while gui.running:
            if gui.get_event():
                mouse_x, mouse_y = gui.get_cursor_pos()
                # print(gui.event.key,gui.event.type,mouse_x,gui.event.pos[1])
                if event := generateFromTaichiEvent(gui.event, (clientWidth, clientHeight)):
                    if targetRender := fintHitRenderObject(renderView,event): 
                        targetDom = targetRender.dom
                        # if targetDom.id:
                        #      print(targetDom.tag,targetDom.id,mouse_x, mouse_y,event.clientX,event.clientY)
                        dispatchEvent(targetDom,event)
            document.handleAnimationFrames()  
            # document.getElementById('render_canvas').paint()       
            if i%interval ==0:    
                gui.set_image(HTMLDocument.f_layer_frames)
                gui.show()
                 
                # image = HTMLDocument.f_layer_frames.to_numpy(dtype=np.float32)
                # print(image[99,100,:])
            i+=1    

 
def buildRenderTree():
    global document
    global parser
    
    cssParser = parser.cssParser
    cssRules = cssParser.rule_list
    
    def walkDomTree(dom):
       
        if dom is None or not RenderObject.is_view(dom):
            # print('Dom no renderObj:',dom.tag)
            return
        
        computedStyle = dom.computeStyles(cssRules)
        
        if not RenderObject.is_visible(computedStyle):
            # print('hide Dom',dom.tag,computedStyle)
            return    
        # print('computedStyle',dom.tag,len(dom.children))
        renderObj = RenderView.genObj(dom,computedStyle)
        # print('new Render',r)
        if renderObj:
            # print(dom.tag,dom.id,computedStyle)
            renderObj.style=StyleObject(computedStyle)
            # print('newStyles=======', dom.classNames, renderObj.style.getAddr())
            renderObj.setDocument(document) 
            if dom.data:
                textObj=RenderView.genTextObj(dom.data)
                textObj.style=renderObj.style
                # textObj.style=StyleObject(computedStyle)
                textObj.setDocument(document)
                renderObj.addChild(textObj,renderObj.root)
            for child in dom.children:
                childR = walkDomTree(child)
                # print('child',child.tag)
                if childR:
                   renderObj.addChild(childR,renderObj.root)      
                 
                
        return renderObj

    # walkDomTree(renderView)
    renderView = walkDomTree(document.children[0])
    # if renderView:
    #    renderView.setDocument(document) 
    return renderView   


def fintHitRenderObject(renderObj,event):
    return renderObj.hitTest(event)
    