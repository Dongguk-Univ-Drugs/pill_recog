import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

""" DRUGES has pid as key
    and value is 
    {'color': ..., 'shape': ..., 'front': ..., 'back': ..., \
     'name': ..., 'manufacturer': ..., 'imageURL': ...}
"""
DRUGS = {}
COLOR_TO_PIDS = {}
# range of color
COLOR_RANGE = {"Red":((0, 60, 80), (45, 255, 255)), \
               "Green":((45, 15, 10), (80, 255, 255)), \
               "Blue": ((90, 60, 70), (115, 255, 255)), \
               "Black": ((0, 0, 0), (180, 255, 40)), \
               "White": ((0, 0, 220), (180, 40, 255))}
SHAPE_TO_PIDS = {}
TEXT_TO_PIDS = {}

with open(os.path.join(BASE_DIR, 'dataset/color_reference.csv'),
                       newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)
    
    define_red = ['노랑', '분홍', '주황', '갈색', '빨강']
    define_green = ['연두', '초록']
    define_blue = ['보라', '파랑', '자주']
    define_black = ['검정', '회색']
    define_white = ['하양']
    rednary = set()
    greenary = set()
    bluenary = set()
    blacknary = set()
    whitenary = set()
    # distribute into groups
    for line in lines[1:]:
        pid, color = line[0], line[1]
        if color in define_red: rednary.add(pid)
        elif color in define_green: greenary.add(pid)
        elif color in define_blue: bluenary.add(pid)
        elif color in define_black: blacknary.add(pid)
        elif color in define_white: whitenary.add(pid)
        DRUGS[pid] = {'color': color}
    COLOR_TO_PIDS.update({'Red': rednary,
                        'Green': greenary,
                        'Blue': bluenary,
                        'Black': blacknary,
                        'White': whitenary})

# read file
with open(os.path.join(BASE_DIR, 'dataset/shape_reference.csv'),
            newline='',
            encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)
    shape_to_eng = {'원형':'circle', '타원형':'oval', '삼각형':'triangle',\
                    '사각형':'square', '마름모형':'rhombus', '오각형':'pentagon', \
                    '육각형':'hexagon', '팔각형':'octagon', '장방형':'stadium', \
                    '반원형':'semicircle'}
    shapes = {}
    list(map(lambda shape: shapes.update({shape:set()}), shape_to_eng.keys()))
    # for shape in shape_to_eng.keys():
    #     shapes[shape] = set()
    # distribute items
    for line in lines:
        pid, shape = line[0], line[1]
        if shape in shapes:
            shapes[shape].add(pid)
            DRUGS[pid]['shape'] = shape_to_eng[shape]

    for shape, pids in shapes.items():
        SHAPE_TO_PIDS[shape_to_eng[shape]] = pids

# 여기는 어떻게 쓸지 잠깐 보류..
# front와 back을 모두 활용해야하는디.:
# read file
with open(os.path.join(BASE_DIR, 'dataset/text_reference.csv'),
          newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)
    # make it into dict
    for line in lines[1:]:
        pid, front_text, back_text = line[0], line[1], line[2]
        # front_text = front_text.replace('마크', '').replace('분할선',
        #                                                     '').upper()
        # the front_text cannot be in dict
        if front_text not in TEXT_TO_PIDS:
            TEXT_TO_PIDS[front_text] = set()
        TEXT_TO_PIDS[front_text].add(pid)

# read file
with open(os.path.join(BASE_DIR, 'dataset/total_reference.csv'),
            newline='',
            encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)
    # put into result_dict
    for pid, name, manufacturer, preview_image in lines[1:]:
        DRUGS[pid]['name']=name
        DRUGS[pid]['manufacturer']=manufacturer
        DRUGS[pid]['imageURL']=preview_image

def get_drugs():
    return DRUGS

def get_drug(pid):
    return DRUGS[pid] if pid in DRUGS else None

def get_color_pids():
    return COLOR_TO_PIDS

def get_color_pid(color):
    return COLOR_TO_PIDS[color] if color in COLOR_TO_PIDS else None

def get_shape_pids():
    return SHAPE_TO_PIDS

def get_shape_pid(shape):
    return SHAPE_TO_PIDS[shape] if shape in SHAPE_TO_PIDS else None

def get_text_pids():
    return TEXT_TO_PIDS

def get_text_pid(text):
    return TEXT_TO_PIDS[text] if text in TEXT_TO_PIDS else None