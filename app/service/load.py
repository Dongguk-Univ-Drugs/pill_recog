import csv
import os


class Reference:
    """get all reference from this class
    
    the main csv file is not included yet - 10.18
    """
    def __init__(self):
        """the initialization of all three references
        
        all of these references are made up from the front data back data is not included !
        
        - color, shape, text
        """
        self.dataset = f'{os.getcwd()}/dataset'
        self.color = self.init_color_ref()
        self.shape = self.init_shape_ref()
        self.text = self.init_text_ref()

    def init_color_ref(self):
        '''initializes the color reference what will be used via `self`
                - keys are named for the groups in numbers
                - values are made up of `set()`s
            ---
            Returns:
                dict:

                1: yellownary set ⇒ [[0, 60, 80], [45, 255, 255]]
                2: grennary set ⇒ [[45, 15, 10], [80, 255, 255]]
                3: bluenary set ⇒ [[90, 60, 70], [115, 255, 255]]
                4: blacknary set ⇒ [[0, 0, 0], [180, 255, 40]]
                5: whitenary set ⇒ [[0, 0, 0], [180, 15, 255]]
            '''
        yellownary = set()
        greenary = set()
        bluenary = set()
        blacknary = set()
        whitenary = set()

        define_yellow = ['노랑', '분홍', '주황', '갈색', '빨강']
        define_green = ['연두', '초록']
        define_blue = ['보라', '파랑', '자주']
        define_black = ['검정', '회색']
        define_white = ['하양']

        # read file
        with open(os.path.join(self.dataset, 'color_reference.csv'),
                  newline='',
                  encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
            # distribute into groups
            for line in lines[1:]:
                pid, color = line[0], line[1]
                if color in define_yellow: yellownary.add(pid)
                elif color in define_green: greenary.add(pid)
                elif color in define_blue: bluenary.add(pid)
                elif color in define_black: blacknary.add(pid)
                elif color in define_white: whitenary.add(pid)

        return {
            1: yellownary,
            2: greenary,
            3: bluenary,
            4: blacknary,
            5: whitenary
        }

    def init_shape_ref(self):
        '''initializes the shape reference what will be used via `self`
                - keys are named of up [ cirlce, oval, triangle, square, rhombus, pentagon, hexagon, octagon, stadium, semicircle ] 
                - values are `set()`s of each key
            ---
            Returns:

                dict: `{ 'circle': set(), 'oval', set(), ... , 'semicircle': set() }`
            '''
        circle = set()
        oval = set()
        triangle = set()
        square = set()
        rhombus = set()
        pentagon = set()
        hexagon = set()
        octagon = set()
        stadium = set()
        semicircle = set()

        # read file
        with open(os.path.join(self.dataset, 'shape_reference.csv'),
                  newline='',
                  encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
            # distribute items
            for line in lines:
                pid, shape = line[0], line[1]
                if shape == '원형': circle.add(pid)
                elif shape == '타원형': oval.add(pid)
                elif shape == '삼각형': triangle.add(pid)
                elif shape == '사각형': square.add(pid)
                elif shape == '마름모형': rhombus.add(pid)
                elif shape == '오각형': pentagon.add(pid)
                elif shape == '육각형': hexagon.add(pid)
                elif shape == '팔각형': octagon.add(pid)
                elif shape == '장방형': stadium.add(pid)
                elif shape == '반원형': semicircle.add(pid)

        return {
            'circle': circle,
            'oval': oval,
            'triangle': triangle,
            'square': square,
            'rhombus': rhombus,
            'pentagon': pentagon,
            'hexagon': hexagon,
            'octagon': octagon,
            'stadium': stadium,
            'semicircle': semicircle
        }

    def init_text_ref(self) -> dict:
        '''initializes the text reference what will be used via `self`

            ---
            Returns:
                dict: the keys are front_text and the values are made up of its pid
                
                ex) dict['CZT'] = ['199703153', ... ]
            '''
        # saves the front text for key and pid for value
        result_dict = {}
        # read file
        with open(os.path.join(self.dataset, 'text_reference.csv'),
                  newline='',
                  encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
            # make it into dict
            for line in lines:
                pid, front_text = line[0], line[1]
                front_text = front_text.replace('마크', '').replace('분할선',
                                                                  '').upper()
                # the front_text cannot be in dict
                if front_text not in result_dict:
                    result_dict[front_text] = set()
                result_dict[front_text].add(pid)

        return result_dict
