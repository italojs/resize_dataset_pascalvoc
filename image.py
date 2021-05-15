import os
import cv2
import numpy as np
from utils import get_file_name
import xml.etree.ElementTree as ET
from math import floor


def process_image(file_path, output_path, x, y, save_box_images, ratio):
    (base_dir, file_name, ext) = get_file_name(file_path)
    image_path = '{}/{}.{}'.format(base_dir, file_name, ext)
    xml = '{}/{}.xml'.format(base_dir, file_name)
    try:
        resize(
            image_path,
            xml,
            (x, y),
            output_path,
            ratio,
            save_box_images=save_box_images
        )
    except Exception as e:
        print('[ERROR] error with {}\n file: {}'.format(image_path, e))
        print('--------------------------------------------------')


def draw_box(boxes, image, path):
    for i in range(0, len(boxes)):
        cv2.rectangle(image, (boxes[i][2], boxes[i][3]), (boxes[i][4], boxes[i][5]), (255, 0, 0), 1)
    cv2.imwrite(path, image)


def resize(image_path,
           xml_path,
           newSize,
           output_path,
           ratio,
           save_box_images=False,
           verbose=False
           ):

    image = cv2.imread(image_path)

    if ratio is None:
        scale_x = newSize[0] / image.shape[1]
        scale_y = newSize[1] / image.shape[0]
    
    else:
        newSize[0] = floor(image.shape[1] * newSize[0])
        newSize[1] = floor(image.shape[0] * newSize[0])
        scale_x = newSize[0] / image.shape[1]
        scale_y = newSize[1] / image.shape[0]

    image = cv2.resize(image, (newSize[0], newSize[1]))

    newBoxes = []
    xmlRoot = ET.parse(xml_path).getroot()
    xmlRoot.find('filename').text = image_path.split('/')[-1]
    size_node = xmlRoot.find('size')
    size_node.find('width').text = str(newSize[0])
    size_node.find('height').text = str(newSize[1])

    for member in xmlRoot.findall('object'):
        bndbox = member.find('bndbox')

        xmin = bndbox.find('xmin')
        ymin = bndbox.find('ymin')
        xmax = bndbox.find('xmax')
        ymax = bndbox.find('ymax')
        
        xmin.text = str(int(np.round(float(xmin.text) * scale_x)))
        ymin.text = str(int(np.round(float(ymin.text) * scale_y)))
        xmax.text = str(int(np.round(float(xmax.text) * scale_x)))
        ymax.text = str(int(np.round(float(ymax.text) * scale_y)))

        newBoxes.append([
            1,
            0,
            int(float(xmin.text)),
            int(float(ymin.text)),
            int(float(xmax.text)),
            int(float(ymax.text))
            ])

    (_, file_name, ext) = get_file_name(image_path)
    cv2.imwrite(os.path.join(output_path, '.'.join([file_name, ext])), image)

    tree = ET.ElementTree(xmlRoot)
    tree.write('{}/{}.xml'.format(output_path, file_name, ext))
    if int(save_box_images):
        save_path = '{}/boxes_images/boxed_{}'.format(output_path, ''.join([file_name, '.', ext]))
        draw_box(newBoxes, image, save_path)
