
import re 
from functools import cmp_to_key

class DOMObject():
    
    

    def __init__(self, tag,attrs):
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
                 
    
    def addChild(self,obj):
        obj.parent=self
        self.children.append(obj)  
        return obj
    def setData(self,data):
        self.data=data
        # print('self tag',self.tag,self.data,'======',data)

    
    def caclDomStyle(self,cssRules):

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
            return sorted([x for x in cssRules if matchRule(self,x)],key=cmp_to_key(comp))
            # return [x for x in cssRules if matchRule(dom,x)].sort(key=cmp_to_key(lambda x1,x2:x1['weight']>x2['weight']))
        