import cv2



class face_cascade(object):
    def __init__(self):
        print("Now initialize function of face detection with the Cascade Classifier")
        self.detector =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        print("Initialization Complete")
        self.face_box=None

    def detect_face(self, frame):
        #Return the boxes that contain the face
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.2, 5)
        if faces != ():
            for (x,y,w,h) in faces:
                return (x,y,x+w, y+h)
        else:
            return (0,0,0,0)

    def cal_face_box(self, frame):
        self.face_box = self.detect_face(frame)
        
        return self.face_box

    def draw_face_box(self, frame):
        if self.face_box != None:
            x1, y1, x2, y2 = self.face_box
            cv2.rectangle( frame, (x1,y1), (x2, y2), (255,0,0), 2)
        
        


        

    

