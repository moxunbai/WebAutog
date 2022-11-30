
from core.CssBgObject import *
from core import HTMLEngine 
import taichi as ti


 

ti.init(arch=ti.gpu)
 
cssFields = CssBgFields()
cssFields.setup_data_cpu(20)

HTMLEngine.load('01.html',None)

