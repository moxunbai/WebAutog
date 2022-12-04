
from demo_pt import RayTracingRender
from core.HTMLEngine import document
from core import FieldManager as fm
import time
import numpy as np

rayTracer=None
canvasDom = document.getElementById('render_canvas')
sppDom = document.getElementById('spp')
if canvasDom :

    canvasW = canvasDom.width()
    canvasH = canvasDom.height()
    
    rayTracer = RayTracingRender((canvasW,canvasH))
    fm.addFieldDeclare(rayTracer.field_declare)
    fm.addFieldPlaced(rayTracer.setup_data_cpu)

    last_t = time.time()
     
    interval = 10
    def renderFrame():
        global rayTracer
        rayTracer.render()
        # print(rayTracer.count,interval,rayTracer.count % interval )
        rayTracer.count += 1 
        if rayTracer.count % interval == 0:
            rayTracer.tonemap(rayTracer.count)
           
            return rayTracer.tonemapped_buffer.to_numpy()
           
        return None    

    canvasDom.setPaintCallback(renderFrame)     


activeDom=None


isStart=False

def startRender(e=None):
    global isStart 
    global activeDom

    isStart=True
    if activeDom and e:
        activeDom.removeCssClass('active')
    elif e:
        activeDom=e.target
        activeDom.addCssClass('active')        
    canvasDom.paint()
    sppDom.setData(rayTracer.count)
    if isStart:
        document.requestAnimationFrame(startRender)  

def stopRender(e=None): 
    global isStart 
    global activeDom
    if not isStart:
        return 
    
    isStart=False
    if activeDom :
        activeDom.removeCssClass('active')
    elif e:
        activeDom=e.target
    activeDom.addCssClass('active')    

       

def hoverIn(e): 
    e.target.addCssClass('hover')
def hoverOut(e): 
    e.target.removeCssClass('hover')
