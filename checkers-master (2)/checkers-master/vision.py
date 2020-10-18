import cv2
import numpy as np


class VisionEngine:
    def __init__(self,highlight=True):
        self.cap = cv2.VideoCapture(0)

        # Homography points for checkerboard
        ref = cv2.imread('checkerboard.jpg');
        gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        retvals, refcorners = cv2.findChessboardCorners(gray, (7,7))
        self.refoutermost = VisionEngine.find_outermost_corners(refcorners)

    @staticmethod
    def detect_pieces(img):
        red  = np.array([[0,130,115],[20,255,255]])
        blue = np.array([[100,200,80], [230,255,255]])
        imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        redmask = cv2.inRange(imghsv, red[0], red[1])
        bluemask = cv2.inRange(imghsv, blue[0], blue[1])
        bluemask = cv2.morphologyEx(bluemask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        redmask = cv2.morphologyEx(redmask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        bluemask = cv2.morphologyEx(bluemask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
        redmask = cv2.morphologyEx(redmask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
        return bluemask, redmask
        
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

    # Transform and center image
    def homographied(self, img, corners):
        w, h = img.shape[:2]
        points = np.array([[0, 0], [0, w], [h, w], [h, w]])
        h, status = cv2.findHomography(corners, self.refoutermost)
        point_top = np.array([[[0., 0.]]])
        dst = np.array([[[0.,0.]]])
        newpnt = cv2.perspectiveTransform(point_top, h)
        new = cv2.warpPerspective(img, h, (round(img.shape[0]*1.3), round(img.shape[1]*1)))
        x = newpnt[0][0][0]
        y = newpnt[0][0][1]

        # Rotate 90 clkwise
        if x < 0 and y > 0:
            new = cv2.rotate(new, cv2.ROTATE_90_CLOCKWISE)

        # Rotate 270 clkwise
        elif x > 0 and y < 0:
            new = cv2.rotate(new, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Rotate 180 clkwise
        elif x > 0 and y > 0:
            new = cv2.rotate(new, cv2.ROTATE_180)

        return new

    # Draw points on neighbourhood of given corner
    def draw_points(self, frame, corner):
        frame[round(corner[1]-1), round(corner[0])] =  (0,255,255)
        frame[round(corner[1]+1), round(corner[0])] =  (0,255,255)
        frame[round(corner[1]+1), round(corner[0])-1] =  (0,255,255)
        frame[round(corner[1]-1), round(corner[0])-1] =  (0,255,255)
        frame[round(corner[1]-1), round(corner[0])+1] =  (0,255,255)
        frame[round(corner[1]+1), round(corner[0])+1] =  (0,255,255)
        frame[round(corner[1]), round(corner[0])] = (0,255,255)

    def main_loop(self, callback):
        # Loop while on
        while True:
            # Find all the chess board corners
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            retvals, corners = cv2.findChessboardCorners(gray, (7,7))
            #print(retvals, corners)
            # Draw points on them
            if retvals:
                for board in corners:

                    for corner in board:
                        pass
                        #self.draw_points(frame, corner)
            blue, red = self.detect_pieces(frame)
            # cv2.imshow('frame', cv2.bitwise_and(frame, frame, mask=blue))

            if corners is not None:
                # Find outermost corners
                outermost = VisionEngine.find_outermost_corners(corners)
                # Transform to centre image
                board = self.homographied(frame, outermost)
                cv2.imshow('frame',board)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release capture stream
        self.cap.release()
        cv2.destroyAllWindows()

a = VisionEngine()
# a.main_loop(lambda x: x)
img = cv2.imread("C:/Users/sktap/OneDrive/Desktop/Sheridan/UNIVERISTY/2020/Semester 2/Hackathon/CheckerBOT/checkers-master (2)/checkers-master/WIN_20201017_12_24_47_Pro.jpg", cv2.IMREAD_UNCHANGED)
img = np.array(img)
while True:
    img1 = VisionEngine.detect_pieces(img)
    cv2.imshow('frame', np.array(img1[0]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
