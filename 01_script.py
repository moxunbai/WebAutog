from core.HTMLEngine import document 

def onClick(e):
    print('click hahahaha',e.target.tag)

def hoverIn(e):
    print('hoverIn ',e.target.tag)
    e.target.addCssClass('hover')
def hoverOut(e):
    print('hoverOut ',e.target.tag)
    e.target.removeCssClass('hover')

a = globals()

print('this is script',  document)  

