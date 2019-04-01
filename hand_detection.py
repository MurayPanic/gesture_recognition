import cv2
import numpy as np

class hand_tracker(object):
    def __init__(self, skin_detector ="CrCb"):
        self.hand_box = None
        self.skin_detector_type = skin_detector
        self.hand_contour = None
        


    def cal_hand_box(self, face_box_coor, x_shift_coef =0.0, y_shift_coef=1.6, scale = 2.0):
        x1, y1, x2, y2 = face_box_coor
        
        x_center = int(0.5 * (x2 + x1))
        y_center = int(0.5 * (y2 + y1))
        
        face_box_width = x2 - x1
        face_box_height = y2 - y1
        x_shift = int(x_shift_coef * face_box_width)
        y_shift = int(y_shift_coef * face_box_height)
        x1_hand_box = x_center + x_shift - int(0.5 * scale * face_box_width)
        x2_hand_box = x_center + x_shift + int(0.5 * scale * face_box_width)
        y1_hand_box = y_center + y_shift - int(0.5 * scale * face_box_height)
        y2_hand_box = y_center + y_shift + int(0.5 * scale * face_box_height)

        self.hand_box = (x1_hand_box, y1_hand_box, x2_hand_box, y2_hand_box)

        return (x1_hand_box, y1_hand_box, x2_hand_box, y2_hand_box)

    def draw_hand_box(self,frame):
        if self.hand_box != None:
            x1, y1, x2, y2 = self.hand_box
            cv2.rectangle( frame, (x1,y1), (x2, y2), (255,0,255), 2)

    def draw_hand_con(self, frame):
        

        if self.hand_contour == None: return
        i =0
        for con in self.hand_contour:
            i+=1
            x,y,w,h = cv2.boundingRect(con)
            cv2.rectangle(frame,(x,y),(x+w, y+h), (255, 100,100), 2)
        cv2.drawContours(frame, self.hand_contour, -1,(0,255,0), 3)
        #print('%s contours are draw'%(i))


    def detect_hand_contour(self, frame):
        skin_mask = self.skin_filter(frame)
        binary, contours, hierarchy = cv2.findContours(skin_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.hand_contour = contours
        



    def skin_filter(self, frame):
        x1, y1, x2, y2 = self.hand_box
        img = np.zeros(frame.shape, dtype = np.uint8)
        img_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype= np.uint8)
        img_mask[ y1:y2, x1:x2]=255
        cv2.add(frame, img, img, mask = img_mask)
        if self.skin_detector_type =="CrCb":
            result = self.skin_detector_CrCb(img)
        elif self.skin_detector_type =="HSV":
            result = self.skin_detector_HSV(img)

        return result

    def skin_detector_CrCb(self, img):
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        channels = cv2.split(img_ycrcb)
        cr = channels[1]
        cb = channels[2]
        range_cr = cv2.inRange(cr,133,173)
        range_cb = cv2.inRange(cb,77,127)
        output_mask = cv2.bitwise_and(range_cr,range_cb)
        output_mask = self.mask_smooth(output_mask)
        
        return output_mask

           

    def skin_detector_HSV(self, img):
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_lower = np.array([0,48,80], dtype = np.uint8)
        hsv_upper = np.array([20,255,255], dtype = np.uint8)
        output_mask = cv2.inRange(img_HSV, hsv_lower, hsv_upper)
        output_mask = self.mask_smooth(output_mask)
        
        return output_mask

    def mask_smooth(self, mask):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3) )
        output_mask = cv2.erode(mask, kernel, iterations = 2 )
        output_mask = cv2.dilate(output_mask, kernel, iterations = 2)
        output_mask = cv2.GaussianBlur(output_mask,(3,3),0)

        return output_mask

    

    

    
        
        
        
        
