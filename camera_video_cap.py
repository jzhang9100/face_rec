import cv2

class vid_app:
    def __init__(self, dir):
        #4byte code to specify video codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        self.dir = dir #dir where videos will be saved
        self.out = cv2.VideoWriter(self.dir + 'output.avi', fourcc, 20.0, (640,480))#vid reorder
        self.vidCap = cv2.VideoCapture(0)#video capturer

    def recordVid(self):
        #create window to record face
        cv2.namedWindow("Face")
        if self.vidCap.isOpened():  # try to get the first frame
            rval, frame = self.vidCap.read()
            while rval:
                cv2.imshow("Face", frame)
                rval, frame = self.vidCap.read()
                f = cv2.flip(frame, 0)
                self.out.write(f)
                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    break
            cv2.destroyWindow("Face")

