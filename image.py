import os
import cv2
import numpy as np
from utils import get_file_name
import xml.etree.ElementTree as ET


def process_image(file_path, output_path, x, y, save_box_images):
    (base_dir, file_name) = get_file_name(file_path)
    try:

        jpg = '{}/{}.jpg'.format(base_dir, file_name)
        xml = '{}/{}.xml'.format(base_dir, file_name)

        resize(
            jpg,
            xml,
            (x, y),
            output_path,
            save_box_images=save_box_images,
        )
    except Exception as e:
        print('[ERROR] error with {}\n file: {}'.format(jpg, e))
        print('--------------------------------------------------')


def draw_box(boxes, image, path):
    for i in range(0, len(boxes)):
        cv2.rectangle(image, (boxes[i][2], boxes[i][3]), (boxes[i][4], boxes[i][5]), (255, 0, 0), 1)
    cv2.imwrite(path, image)


def resize(image_path,
           xml_path,
           newSize,
           output_path,
           save_box_images=False,
           verbose=False):

    image = cv2.imread(image_path)

    scale_x = newSize[0] / image.shape[1]
    scale_y = newSize[1] / image.shape[0]

    image = cv2.resize(image, (newSize[0], newSize[1]))

    newBoxes = []
    xmlRoot = ET.parse(xml_path).getroot()
    for member in xmlRoot.findall('object'):
        bndbox = member.find('bndbox')

        xmin = bndbox.find('xmin')
        ymin = bndbox.find('ymin')
        xmax = bndbox.find('xmax')
        ymax = bndbox.find('ymax')

        xmin.text = str(np.round(int(xmin.text) * scale_x))
        ymin.text = str(np.round(int(ymin.text) * scale_y))
        xmax.text = str(np.round(int(xmax.text) * scale_x))
        ymax.text = str(np.round(int(ymax.text) * scale_y))

        newBoxes.append([
            1,
            0,
            int(float(xmin.text)),
            int(float(ymin.text)),
            int(float(xmax.text)),
            int(float(ymax.text))
            ])

    (_, file_name) = get_file_name(image_path)
    cv2.imwrite(os.path.join(output_path, '_new'.join([file_name, '.jpg'])), image)

    tree = ET.ElementTree(xmlRoot)
    tree.write('{}/{}_new.xml'.format(output_path, file_name.split('.')[0]))
    if int(save_box_images):
        save_path = '{}/boxes_images/boxed_{}'.format(output_path, ''.join([file_name, '.jpg']))
        draw_box(newBoxes, image, save_path)
