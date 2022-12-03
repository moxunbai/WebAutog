

class ScriptEventListener():
    scriptScopes={}

    @staticmethod
    def registScriptScope(moduleScope):
        for attrName in dir(moduleScope):
            val = getattr(moduleScope,attrName)
            ScriptEventListener.scriptScopes[attrName]=val
            # print(attrName,type(val))

    @staticmethod
    def findInScope(attrName):
        if attrName in ScriptEventListener.scriptScopes:
            return ScriptEventListener.scriptScopes[attrName]
        return None    

             
