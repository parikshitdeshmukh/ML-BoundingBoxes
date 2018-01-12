from PIL import Image
import glob
import numpy as np
import pandas as pd
import cv2
import math
import os
import xml.etree.ElementTree as ET
from decimal import *
##b'\xE2\x82\xAC'.decode('UTF-8')

def parseImageAndFiles(path):
    print("Parsing Images for dimensions and corresponding text files for collecting the Bounding Boxes data")
    bigDict = {}
    s = np.empty(0,dtype=[('width', 'i8'), ('height', 'i8'), ('name', 'S20')])
    for filename in glob.glob(path+'*.jpg'):
        for fileTxt in glob.glob(path+'*.txt'):
            s = np.empty(0, dtype=[('width', 'i8'), ('height', 'i8'), ('name', 'S20')])
            if os.path.splitext(os.path.basename(filename))[0]== os.path.splitext(os.path.basename(fileTxt))[0]:
                im = Image.open(filename)
                s = np.append(s, np.array([(im.size[0], im.size[1], os.path.splitext(os.path.basename(filename))[0])], dtype=s.dtype))
                if os.stat(fileTxt).st_size !=0:
                    data = pd.read_csv(fileTxt, sep=" ", usecols=(1,2,3,4), header = None)
                else: data = pd.DataFrame(np.zeros((1, 4)))
                bigDict[os.path.basename(filename)] = [s, data]
                break;
    return bigDict



#Sample Output XML:
#
# <annotation>
# 	<folder>NFPA dataset</folder>
# 	<filename>pos-33.jpg</filename>
# 	<path>C:/Users/admin/Desktop/NFPA dataset/pos-33.jpg</path>
# 	<source>
# 		<database>Unknown</database>
# 	</source>
# 	<size>
# 		<width>800</width>
# 		<height>640</height>
# 		<depth>3</depth>
# 	</size>
# 	<object>
# 		<name>nfpa</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>54</xmin>
# 			<ymin>206</ymin>
# 			<xmax>464</xmax>
# 			<ymax>608</ymax>
# 		</bndbox>
# 	</object>
# 	<object>
# 		<name>nfpa</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>408</xmin>
# 			<ymin>211</ymin>
# 			<xmax>747</xmax>
# 			<ymax>548</ymax>
# 		</bndbox>
# 	</object>
# </annotation>
#


def reverse_bound(bigDict, filepath, l):
    print("Using parsed data to generate XMLs and modifying images with the bounding boxes")
    print("Genrated XML files will be stored in OutputLabels and Images inside OutputImages folder both residing in NFPA_Dataset folder")
    outLabel= filepath +'OutputLabels'
    outImages = filepath + 'OutputImages'
    if not os.path.exists(outLabel):
        os.makedirs(outLabel)
    if not os.path.exists(outImages):
        os.makedirs(outImages)
    for key, value in bigDict.items():
        fname= key;
        img = cv2.imread(filepath+fname, cv2.IMREAD_COLOR)
        w = value[0][0][0]
        h = value[0][0][1]

        annotation = ET.Element('annotation')
        folder = ET.SubElement(annotation, 'folder')
        folder.text = 'NFPA dataset'
        filename = ET.SubElement(annotation, 'filename')
        filename.text = fname
        path = ET.SubElement(annotation, 'path')
        path.text = filepath + fname
        source = ET.SubElement(annotation, 'source')
        database = ET.SubElement(source, 'database')
        database.text = 'Unknown'
        size = ET.SubElement(annotation, 'size')
        width = ET.SubElement(size, 'width')
        width.text = str(w)
        height = ET.SubElement(size, 'height')
        height.text = str(h)
        temp = np.array(value[1])
        for m in range(value[1].shape[0]):
            object = ET.SubElement(annotation, 'object')
            name = ET.SubElement(object, 'name')
            name.text = 'nfpa'
            pose = ET.SubElement(object, 'pose')
            pose.text = 'Unspecified'
            truncated = ET.SubElement(object, 'truncated')
            truncated.text = '0'
            difficult = ET.SubElement(object, 'difficult')
            difficult.text = '0'
            bndbox = ET.SubElement(object, 'bndbox')
            # xmin = ET.SubElement(bndbox, 'xmin')
            # _xmin = math.ceil((w * (2 * temp[m][0] + temp[m][2]) / 2) - temp[m][2] * w)
            # xmin.text = str(_xmin)
            # ymin = ET.SubElement(bndbox, 'ymin')
            # _ymin = math.ceil((h * (2 * temp[m][1] + temp[m][3]) / 2) - temp[m][3] * h)
            # ymin.text = str(_ymin)
            # xmax = ET.SubElement(bndbox, 'xmax')
            # _xmax = math.ceil(w*(2*temp[m][0] + temp[m][2])/2)
            # xmax.text = str(_xmax)
            # ymax = ET.SubElement(bndbox, 'ymax')
            # _ymax = math.ceil(h*(2*temp[m][1]+ temp[m][3])/2)
            # ymax.text = str(_ymax)

            xmin = ET.SubElement(bndbox, 'xmin')
            _xmin = Decimal.from_float(w * (2 * temp[m][0] + temp[m][2]) / 2.0 - temp[m][2] * w)
            xmin.text = str(math.ceil(_xmin))
            ymin = ET.SubElement(bndbox, 'ymin')
            _ymin = Decimal.from_float(h * (2 * temp[m][1] + temp[m][3]) / 2.0 - temp[m][3] * h)
            ymin.text = str(math.ceil(_ymin))
            xmax = ET.SubElement(bndbox, 'xmax')
            _xmax = Decimal.from_float(w * (2 * temp[m][0] + temp[m][2]) / 2.0)
            xmax.text = str(math.ceil(_xmax))
            ymax = ET.SubElement(bndbox, 'ymax')
            _ymax = Decimal.from_float(h * (2 * temp[m][1] + temp[m][3]) / 2.0)
            ymax.text = str(math.ceil(_ymax))
            img = cv2.rectangle(img, (math.ceil(_xmin), math.ceil(_ymax)), (math.ceil(_xmax), math.ceil(_ymin)), l, 4 )
        mydata = ET.tostring(annotation)
        mydata = mydata.decode('UTF-8')
        myfile = open(outLabel+'/'+ os.path.splitext(os.path.basename(fname))[0]+'.xml', "w+")
        myfile.write(mydata)
        myfile.close()
        cv2.imwrite(outImages+'/'+ os.path.splitext(os.path.basename(fname))[0]+'.jpg', img)
