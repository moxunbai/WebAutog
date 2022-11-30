
from .HTMLParser import *
from .CSSParser import CSSParser
from .HTMLDocument import HTMLDocument
from .StyleObject import StyleObject
from .render import RenderView,RenderObject
import re
from functools import cmp_to_key
from  . import FieldManager as fm
import taichi as ti
import math

parser = HTMLParser()

global document 
def load(fname,option):
    with open(fname,'r') as f:
        c = f.read()
        global document
        root = parser.parse(c)
        document = HTMLDocument(root,option)
        renderView = buildRenderTree()
        fm.fieldsBuilder()
        fm.fieldsPlace()
        renderView.layout()
        renderView.paint()
        document.initScripts()
        # ro = document.f_render_objects[0]
        # print(document.f_styles)
        # print('taichi val:',document.f_styles.border_width.to_numpy())
        # print('taichi val:',document.f_render_objects.frame_rect.to_numpy())

        print('TEST=======',33/255.0)
        gui = ti.GUI('Hello World!', (document.option['viewportWidth'], document.option['viewportHeight']))
        while gui.running:
            image = HTMLDocument.f_layer_frames.to_numpy()
            # print(gui.get_cursor_pos())
            gui.set_image(image)
            gui.show()

@ti.func
def inRect(i, j, x, y, w, h):
    rst = True
    if i < x or i > x + w:
        rst =False
    if j<y or j>y+h:
        rst = False
    return rst         
 
@ti.kernel
def render(renderObjCount:ti.i32):
    for i,j in HTMLDocument.f_layer_frames:

        for k in range(renderObjCount):
            obj_field =  HTMLDocument.f_render_objects[k]  
            frame_rect = obj_field.frame_rect
             
            w=frame_rect[0]
            h=frame_rect[1]
            x=frame_rect[2]
            y=frame_rect[3]
            if  inRect(i, j, x, y, w, h):
                style_addr = obj_field.style_addr  
                if style_addr>-1:
                    s = HTMLDocument.f_styles[style_addr]
                    border_use = s.border_use
                    if border_use[0] == 1 and j==y:
                        print(j)
                        HTMLDocument.f_layer_frames[i,j]=ti.Vector([s.border_color[0],s.border_color[1],s.border_color[2]])
                        
 
def buildRenderTree():
    global document
    global parser
    
    cssParser = parser.cssParser
    cssRules = cssParser.rule_list
    
    def walkDomTree(dom):
       
        if dom is None or not RenderObject.is_view(dom):
            # print('Dom no renderObj:',dom.tag)
            return
        attr_dict = dom.attr_dict
        computedStyle = {}
        for r in dom.caclDomStyle( cssRules):
            # print('rrrrr=',r)
            computedStyle.update(r['style'])
        if 'style' in attr_dict:
            styles = CSSParser.parse(attr_dict['style'])
            dom.styles=styles
            computedStyle.update(styles)
        # print('styles',dom.tag,computedStyle)
            
        if not RenderObject.is_visible(computedStyle):
            # print('hide Dom',dom.tag,computedStyle)
            return    
        # print('computedStyle',dom.tag,len(dom.children))
        renderObj = RenderView.genObj(dom,computedStyle)
        # print('new Render',r)
        if renderObj:
            renderObj.style=StyleObject(computedStyle)
            renderObj.setDocument(document) 
            for child in dom.children:
                # print('child',child.tag)
                childR = walkDomTree(child)
                if childR:
                   renderObj.addChild(childR)      
                 
                
        return renderObj

    # walkDomTree(renderView)
    renderView = walkDomTree(document.children[0])
    # if renderView:
    #    renderView.setDocument(document) 
    return renderView   