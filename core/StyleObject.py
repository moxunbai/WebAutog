

import taichi as ti
from .FieldBase import FieldBase
from .common import splitStr,parsePxValue
from . import FieldManager as fm

vec3 = ti.math.vec3
vec4 = ti.math.vec4


def getDistanceVal(v):
    if v is None:
        return [0.,-1]
    if v.endswith('px'): 
        return [parsePxValue(v),0]
    elif v.endswith('%'):
        return [float(v[:-1]) / 100, 1]   
    return [0.,0]    
# def parseD4(v):

def parseColor(s):  # sourcery skip: avoid-builtin-shadow
    if s is None or len(s) not in [4,7]:
        return [0,0,0]
    hex=  s[1:]
    if len(hex)==3:
        return [int(hex[i:i+1]+hex[i:i+1], 16)/255 for i in range(3)]
    return [int(hex[i:i+2], 16)/255 for i in (0, 2, 4)]
aa=parseColor('#ff0000') # (255, 165, 1)
print('color',aa)
def parseBorder(s):
    vals = splitStr(s)
    w = max(0,parsePxValue(vals[0])) if len(vals)>0 else 0
    btype = 1 if len(vals)>1 and vals[1]=='dashed' else 0
    color = parseColor(vals[2]) if len(vals)>2 else [0,0,0]
    return w,btype,color    

def setBorder(style,name,s):
    i=0
    if name=='border-right':
        i=1
    elif name == 'border-top':
        i=2
    elif name == 'border-bottom':
        i=3
    if s !='none':
        style.border_use[i]=1
        w,btype,color =parseBorder(s)
        style.border_width[i]=w
        style.border_type[i]=btype
        style.border_color[i]=color
    else:
        style.border_use[i]=0

def setPaddingMargin(target,prifix,name,s):
    i=0
    if name == f'{prifix}-right':
        i=1
    elif name == f'{prifix}-bottom':
        i=2
    elif name == f'{prifix}-left':
        i=3
    target[i]= getDistanceVal(s)      

def parsePaddingMargin(v):
    vals = splitStr(v)
    pd = [[0.,0],[0.,0],[0.,0],[0.,0]]
    match len(vals):
        case 1:
            dv = getDistanceVal(vals[0])
            pd=[dv,dv,dv,dv]
        case 2:
            dv0 = getDistanceVal(vals[0])
            dv1 = getDistanceVal(vals[1])
            pd=[dv0,dv1,dv0,dv1]  
             
        case 3:
            dv0 = getDistanceVal(vals[0])
            dv1 = getDistanceVal(vals[1])
            dv2 = getDistanceVal(vals[2])
            pd[0]=dv0  
            pd[1]=dv1  
            pd[2]=dv2   
        case 4:
            dv0 = getDistanceVal(vals[0])
            dv1 = getDistanceVal(vals[1])
            dv2 = getDistanceVal(vals[2])
            dv3 = getDistanceVal(vals[3])
            pd=[dv0,dv1,dv2,dv3]  
             
        case _:
            pass
   
    return pd
@ti.dataclass
class StyleStruct():
    
    pos_type:int
    left:float
    right:float
    top:float
    bottom:float
    width:float
    height:float
    display:int
    margin:vec4
    padding:vec4

    z_index:int

    bg_use:int
    bg_color_type:int
    bg_color:ti.types.vector(6, float)

    opacity:float

    border_use:vec4
    border_type:vec4
    border_width:vec4
    border_radius:vec4
    border_color:ti.types.vector(12, float)

    font_size:float
    font_weight:float
    font_color:vec3

class MultDistValue():

    def __init__(self,v,t) -> None:
        self.v=v
        self.t=t

    def isPercent(self):
        return self.t==1    

class StyleObject(FieldBase):

    def __init__(self,data) -> None:
        super().__init__()
        self.data=data   
        
        
        self.pos_type=0
        self.left=[0.0,0]
        self.right=[0.0,0]
        self.top=[0.0,0]
        self.bottom=0.0
        self.width=[0.0,-1]
        self.max_width=[0.0,-1]
        self.min_width=[0.0,-1]
        self.height=[0.0,-1]
        self.display=0
        # 0 :none 1:left 2:right
        self.float_type=0
        self.margin=[[0.,0],[0.,0],[0.,0],[0.,0]]
        self.padding=[[0.,0],[0.,0],[0.,0],[0.,0]]

        self.z_index=0

        self.bg_use=0
        self.bg_color_type=0
        self.bg_color=[0.,0.,0.]

        self.opacity=1.0

        self.border_use=[0,0,0,0]
        self.border_type=[0.,0.,0.,0.]
        self.border_width=[0.,0.,0.,0.]
        self.border_radius=[0.,0.,0.,0.]
        self.border_color=[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]

        self.font_size=0.0
        self.font_weight=0.0
        self.font_color=[0.,0.,0.]
        self.setDate(data) 

    @staticmethod
    def getBaseName():
       return 'StyleObject'
    
    def setDate(self,data):
        for k,v in data.items():
            match k:
                case 'display':
                    if v == 'inline':
                        self.display=1
                    elif v == 'none':
                        self.display=-1
                case 'float':
                    if v == 'left':
                        self.float_type=1
                    elif v == 'right':
                        self.float_type=2
                case 'position':
                    if v =='relation':
                        self.pos_type =1
                    elif v== 'absolute':
                        self.pos_type=2 
                    elif v=='fixed':
                        self.pos_type=3
                case 'width':
                    if v:
                       self.width=getDistanceVal(v)   
                       
                case 'height':
                    if v:
                       self.height=getDistanceVal(v)   
                case 'margin':
                    if v:
                           
                        self.margin=parsePaddingMargin(v)    
                case 'left'|'right'|'top'|'bottom'|'height'|'width':
                    if v:
                       setattr(self,k,getDistanceVal(v)) 
                       
                case 'border':
                    if v:
                       if v !='none':
                           self.border_use=[1,1,1,1]
                           w,btype,color =parseBorder(v)
                           self.border_width=[w,w,w,w]
                           self.border_type=[btype,btype,btype,btype]
                           self.border_color=[color,color,color,color]
                       else:
                          self.border_use=[0,0,0,0]
                case 'border-left'|'border-right'|'border-top'|'border-bottom':   
                    setBorder(self,k,v)           
                case 'padding':   
                     
                    self.padding=parsePaddingMargin(v)      

                case 'padding-left'|'padding-right'|'padding-top'|'padding-bottom':   
                    setPaddingMargin(self.padding,'padding',k,v)  
                case 'margin-left'|'margin-right'|'margin-top'|'margin-bottom':   
                    setPaddingMargin(self.margin,'margin',k,v) 
                case 'background'|'background-color':
                    if v!='none':
                        self.bg_use=1
                        self.bg_color= parseColor(v)   
                case 'font-size':
                    if v!='none':
                        self.font_size=max(10,parsePxValue(v))     
                case 'color':
                    if v!='none': 
                        self.font_color= parseColor(v)  
                        
                case 'opacity':
                    opy = float(v)
                    
                    self.opacity=0. if opy<0.  else 1. if opy>1 else opy
                     
                case _:
                    pass            
    
    def borderLeftWidth(self):
        return 0 if self.border_use[0]==0 else self.border_width[0]
    def borderRightWidth(self):
        return 0 if self.border_use[1]==0 else self.border_width[1]
    def borderTopWidth(self):
        return 0 if self.border_use[2]==0 else self.border_width[2]
    def borderBottomWidth(self):
        return 0 if self.border_use[3]==0 else self.border_width[3]

    def marginLeft(self,parentContentWidth):
        marginVal = self.margin[3]
        return marginVal[0]*parentContentWidth if marginVal[1]==1 else marginVal[0] 
         
    def marginRight(self,parentContentWidth):
        marginVal = self.margin[1]
        return marginVal[0]*parentContentWidth if marginVal[1]==1 else marginVal[0] 
    def marginTop(self,parentContentWidth):
        marginVal = self.margin[0]
        return marginVal[0]*parentContentWidth if marginVal[1]==1 else marginVal[0] 
    def marginBottom(self,parentContentWidth):
        marginVal = self.margin[2]
        return marginVal[0]*parentContentWidth if marginVal[1]==1 else marginVal[0] 

    @staticmethod
    def isPercentValue(v):
        return bool(v and v[1]==1)

    def isBlock(self):
        return self.display==0   

    def isFloat(self):
        return self.float_type>0   
         
    def floatLeft(self):
        return self.float_type==1    

    def floatRight(self):
        return self.float_type==2  



    def cssWidth(self,parentContentWidth):
        if self.width[1] == -1:
           return parentContentWidth
        elif self.width[1] == 1:
            return  self.width[0]*parentContentWidth
        elif self.width[1] == 0:
            return  self.width[0]
        return 0.     
    def cssHeight(self,parentContentWidth):
        if self.height[1] == -1:
           return 0
        elif self.height[1] == 1:
            return  self.height[0]*parentContentWidth
        elif self.height[1] == 0:
            return  self.height[0]
        return 0.     

    def isIntrinsicHeight(self):
        return self.height[1]!=-1  

    def isIntrinsicWidth(self):
        return self.width[1]!=-1  

    def isPercent(self,name):
        vals = splitStr(name,'-')
        if vals and len(vals)>0:
            mainName = vals[0]
            v=getattr(self,mainName)  
            if  v:
                if len(vals)==0:
                    return self.isPercentValue(v)
                else:
                    i=0
                    match vals[1]:
                        case 'right':
                            i=1
                        case 'bottom':
                            i=2
                        case 'left':
                            i=3
                        case _:
                            i=0
                    return   self.isPercentValue(v[i])                      

    def fontSize(self):
        return self.font_size
        
    def fontColor(self):
        return self.font_color

    def fillField(self):
        if styleFields := fm.findFieldByName(self.getBaseName()):
            styleField=styleFields[self.getAddr()]
            styleField.bg_use=self.bg_use
            if self.bg_use == 1:
                for i in range(6):
                    styleField.bg_color[i] = self.bg_color[i%3]
            styleField.border_use = self.border_use
            styleField.border_use=vec4(self.border_use)
            # styleField.border_width[0]=self.border_width[0]
            # styleField.border_width[1]=self.border_width[1]
            # styleField.border_width[2]=self.border_width[2]
            # styleField.border_width[3]=self.border_width[3]
            styleField.border_width = vec4(self.border_width )
            colors =self.border_color[0]+self.border_color[1]+self.border_color[2]+self.border_color[3]
            styleField.border_color = ti.Vector(colors)
            styleField.border_type = vec4(self.border_type)
            styleField.border_radius = vec4(self.border_radius)
            styleField.opacity = self.opacity