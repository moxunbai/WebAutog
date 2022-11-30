
import cssutils
import os

class CSSParser():

    rule_list = []
    def __init__(self) -> None:
        # print('file===',os.path.abspath('.')+os.sep+__package__)
        path = os.path.abspath('.')+os.sep+__package__+os.sep
        with open(f'{path}useragent.css', 'r') as f:
            c= f.read()
            self.parseIn(c,0)
        

    def parseIn(self,content,weight=1):
        cssSheets = cssutils.parseString(content)
        for rule in cssSheets:
            if rule.type == rule.STYLE_RULE:
                # disp = rule.style.getProperty('display')
                rule_styles = dict(rule.style)
                # print(rule_styles)
                for selector in rule.selectorList:
                    # print('selector',selector.selectorText)
                    self.rule_list.append({'selector':selector,'style':rule_styles,'weight':weight})
                    # for name, val in rule_styles.items():
                    #     self.rule_list.append({'selector':selector,'name':name,'value':val,'weight':weight})
                    # for i in dir(selector):
                    #     print(i)

    @staticmethod
    def parse(content):
        style = cssutils.parseStyle(content)
        return dict(style)
