

from html.parser import HTMLParser
from html.entities import name2codepoint
from .CSSParser import CSSParser 


from .dom import createDomObject

class HTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.cssParser = CSSParser()
    
    def handle_starttag(self,tag,attrs):
        # global self.curDom
        newObj = createDomObject(tag,attrs)
        if self.curDom is not None:
            self.curDom.addChild(newObj)  
        else:
            self.root =  newObj   
        
        self.curDom =newObj 
        self.eleStack.append(self.curDom)
    def handle_endtag(self,tag):
        
        while len(self.eleStack)>0:
            self.curDom=self.eleStack.pop()
            if self.curDom.tag == tag:
                self.curDom=self.curDom.parent
                break
            
        # print('endtag','<%s>'% tag)
        
    def handle_startendtag(self,tag,attrs):
        if self.curDom is not None:

            self.curDom.addChild(createDomObject(tag,attrs))
            
        
    def handle_data(self,data):
        if data is not None and data.strip() != '':
           c=data.strip()
           self.curDom.setData(c)
           if self.curDom.tag == 'style':
               self.cssParser.parseIn(c)
        
    def handle_comment(self,data):
        pass
        # print('<!--',data,'-->')
        
    def handle_entityref(self,name):
        pass
        # print('&%s;'%name)
        
    def handle_charref(self,name):
        pass
        # print('&#%s;'%name)
        
    def parse(self,content):
        if content is None or content.strip()=='' :
            return None
        self.curDom=None
        self.eleStack=[]
        self.feed(content.strip())
        return self.root