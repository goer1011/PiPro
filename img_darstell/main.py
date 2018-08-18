##
 #  @filename   :   main.cpp
 #  @brief      :   2.7inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 16 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd2in7
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def main():
    epd = epd2in7.EPD()
    epd.init()
    ImageDrawer('Ali')
    # display images from Image
    epd.display_frame(epd.get_frame_buffer(Image.open('IsThere.bmp')))

def ImageDrawer(name = 'Müller',there = 'ist nicht da'):
    #Image Size ( it is horizontal )
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    # Create a white mask 
    mask = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)   
    #Create font
    font = ImageFont.truetype('/home/pi/PiPro/img_darstell/font/BEBAS.ttf', 15)
    #Create a Draw object than allows to add elements (line, text, circle...) 
    draw = ImageDraw.Draw(mask)
    #Some Text
    draw.text((EPD_HEIGHT/4,EPD_WIDTH/2), 'Prof. {} {} '.format(name, there),font = font fill = 0)
    #Save the picture on disk ( now create a new Image with vertikal orientation)
    neu = Image.new('1',(EPD_WIDTH, EPD_HEIGHT),255)
    #rotate the image in mask created 90 degree
    neu = mask.transpose(Image.ROTATE_90)
    neu.save('IsThere.bmp',"bmp")

if __name__ == '__main__':
    main()
