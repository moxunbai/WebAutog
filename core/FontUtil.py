import numpy as np
import freetype 


class TureTypeLoader():

    def __init__(self,ttf) -> None:
        self._ttfFace = freetype.Face(ttf)


    def genTextBitmap(self,text,fontSize):
            
        self._ttfFace.set_char_size(fontSize * 64)

        prev_char = 0
        pen = freetype.Vector()
        
        hscale = 1.0
        matrix = freetype.Matrix(int(hscale) * 0x10000, int(1.2 * 0x10000), \
                int(0.0 * 0x10000), int(1.1 * 0x10000))
        curPen = freetype.Vector()
        penTranslate = freetype.Vector()
        
        imgList = []

        for everyChar in text:
            self._ttfFace.set_transform(matrix, penTranslate)
            self._ttfFace.load_char(everyChar)
            kerning = self._ttfFace.get_kerning(prev_char, everyChar)
            pen.x += kerning.x
            slot = self._ttfFace.glyph
            bitmap = slot.bitmap

            curPen.x = pen.x
            curPen.y = pen.y - slot.bitmap_top * 64
            imgList.append(self.getWordBitmap(  bitmap, curPen,fontSize))
            

            pen.x += slot.advance.x
            prev_char = curPen

    def getWordBitmap(self,bitmap,pen,fontSize):

        cols = bitmap.width
        rows = bitmap.rows
        img=np.zeros(shape=(fontSize+1,fontSize+1))
        glyph_pixels = bitmap.buffer

        offset_x=0
        offset_y=0
        if fontSize>rows:
            offset_y = int((fontSize-rows)/2)
        if fontSize>cols:
            offset_x = int((fontSize-cols)/2)

        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    try: 
                        imx_x= offset_x+ col
                        imx_y=rows- row-offset_y
                        img[imx_x][imx_y] = 1
                        
                    except:
                        continue
        img=(img/255)**1.25              
        return img        
