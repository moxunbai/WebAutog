from ..FieldBase import FieldBase
import taichi as ti 

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
        
    def setDocument(self,doc):
        self.doc=doc

    def addChild(self,obj):
        if obj is None :
            return    
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

    def paint(self):
        self.style.fillField()
        if thisField := self.doc.getObjStructField(self):
            if self.style:
                thisField.style_addr = self.style.getAddr() 
            self.renderByTi(self.getAddr())  
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

    def fillInFieldFrameRect(self):
        if thisField := self.doc.getObjStructField(self):
            # print(thisField,self.frameRect['width'])
            thisField.frame_rect[0]=self.frameRect['width']
            thisField.frame_rect[1]=self.frameRect['height']
            thisField.frame_rect[2]=self.frameRect['x']
            thisField.frame_rect[3]=self.frameRect['y']
            # thisField.frame_rect=vec4(self.frameRect['width'],self.frameRect['height'],self.frameRect['x'],self.frameRect['y'])

    @staticmethod
    def is_view(dom):
        return dom and dom.tag in RenderObject.view_dom_tags;
    @staticmethod
    def is_visible(style):
        return style is not None and 'display' in style and style['display']!='none';


    
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
        return heightl_c*(1-opacity)+lowl_c*opacity

    

    @ti.kernel
    def renderByTi(self,objAddr:ti.i32): 
        obj_field = self.doc.f_render_objects[objAddr]
        (frame_w,frame_h)=self.doc.f_layer_frames.shape
        # print(frame_h)
        frame_rect =ti.cast(obj_field.frame_rect,ti.i32) 

        # for m in ti.static(range(4)):
        w=frame_rect[0]
        h=frame_rect[1]
        x=frame_rect[2]
        y=frame_rect[3]
        style_addr = obj_field.style_addr
        if style_addr>-1:
            s = self.doc.f_styles[style_addr]
            opacity=s.opacity
            for i,j in ti.ndrange(w, h):
                abs_x = i+x
                abs_y = frame_h-j-y
                in_pos,border_color  = self.inBorder(i,j,w,h,s)
                if in_pos>-1:
                    # print(border_color)
                    self.doc.f_layer_frames[abs_x,abs_y]=self.caclColor(self.doc.f_layer_frames[abs_x,abs_y],border_color,opacity)
                elif s.bg_use==1:
                    bg_color=vec3(0.)
                    for k in ti.static(range(3)):
                        bg_color[k]=s.bg_color[k]
                    # print(bg_color)    
                    self.doc.f_layer_frames[abs_x,abs_y]+=self.caclColor(self.doc.f_layer_frames[abs_x,abs_y],bg_color,opacity)   

    @ti.kernel
    def renserChar(self,charBitmap:ti.types.ndarray(),x:ti.i32,y:ti.i32,objAddr:ti.i32):
        obj_field = self.doc.f_render_objects[objAddr]
        style_addr = obj_field.style_addr
        s = self.doc.f_styles[style_addr]
        (frame_w,frame_h)=self.doc.f_layer_frames.shape
        opacity=s.opacity
        for i,j in ti.ndrange(charBitmap.shape[0],charBitmap.shape[1]):
            # for j in range()
              abs_x=i+x+20
              abs_y=frame_h-y+j-20
              fontColor = vec3(charBitmap[i,j,0],charBitmap[i,j,1],charBitmap[i,j,2])
              if fontColor[0]>0:
                  print(abs_x,abs_y,fontColor)
              self.doc.f_layer_frames[abs_x,abs_y]=fontColor
            #   self.doc.f_layer_frames[abs_x,abs_y]=self.caclColor(self.doc.f_layer_frames[abs_x,abs_y],fontColor,opacity) 