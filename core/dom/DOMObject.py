
import re 
from functools import cmp_to_key
from ..event.EventListener import EventListener

from ..event.EventTarget import EventTarget 
from ..event.Event import Event 
from ..CSSParser import CSSParser
from ..HTMLDocument import HTMLDocument


def createAttributeEventListener(dom):
    if dom:
        atrrDict = dom.attr_dict
        # print(dom.tag,atrrDict)
        for k,v in atrrDict.items():
            k=k.lower()
            if k.startswith('on'):
                eventType = k[2:]
                print('createAttributeEventListener eventType',eventType,v,dom.id)
                dom.addEventListener(eventType,EventListener(v))
                
class DOMObject(EventTarget):
    
    def __init__(self, tag,attrs):
        super().__init__()
        self.render=None
        self.parent=None
        self.id = None
        self.data = None 
        self.styles = {}
        self.attr_dict = {}
        self.classNames = []
        self.children = []
        self.tag = tag
        self.attrs = attrs
        if len(attrs) >0:
        #  print('attr',attrs)
            for (name,val) in attrs:
                # print(name,val)
                self.attr_dict[name]=val
                if val is not None:
                    if name == 'class':
                        strClassName = re.sub(' +',' ',val).strip()
                        if len(strClassName)>0:
                            self.classNames=strClassName.split(' ')
                    elif name == 'id':
                        self.id = val 
        if self.id:                 
             HTMLDocument.setInIdMap(self.id,self)
        createAttributeEventListener(self)                     
                    
    def addChild(self,obj):
        obj.parent=self
        self.children.append(obj)  
        return obj
    def setData(self,data):
        self.data=data
      
    def isLeaf(self):
        return len(self.children)==0

    def emitCssChange(self):
        event =Event()
        event.type = 'cssChange'  
        self.dispatchEvent(event)

    def addCssClass(self,className):
        if className not in self.classNames:
            self.classNames.append(className)
            self.emitCssChange()

    def removeCssClass(self,className):   
        if className in self.classNames:
            self.classNames.remove(className)
            self.emitCssChange()
            

    
    def computeStyles(self,cssRules):
            self.cssRules=cssRules
            def matchRule(dom,rule):
                if dom is None:
                    return False
                selectorText = rule['selector'].selectorText
                l = re.sub(' +',' ',selectorText).strip().split(' ')
                is_matched = True
                for i in range(len(l)-1,-1,-1):
                    if dom is None:
                        return False
                    tag,id,styles,classNames = dom.tag,dom.id,dom.styles,dom.classNames
                    t=l[i]
                    
                    
                    if t == '*':
                        continue
                    if t.startswith('#')  :
                        is_matched = id == t[1:]
                        break
                    elif t.startswith('.') :
                        is_matched = t[1:]  in classNames 
                        break
                    elif t!=tag:
                        is_matched = False
                        break
                    
                    dom = dom.parent
                return is_matched
            def comp(x1,x2):
                if x1['weight']>x2['weight']:
                    return 1
                elif x1['weight']<x2['weight']:  
                    return -1
                else:
                    return 0 
            # print([x for x in cssRules if matchRule(dom,x)])        
            matchedStyles =  sorted([x for x in cssRules if matchRule(self,x)],key=cmp_to_key(comp))
            computedStyle = {}
            for r in matchedStyles:
                # print('rrrrr=',r)
                computedStyle.update(r['style'])
            if 'style' in self.attr_dict:
                styles = CSSParser.parse(self.attr_dict['style'])
                self.styles=styles
                computedStyle.update(styles)
            return computedStyle