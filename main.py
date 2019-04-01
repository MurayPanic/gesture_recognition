import face_detection as fd
import hand_detection as hd
import gesture_dict as gd
import gesture_matcher as gm
import cv2
import threading
import time

threadLock = threading.Lock()

def detection_op(camera,ges_matcher):

    
    global face_detector
    global hand_detector
    while(True):
        ret, frame = camera.read()
        threadLock.acquire()
        
        #print('Detection Runing at', time.ctime(time.time()))

        face_detector.cal_face_box(frame)
        
        hand_detector.cal_hand_box(face_detector.face_box,1.3,0,1.5)

        hand_detector.detect_hand_contour(frame)
        
        
        
        threadLock.release()
        #print(hand_detector.hand_contour)
        
        #threadLock.acquire()
        #ges_matcher.draw_label(frame)
        #threadLock.release()

    


def match_op( ges_matcher):

    global hand_detector
    

    while(True):
        threadLock.acquire()
        contour = hand_detector.hand_contour
        threadLock.release()
        if contour == None :
            pass
        else:
            ges_matcher.match_ges(contour)


    
        
        


    


if __name__ == "__main__":
    face_detector = fd.face_cascade()
    hand_detector = hd.hand_tracker()
    ges_dict = gd.gesture_dict()
    ges_matcher = gm.gesture_matcher(ges_dict)
    
    

    
    
    camera = cv2.VideoCapture(0)
    

    #camera setting
    fps  = camera.get(cv2.CAP_PROP_FPS)
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    demo_name='G:/temp work/GR_with_MultiThread_with_DCP/demo/record_' + time.asctime()[12:20].strip().replace(':','_') + '.avi'
    videoWriter = cv2.VideoWriter(demo_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size,True)
    #print(demo_name)


    #ret, frame = camera.read()
    face_coor = None
    hand_coor = None

    detection_thread= threading.Thread(target = detection_op,  \
                                       args = (camera,ges_dict,)
                                       )
    

    
    match_thread = threading.Thread(target = match_op, \
                                    args   = (ges_matcher,)
                                    )

    
    

    detection_thread.setDaemon(True)
    detection_thread.start()

    
    match_thread.setDaemon(True)
    match_thread.start()

    

    while True:
        ret, frame = camera.read()
        display =frame
        #draw face box
        face_detector.draw_face_box(display)
        #draw hand box
        hand_detector.draw_hand_box(display)
        #draw hand contour
        hand_detector.draw_hand_con(display)
        #draw match gesture label
        ges_matcher.draw_label(display)


        

        videoWriter.write(display)
        cv2.imshow('display', display)
        
        if cv2.waitKey(1) == ord('q'):
            camera.release()
            cv2.destroyAllWindows()

        

    
    

    detection_thread.exit()
    match_thread.exit()

   


        

    

    
    
    
    
    
    
