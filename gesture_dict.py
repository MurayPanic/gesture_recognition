import os
import cv2
import importlib

class gesture_dict(object):

    def __init__(self, path='.\gesture_database', shape_descriptor ="ShapeDescriptor_hu"):
        self.data = self.load_contour(path)
        self.shape_descriptor = importlib.import_module(shape_descriptor)
        self.feature_dict = self.gen_dict()
        

    def load_contour(self, path):
        print("Now Load the gesture database")
        current_dir = os.curdir
        data_dir='.\gesture_database'
        os.chdir(data_dir)
        file_list = os.listdir()
        print("%d gesture templates are loaded"  %( len(file_list) ))
        con_dict={}
        for file_name in file_list:
              temp = cv2.imread(file_name)
              temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
              ret, thresh = cv2.threshold(temp_gray, 127, 255, 0)
              binary, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
              dict_key = file_name.split('_')[0]
              con_dict[dict_key]= contours

        os.chdir(current_dir)
        

        return con_dict

    def gen_dict(self):
        print("Now Calculate features of the shape templates")

        feature_dict = {}
        for key in self.data.keys():
            temp_feature = self.shape_descriptor.gen_feature_object(self.data[key])
            feature_dict[key] = temp_feature

        print("Calculation Complete")


        return feature_dict

    
        
        
                



    
        



