from copy import deepcopy
import time
import math


class Robot:

    def __init__(self, l1=0, l2=0):

        self.l1 = l1        # Length of first arm
        self.l2 = l2        # Length of second arm
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0


    def return_default_pos(self):


    def get_ee1_pos(self):
        x1 = self.l1 * math.cos(self.a1)
        y1 = self.l1 * math.sin(self.a1)
        z1 = self.l1 * math.sin(self.a2)
        return (x1, y1, z1)


    def get_grip_pos(self):
        x1, y1, z1 = self.get_ee1_pos()
       # x2 = x1 + self.l2 * math



    def move_to(self, x, y, z):
        """

        :param x: x coordinate on checkerboard
        :param y: y coordinate on checkerboard
        :return: None
        """

    def grab(self):


    def release(self):


