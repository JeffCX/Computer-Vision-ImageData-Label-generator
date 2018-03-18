#!/usr/bin/python
"""Author:Jeff Cui"""
from PIL import Image, ImageFilter
import random

#1
'''
func input image, scale, maxW, maxH
output scaled image with maxW, maxH
if scale == None, rand between 0.5 ~ 2.5
if maxW == None, INF
if maxH == None, INF'''

def scale_img(image, scale=None, maxW=None, maxH=None):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")
        width,height=image.size
        if scale!=None:
                if not isinstance(scale,(int,float)):
                        raise ValueError ("scale should an int or a float")
                width=width*scale
                height=height*scale
        else:
                num=random.randint(5,25)/10
                width=width*num
                height=height*num
        if maxW==None:
                maxW=float("inf")
        else:
                if not isinstance(maxW,(int,float)):
                        raise ValueError("max Width should an int or a float")
        if maxH==None:
                maxH=float("inf")
        else:
                if not isinstance(maxH,(int,float)):
                        raise ValueError("max Heigth should an int or a float")
        if maxW <= width:
                width=maxW
        if maxH <= height:
                height=maxH
        return image.resize((int(width),int(height)))

#2
'''
func input image
output mirrored image'''

def mirror_img(image):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")
        return image.transpose(Image.FLIP_LEFT_RIGHT)

#3
'''
func input image, rotation
output rotated image'''

def rotate_img(image,rotation=90):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")

        if not isinstance(rotation,(int)):
                raise ValueError("rotate degree should an int")

        return image.rotate(rotation,0,1)


#4
'''
func input image, scale, rotation, maxW, maxH
output image processed by all previous func'''

def process_img(image,scale=None,rotation=90,maxW=None, maxH=None):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")
        image=scale_img(image,scale,maxW,maxH)
        image=mirror_img(image)
        image=rotate_img(image,rotation)
        return image

#5
'''
func input image, mul
outpumage with thicker lines (thickness multiplied by mul)'''






#6
'''
func input img, bg, tlx, tly
output img on bg with tl on (tlx, tly)
raise RuntimeError if exceed boundary'''

def stitch_img_top_left(image,bg,tlx,tly):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")

        if isinstance(bg,str):
                bg=Image.open(bg)
        else:
                if not isinstance(bg,Image.Image):
                        raise TypeError("background image file must be in right type")

        if not isinstance(tlx,int):
                raise ValueError ("top left x coordinate should be an int")
        if not isinstance(tly,int):
                raise ValueError ("top left y coordinate should be an int")

        size_img=width,height=image.size
        size_bg= width_bg,height_bg=bg.size
        if tlx+width > width_bg:
                raise RuntimeError ("boundary out of range")
        if tly+height > height_bg:
                raise RuntimeError ("boundary out of range")

        box1=(0,0,width,height)
        region=image.crop(box1)
        box2=(tlx,tly,tlx+width,tly+height)
        bg.paste(region,box2)
        return bg


#7
'''
func input img, bg
output img on random loc on bg, tlx, tly (make sure not exceeding boundary)'''
def stitch_img_random(image,bg):
        if isinstance(image,str):
                image=Image.open(image)
        else:
                if not isinstance(image,Image.Image):
                        raise TypeError("image file must be in right type")

        if isinstance(bg,str):
                bg=Image.open(bg)
        else:
                if not isinstance(bg,Image.Image):
                        raise TypeError("background image file must be in right type")


        size_img=width,height=image.size
        size_bg= width_bg,height_bg=bg.size
        x_range=abs(width_bg-width)
        y_range=abs(height_bg-height)
        numx_random=random.randint(0,x_range)
        numy_random=random.randint(0,y_range)

        box1=(0,0,width,height)
        region=image.crop(box1)
        width,height=region.size
        while numx_random+width>width_bg or numy_random+height>height_bg:
                width=int(width/2)
                height=int(height/2)
                if width<=0 or height<=0:
                        return stitch_img_random(image,bg)
                region=region.resize((width,height))
        box2=(numx_random,numy_random,numx_random+width,numy_random+height)
        return_box=(numx_random,numx_random+width,numy_random,numy_random+height)
        bg.paste(region,box2)
        return (bg,return_box)
        
                                 