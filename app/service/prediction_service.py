from app.service.load import init_color_ref, init_shape_ref, init_text_ref


class PredictionService:
    def __init__(self):
        ''' only initialized with 'front' property
        initializes 4 references
        - color_ref
        - shape_ref
        - divider_ref
        - text_ref
        get data from csv file
        '''
        self.color_ref = init_color_ref()
        self.shape_ref = init_shape_ref()
        self.text_ref = init_text_ref()
    

    def get_converted_img(self, img):
        '''convert input image to Canny, ... 

        Args:
            - img: input image from client
        
        Returns:
            - numpy.ndarray: the result of image with binary data
        '''

        pass
    
    def get_color_group(self, img):
        '''
        Place Jungin's code here
        '''
        pass

    
    def get_shape(self, img):
        '''
        Place Jungin's code here
        '''
        pass
    
    def get_divider(self, img):
        '''
        Place Jungin's code here
        '''
        pass
