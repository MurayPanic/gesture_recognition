import cv2


def gen_feature_object(contour):
    return hu_moment(contour)


class hu_moment(object):
    def __init__(self, contour):
        self.con = contour
        self.feature = self.cal_feature(contour)

    def cal_feature(self, contour):
        feature = cv2.HuMoments(contour)
        return feature

    def match_two_contour(self, con_2):

        score = cv2.matchShapes(self.con[0], con_2,1,0.0)

        return score
            
        
