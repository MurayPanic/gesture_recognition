import cv2
import sys

class gesture_matcher(object):

    def __init__(self, ges_dict):
        self.ges_dict = ges_dict
        self.ready = 'idle'  #True for finished matching,
                            #False for Not finish Or just output a gesture
        
        self.result_list= []


    def match_ges (self, input_con_list):
        self.ready = 'working'
        max_con=None
        max_con_len = 0

        for con in input_con_list:
            if len(con)> max_con_len:
                max_con_len = len(con)
                max_con=con
        
        
        if max_con_len!=0:
            
            best_match = 9999999
            best_key = None
            for key in self.ges_dict.feature_dict:
                #print('Now match the input contour:', key)
                match_score = self.ges_dict.feature_dict[key].match_two_contour( max_con )
                print('The match score is', key, match_score)

                if match_score< best_match:
                    best_match = match_score
                    best_key =key
            print('-'*10)        
            if(best_key !=None ):
                if self.result_list:
                    self.result_list[0]=(best_key, con)
                else:
                    self.result_list.append((best_key, con))

        #if best_key!= None: print('best_key:', best_key)

        self.ready = 'complete'

    def draw_label(self, frame):
        if self.result_list == None:
            return
        for con in self.result_list:
            x,y, w, h = cv2.boundingRect(con[1])
        #cv2.rectangle(img,(x,y),(x+w, y+h), (255, 0,100), 2)
            cv2.putText(frame, con[0],(x,y), cv2.FONT_ITALIC, 1, (255,255,255), thickness=3 )
            

        

        self.ready = 'idle'
        #self.result_list = []
        
