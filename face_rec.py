import cv2
import numpy as np


class face_fun:
    def __init__(self, dir):
        self.dir = dir  # dir where videos will be saved
        self.vidCap = cv2.VideoCapture(0)  # video capturer

    def get_face_data(self):
        #gathers face imgs from computer camera
        i = 0
        if self.vidCap.isOpened():  # try to get the first frame
            retval, frame = self.vidCap.read()
            while retval:
                cv2.imshow("Gather Facial Images", frame)
                retval, frame = self.vidCap.read()
                if (i % 2 == 0):
                    cv2.imwrite(self.dir + 'my_face' + str(i // 2) + '.jpg', frame)
                i += 1

                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    break
            self.vidCap.release()
            cv2.destroyAllWindows()


    def detect_face(self):
        # create window and puts box arond face
        cv2.namedWindow("Found yo Face")
        i = 0
        if self.vidCap.isOpened():  # try to get the first frame
            retval, frame = self.vidCap.read()
            while retval:
                frame, kps = self.process_frame(frame)
                frame = cv2.drawKeypoints(frame,kps, None, color=(0,255,0), flags=0)
                cv2.imshow("Found yo Face", frame)
                retval, frame = self.vidCap.read()
                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    break
            self.vidCap.release()
            cv2.destroyAllWindows()

    def process_frame(self, img):
        #use openCv's Haar-cascade detection
        face_cascade = cv2.CascadeClassifier('D:\\MAS\\Python\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        f = face_cascade.detectMultiScale(gray, 1.3, 5)
        kps = None
        #draw rectangle around detected face
        for (x,y,w,h) in f:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            rect_img = img[x : x+w+1, y : y+h+1]
            kps = self.featuresExtract(img, x, y, h, w)
        if(kps is not None):
            return img, kps
        return img, kps

    def featuresExtract(self, img, x, y, h ,w):
        orb = cv2.ORB_create()

        #detection of key corners
        points = cv2.goodFeaturesToTrack(np.mean(img, axis=2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance=7)


        key_points = []
        for p in points:
            px = p[0][0]
            py = p[0][1]
            if((px >= x and px <= x+w+1) and (py >= y and py <= y+h+1)):
                k = cv2.KeyPoint(x=px, y=py, _size=20)
                key_points.append(k)
        key_points, des = orb.compute(img, key_points)
        return key_points