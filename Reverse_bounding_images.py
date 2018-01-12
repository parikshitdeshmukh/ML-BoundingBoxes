from PIL import Image
import glob
import numpy as np
import pandas as pd

import os
import lxml.etree
import lxml.builder
import xml.etree.ElementTree as ET
##b'\xE2\x82\xAC'.decode('UTF-8')

def parseImageAndFiles(path):
    imList = []
    bigDict = {}
    s = np.empty(0,dtype=[('width', 'i8'), ('height', 'i8'), ('name', 'S20')])
    for filename in glob.glob(path+'*33.jpg'):  # assuming gif
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


def reverse_bound(bigDict, filepath):
    # E = lxml.builder.ElementMaker()
    # annotation = E.annotation
    # folder = E.folder
    # filename = E.filename
    # path = E.path
    # source = E.source
    # database = E.database
    # size = E.size
    # width = E.width
    # height = E.height
    # object = e.object
    # name = E.name
    # pose = E.pose
    # truncated = E.truncated
    # difficult = E. difficult
    # bndbox = E.bndbox
    # xmin = E.xmin
    # ymin = E.ymin
    # xmax = E.xmax
    # ymax = E.ymax
    for key, value in bigDict.items():
        fname= key;
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
        m=0
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
            xmax = ET.SubElement(bndbox, 'xmax')
            temp = np.array(value[1])
            xmax.text = str((2*temp[m][0]*w + temp[m][2]*w)/2)
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str((2*temp[m][1]*h + temp[m][3]*h)/2)
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str((2*temp[m][0]*w + temp[m][2]*w)/2 - temp[m][2]*w )
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = str((2*temp[m][0]*w + temp[m][2]*w)/2 - temp[m][3]*h )

        mydata = ET.tostring(annotation)
        mydata = mydata.decode('UTF-8')
        myfile = open('/media/parik/New Volume/PractiseProbems/ESSI/NFPA_dataset/xmls/'+os.path.splitext(os.path.basename(fname))[0]+'.xml', "w+")
        myfile.write(mydata)
        myfile.close()




        # the_doc = annotation(
        #     folder('NFPA dataset'),
        #     filename(fname),
        #     path(filepath + fname),
        #     source(
        #         database('Unknown')
        #     ),
        #     size(
        #         width(w),
        #         height(h)
        #     ),
        #     for i in range(value[1].size):
        #         object(
        #             name('nfpa'),
        #             pose('Unspecified'),
        #             truncated('0'),
        #             difficult('0'),
        #             bndbox(
        #                 xmax('(2*value[1][i][0]*w + value[1][i][2]*w)/2'),
        #                 ymax('(2*value[1][i][1]*h + value[1][i][3]*h)/2'),
        #                 xmin('2*value[1][i][0]*w -(2*value[1][i][0]*w + value[1][i][2]*w)/2' ),
        #                 ymin('2*value[1][i][1]*h - (2*value[1][i][0]*w + value[1][i][2]*w)/2')
        #             )
        #         ),
        #
        #
        # )

bigD = parseImageAndFiles('/media/parik/New Volume/PractiseProbems/ESSI/NFPA_dataset/')

print(bigD)

reverse_bound(bigD,'/media/parik/New Volume/PractiseProbems/ESSI/NFPA_dataset/' )

print("Success")