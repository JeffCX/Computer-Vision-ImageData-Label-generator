from __future__ import division
from PIL import Image
import random
from image_processing_helper import stitch_img_random #import helper function
import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from lxml import etree
import xml.etree.cElementTree as ET
import re

def write_xml(folder, img, objects, tl, br, savedir):
    if not os.path.isdir(savedir):
        os.system("mkdir %s"%savedir)
    image = cv2.imread(img.path)
    height, width, depth = image.shape
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = img.name
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    obj = objects[0]
   
    ob = ET.SubElement(annotation, 'object')
    ET.SubElement(ob, 'name').text = obj
    ET.SubElement(ob, 'pose').text = 'Unspecified'
    ET.SubElement(ob, 'truncated').text = '0'
    ET.SubElement(ob, 'difficult').text = '0'
    bbox = ET.SubElement(ob, 'bndbox')
    ET.SubElement(bbox, 'xmin').text = str(tl[0])
    ET.SubElement(bbox, 'ymin').text = str(tl[1])
    ET.SubElement(bbox, 'xmax').text = str(br[0])
    ET.SubElement(bbox, 'ymax').text = str(br[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    # randomly jb gai
    save_path = os.path.join(savedir, img.name.replace('png', 'xml'))
    print(save_path)
    save_path = save_path.split(".")
    save_path[-1]="xml"
    save_path = ".".join(save_path)
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)

img = None
tl_list = []
br_list = []
object_list = []

# constants
image_folder_fore = 'image_fore'
image_folder_bg = "image_bg"
data = "images" 
savedir = 'annotations'
obj = 'cellar' #what is the object

if not os.path.isdir(image_folder_fore):
	raise ValueError ("positive images should be put into %s folder"%image_folder_fore)

if not os.path.isdir(image_folder_bg):
	raise ValueError ("positive images should be put into %s folder"%image_folder_bg)

if not os.path.isdir(data):
	os.system("mkdir images")

if not os.path.isdir(savedir):
	os.system("mkdir annotations")

name = 0
list_img_fore = os.listdir(image_folder_fore)
list_img_bg = os.listdir(image_folder_bg)
for i in list_img_fore:
	if ".jpg" in i:
		for j in list_img_bg:
			if ".jpg" in j:
				f = image_folder_fore + "/" + i
				b = image_folder_bg + "/" + j
				img,labels = stitch_img_random(f,b)
				img = img.convert("RGB")
				save_path_img = "images/" + str(name) 
				img.save(save_path_img +".jpg",mode="RGBA")
				x1,x2,y1,y2 = labels
				txt_file  = open(save_path_img+".txt","w")
				txt_file.write(str((x1,x2,y1,y2))+ " "+obj)
				txt_file.close()
				name+=1
				
lst = os.scandir(data)
for image_file in lst:
    try:
        img = image_file
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        txt_path = re.findall("[0-9]+",image_file.path)[0]     
        txt_path = "images/" + str(txt_path) +".txt"   
        txt_path = open(txt_path,"r")
        txt_path = re.sub("[(),]"," ",txt_path.read()).split()
        x1,x2,y1,y2,obj = txt_path
        object_list.append(obj)
        write_xml(data, img, object_list,[x1,y1], [x2,y2], savedir)
        object_list = []
    except:
        pass






