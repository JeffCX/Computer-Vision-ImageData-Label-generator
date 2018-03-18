import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from lxml import etree
import xml.etree.cElementTree as ET

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
    for obj, topl, botr in zip(objects, tl, br):
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = obj
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(topl[0])
        ET.SubElement(bbox, 'ymin').text = str(topl[1])
        ET.SubElement(bbox, 'xmax').text = str(botr[0])
        ET.SubElement(bbox, 'ymax').text = str(botr[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    # randomly jb gai
    save_path = os.path.join(savedir, img.name.replace('png', 'xml'))
    save_path = save_path.split(".")
    save_path[-1]="xml"
    save_path = ".".join(save_path)
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)

# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants
image_folder = 'images'
savedir = 'annotations'
obj = 'fidget_spinner'


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.xdata)))
    br_list.append((int(rls.xdata), int(rls.xdata)))
    object_list.append(obj)


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'q':
        savedir = "annotations"
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

if __name__ == '__main__':
    lst = os.scandir(image_folder)
    for image_file in lst:
        try:
            img = image_file
            fig, ax = plt.subplots(1, figsize=(10.5, 8))
            mngr = plt.get_current_fig_manager().canvas
            #mngr.window.setGeometry(250, 40, 800, 600)
            image = cv2.imread(image_file.path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ax.imshow(image)

            toggle_selector.RS = RectangleSelector(
                ax, line_select_callback,
                drawtype='box', useblit=True,
                button=[1], minspanx=5, minspany=5,
                spancoords='pixels', interactive=True,
            )
            bbox = plt.connect('key_press_event', toggle_selector)
            key = plt.connect('key_press_event', onkeypress)
            plt.tight_layout()
            plt.show()
            plt.close(fig)
        except:
            pass