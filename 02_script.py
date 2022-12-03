
from demo_pt import RayTracingRender
from core.HTMLEngine import document
from core import FieldManager as fm
import time
import numpy as np


canvasDom = document.getElementById('render_canvas')
if canvasDom :

    canvasW = canvasDom.width()
    canvasH = canvasDom.height()
    print(canvasW,canvasH)
    rayTracer = RayTracingRender((canvasW,canvasH))
    fm.addFieldDeclare(rayTracer.field_declare)
    fm.addFieldPlaced(rayTracer.setup_data_cpu)

    last_t = time.time()
     
    interval = 10
    def renderFrame():
        rayTracer.render()
        rayTracer.count += 1 
        # print(rayTracer.count,interval,rayTracer.count % interval )
        if rayTracer.count % interval == 0:
            rayTracer.tonemap(rayTracer.count)
           
            return rayTracer.tonemapped_buffer.to_numpy()
           
        return None    

    canvasDom.setPaintCallback(renderFrame)     

def startRender(e=None): 
    canvasDom.paint()
    document.requestAnimationFrame(startRender)   

       

def hoverIn(e): 
    e.target.addCssClass('hover')
def hoverOut(e): 
    e.target.removeCssClass('hover')
