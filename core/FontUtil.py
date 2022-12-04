import numpy as np
import freetype 
from freetype.raw import * 

class TureTypeLoader():

    def __init__(self,ttf) -> None:
        self._ttfFace = freetype.Face(ttf)


    def genTextBitmap(self,text,fontSize,color):

        flags = FT_LOAD_RENDER| FT_LOAD_FORCE_AUTOHINT| FT_LOAD_NO_HINTING 
        self._ttfFace.set_char_size(fontSize * 64)
        
        imgList = []

        for everyChar in text:
            # self._ttfFace.set_transform(matrix, penTranslate)
            self._ttfFace.load_char(everyChar,flags)
            # kerning = self._ttfFace.get_kerning(prev_char, everyChar)
            # pen.x += kerning.x
            slot = self._ttfFace.glyph
            bitmap = slot.bitmap

            imgList.append(self.getWordBitmap(  bitmap,  fontSize,color))
            
        return imgList    

    def getWordBitmap(self,bitmap, fontSize,color):

        # print('color',color)
        cols = bitmap.width
        rows = bitmap.rows
        # img=np.zeros(shape=(fontSize+1,fontSize+1))
        img=np.zeros(shape=(cols+1,rows+1,3),dtype=np.float32)
        img.fill(-1)
        glyph_pixels = bitmap.buffer

        offset_x=0
        offset_y=0
    
        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    try: 
                        imx_x= offset_x+ col
                        imx_y=rows- row-offset_y
                        grayRate = glyph_pixels[row * cols + col]/255 
                        img[imx_x][imx_y][0] = grayRate*color[0]
                        img[imx_x][imx_y][1] = grayRate*color[1]
                        img[imx_x][imx_y][2] = grayRate*color[2]
                        # img[imx_x][imx_y][0] = grayRate 
                        # img[imx_x][imx_y][1] = grayRate 
                        # img[imx_x][imx_y][2] = grayRate 
                        
                    except:
                        continue
        # img=(img/255)**1.25              
        return img        
