
from core.CssBgObject import *
from core import HTMLEngine
import taichi as ti
import sys

ti.init(arch=ti.gpu)


if __name__ == '__main__':
    html_fn=None
    if len(sys.argv)==1:
        html_fn ="00.html"
    else:
        html_fn = sys.argv[1]
    HTMLEngine.load(html_fn,{'viewportWidth':800,'viewportHeight':750})
