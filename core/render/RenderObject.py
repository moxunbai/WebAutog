from ..FieldBase import FieldBase
import taichi as ti 
from ..event.Event  import EventType

vec2 = ti.math.vec2
vec3 = ti.math.vec3
vec4 = ti.math.vec4

@ti.dataclass
class RenderObjectStruct():
    parent:int
    style_addr:int
    is_text:int
    frame_rect:vec4
    client_area:vec2
    content_area:vec2
    relat_pos:vec2
    abs_pos:vec2

class LayoutRect(dict):
    
    def __init__(self,v):
        super().__init__(v)
        self.__listener__=None

    def __setitem__(self, item, value):
        super(LayoutRect, self).__setitem__(item, value)
        if self.__listener__ is not None and item in  self.__listener__:
            for cb in self.__listener__[item]:
                cb(item,self[item],value)

    def addListener(self,name,callback):
        if self.__listener__ is None:
           self.__listener__ = {name:[]}
        if name not in self.__listener__:
            self.__listener__[name]=[]
        self.__listener__[name].append(callback)        


class RenderObject(FieldBase):

    view_dom_tags=['html','body','div','p','a','span','img','canvas','button','input','h1','h2']
    def __init__(self) -> None:
        super().__init__()
        self.root = None
        self.parent = None
        self.m_previousSibling = None
        self.m_nextSibling = None
        self.children = []
        self.doc = None
        self.dom = None
        self.frameRect = LayoutRect({'width':0,'height':0,'x':0,'y':0})
        self.style = None
        self.positioned = False
        self.isText = False
        self.inline = False
        self._isBlock = False
        self.posChildNeedsLayout = True
        self.m_needsLayout = True
        self.m_needsUpdateField = True
        self._paintCallback = None
        
    def setDocument(self,doc):
        self.doc=doc

    def addChild(self,obj,root=None):
        if obj is None :
            return    
        if root is None:
            root = self
            while root:
                if root.parent:
                    root=root.parent
                else:
                    break    
         
        obj.root=root
        obj.parent=self
        oldLen = len(self.children)
        if oldLen>0:
            self.children[oldLen-1].m_nextSibling = obj
            obj.m_previousSibling = self.children[oldLen-1]
        self.children.append(obj)
        self.needsLayout = True

    def firstChild(self):
        return self.children[0] if len(self.children)>0 else None
        
    def previousSibling(self):
        return self.m_previousSibling    

    def nextSibling(self):
        return self.m_nextSibling    

    def needsLayout(self) ->bool:
        return True

    def layout(self):
        pass

    def paintText(self):
        pass

    def reLayout(self):
        root = self.root
        if root:
            root.layout() 
               
    def rePaint(self):
        root = self.root
        if root:
            # print('rePaint',root)
            root.paint() 
               

    def paint(self):
        self.style.fillField()
        if self.m_needsUpdateField:
            self.m_needsUpdateField=False
        if thisField := self.doc.getObjStructField(self):
            if self.style:
                thisField.style_addr = self.style.getAddr() 
            if self._paintCallback and callable(self._paintCallback):
                image = self._paintCallback()
                
                if image is not None:
                    # print(image)
                    self.renderInTiByExternal(self.getAddr(),image)
                # else:
                #     self.renderInTi(self.getAddr())      
            else:   
                if self.dom:     
                    self.renderInTi(self.getAddr())  
            # self.renderInTi(self.getAddr())  
            # if self.dom:
            #     print('paint',self.dom.tag,self.getAddr())
            if self.isText:
                self.paintText()      
        child = self.firstChild()
        
        while child: 
           child.paint()
           child = child.nextSibling()

    @staticmethod
    def getBaseName():
        return 'RenderObject'

    def isBlock(self):
        return   self.style.isBlock() if self.style else False 
    def isFloat(self):
        return   self.style.isFloat() if self.style else False 
    def floatLeft(self):
        return   self.style.floatLeft() if self.style else False 
    def floatRight(self):
        return   self.style.floatLeft() if self.style else False 

    def isInline(self):
        return self.inline    

    def containerBlock(self):
        p = self.parent
        
        while p and not p.isBlock():
            # print('pp=',p.dom.tag)
            if p.parent:
                p=p.parent
            else:
                break    
        return p

    def hitTest(self,pointer):
        pass    

    def fillInFieldFrameRect(self):
        if thisField := self.doc.getObjStructField(self):
            thisField.frame_rect[0]=self.frameRect['width']
            thisField.frame_rect[1]=self.frameRect['height']
            thisField.frame_rect[2]=self.frameRect['x']
            thisField.frame_rect[3]=self.frameRect['y']
            
            # print('fillInFieldFrameRect',self.getAddr(),self.dom.tag,thisField.frame_rect[0],thisField.frame_rect[1],thisField.frame_rect[2],thisField.frame_rect[3])
            # thisField.frame_rect=vec4(self.frameRect['width'],self.frameRect['height'],self.frameRect['x'],self.frameRect['y'])

    @staticmethod
    def is_view(dom):
        return dom and dom.tag in RenderObject.view_dom_tags;
    @staticmethod
    def is_visible(style):
        return style is not None and 'display' in style and style['display']!='none';

    def setPaintCallback(self,callback):
        self._paintCallback = callback 
    
    @ti.func
    def inBorder(self,i, j,frame_width,frame_height, s):
        in_pos=-1
        border_color=vec3(0.)
        border_use = s.border_use
        border_width=s.border_width
        if border_use[0]==1 and border_width[0]>0:
           w=border_width[0]
           if i<w:
               in_pos=0
        if border_use[1]==1 and border_width[1]>0:
            w=border_width[1]
            if i>=frame_width-w:
               in_pos=1 
        if border_use[2]==1 and border_width[2]>0:
            w=border_width[2]
            if j>=frame_height-w:
               in_pos=2 
        if border_use[3]==1 and border_width[3]>0:
            w=border_width[3]
            if j<=w:
               in_pos=3 
        if in_pos>-1:
        #    print(frame_width,frame_height) 
           for k in ti.static(range(12)):
               if k>=in_pos and k<in_pos+3 :
                  border_color[k%3]=s.border_color[k]
                #   border_color=vec3(s.border_color[in_pos],s.border_color[in_pos+1],s.border_color[in_pos+2])        
        return in_pos,border_color    

    @ti.func 
    def caclColor(self,heightl_c,lowl_c,opacity):
        result = heightl_c
        if lowl_c[0]>=0 and lowl_c[1]>=0 and lowl_c[2]>=0:
            result =heightl_c*(1-opacity)+lowl_c*opacity
        return result

    
    @ti.kernel
    def renderInTiByExternal(self,objAddr:ti.i32,image:ti.types.ndarray()): 
        obj_field = self.doc.f_render_objects[objAddr]
        (frame_w,frame_h)=self.doc.f_layer_frames.shape
        frame_rect =ti.cast(obj_field.frame_rect,ti.i32) 
        w=frame_rect[0]
        h=frame_rect[1]
        x=frame_rect[2]
        y=frame_rect[3]
        # print(w,h,x,y,frame_h)
        for i,j in ti.ndrange(w, h):
                abs_x = i+x
                abs_y = frame_h-y-j
                c = vec3(image[i,j,0],image[i,j,1],image[i,j,2])
                # print(abs_x,abs_y)
                # self.doc.f_layer_frames[abs_x,abs_y]=vec3(0)
                if abs_x>=0 and abs_x<frame_w and abs_y>=0 and abs_y <frame_h:
                    self.doc.f_layer_frames[i,j]=c

    @ti.func
    def diffSelColor(self,colorA,colorB):
        rst=colorA
        delte =0.6
        d= colorB.norm() 
        if d>delte:
            rst=colorB
        return rst    

    @ti.kernel
    def renderInTi(self,objAddr:ti.i32): 
        obj_field = self.doc.f_render_objects[objAddr]
        (frame_w,frame_h)=self.doc.f_layer_frames.shape
        frame_rect =ti.cast(obj_field.frame_rect,ti.i32) 

        # for m in ti.static(range(4)):
        w=frame_rect[0]
        h=frame_rect[1]
        x=frame_rect[2]
        y=frame_rect[3]
        style_addr = obj_field.style_addr
        # print('renderInTi',objAddr,x,y,w, h)
        for i,j in ti.ndrange(w, h):
            if style_addr>-1:
                s = self.doc.f_styles[style_addr]
                opacity=s.opacity
                abs_x = i+x
                abs_y = frame_h+j-h
                in_pos,border_color  = self.inBorder(i,j,w,h,s)
                if in_pos>-1:
                    # print(border_color)
                    self.doc.f_layer_frames[abs_x,abs_y]=self.caclColor(self.doc.f_layer_frames[abs_x,abs_y],border_color,opacity)
                elif s.bg_use==1:
                    bg_color=vec3(0.)
                    for k in ti.static(range(3)):
                        bg_color[k]=s.bg_color[k]
                    # if objAddr == 2:
                    #     print('===',bg_color)
                    # print(bg_color)    
                    self.doc.f_layer_frames[abs_x,abs_y]=self.caclColor(self.doc.f_layer_frames[abs_x,abs_y],bg_color,opacity)   
            

    @ti.kernel
    def renserChar(self,charBitmap:ti.types.ndarray(),x:ti.i32,y:ti.i32,objAddr:ti.i32):
        obj_field = self.doc.f_render_objects[objAddr]
        style_addr = obj_field.style_addr
        s = self.doc.f_styles[style_addr]
        (frame_w,frame_h)=self.doc.f_layer_frames.shape
        opacity=s.opacity
        font_color=s.font_color
        # print('font_color',x,y,charBitmap.shape[1])
        for i,j in ti.ndrange(charBitmap.shape[0],charBitmap.shape[1]):
            if charBitmap[i,j,0]>-1:
                # fontColor =vec3(font_color[0]*charBitmap[i,j,0],font_color[1]*charBitmap[i,j,1],font_color[2]*charBitmap[i,j,2]) 
                abs_x=i+x
                abs_y=frame_h-y-charBitmap.shape[1]+j
                #   fontColor=(fontColor/255.)**1.25
                # fontColor=ti.pow(fontColor/255., 1.25)
                 
                fontColor = vec3(charBitmap[i,j,0],charBitmap[i,j,1],charBitmap[i,j,2])
                
                #   self.doc.f_layer_frames[abs_x,abs_y]=fontColor
                bg=self.doc.f_layer_frames[abs_x,abs_y]
                # fontColor+=0.2*bg
                # self.doc.f_layer_frames[abs_x,abs_y]=self.diffSelColor(bg,fontColor)
                # g=fontColor[0]*0.2126*255 + 0.7152*255*fontColor[1] + 0.0722*255*fontColor[2]
                # g=fontColor[0]+fontColor[1]+fontColor[2]
                # if g<0.4:
                #     fontColor+=bg
                # self.doc.f_layer_frames[abs_x,abs_y]=self.caclColor(bg,fontColor,opacity) 
                self.doc.f_layer_frames[abs_x,abs_y]=fontColor/255 