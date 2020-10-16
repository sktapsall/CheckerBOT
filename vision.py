import cv2
# cap = cv2.VideoCapture(0)
import numpy as np
class VisionEngine:
    def __init__(self,highlight=True):
        self.cap = cv2.VideoCapture(0)


    def detect_pieces(self, img):
        pass

    @staticmethod
    def find_outermost_corners(corners):
        topleft = corners[0]
        topright = corners[6]
        bottomright = corners[6*7+6]
        bottomleft = corners[6*7]
        topleftx = (topleft-topright)*1/6+(topleft-bottomleft)*1/6+topleft
        toprightx = (topright-topleft)*1/6+(topright-bottomright)*1/6+topright
        bottomleftx = (bottomleft-bottomright)*1/6+(bottomleft-topleft)*1/6+bottomleft
        bottomrightx = (bottomright-bottomleft)*1/6+(bottomright-topright)*1/6+bottomright
        outermost = np.array([topleftx,toprightx,bottomrightx, bottomleftx],dtype=np.int32)
        return outermost

    @staticmethod
    def homographied(img, corners):
        pass
    

    def main_loop(self, callback):
        while True:
            ret, frame = self.cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            retvals, corners = cv2.findChessboardCorners(gray, (7,7))
            # Display the resulting frame
            print(corners)
            if corners is not None:
                for board in corners:
                    outermost = self.find_outermost_corners(corners)
                    cv2.fillPoly(frame, pts=[outermost], color=(0,0,255))
                    for corner in board:
                        frame[round(corner[1]-1), round(corner[0])] =  (0,255,255)
                        frame[round(corner[1]+1), round(corner[0])] =  (0,255,255)
                        frame[round(corner[1]+1), round(corner[0])-1] =  (0,255,255)
                        frame[round(corner[1]-1), round(corner[0])-1] =  (0,255,255)
                        frame[round(corner[1]-1), round(corner[0])+1] =  (0,255,255)
                        frame[round(corner[1]+1), round(corner[0])+1] =  (0,255,255)
                        frame[round(corner[1]), round(corner[0])] = (0,255,255)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

a = VisionEngine()
a.main_loop(lambda x: x)
# When everything done, release the capture
