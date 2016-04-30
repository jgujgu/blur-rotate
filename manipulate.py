import sys
import os
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
import pandas as pd

class ImageManipulator(object):
    def __init__(self, driver_csv):
        self.driver_csv = driver_csv
        self.driver_csv_file = open(driver_csv, 'a')
        self.driver_csv_file.write("\n")

    def make_manipulated_images(self):
        driver_df = pd.read_csv(self.driver_csv)
        zip_drivers = zip(driver_df['subject'], driver_df['classname'], driver_df['img'])
        self.make_images(zip_drivers)

    def make_images(self, zip_drivers):
        for driver in zip_drivers:
            subject = driver[0]
            classname = driver[1]
            image_name = driver[2]
            src_dir = classname
            self.rotate(image_name, src_dir, subject)

    def write_row(self, subject, classname, image, action):
        csv_row = ",".join([subject, classname, image, action, "\n"])
        self.driver_csv_file.write(csv_row)

    def rotate(self, image_name, src_dir, subject):
        action = "rotate"
        degrees_bottom = -15
        degrees_top = 16
        print(action)
        print(image_name)
        for degree in range(degrees_bottom, degrees_top):
            image = misc.imread(src_dir + "/" + image_name)
            if degree == 0:
                pass
            else:
                rotate_img = ndimage.rotate(image, degree, reshape=False)
                new_image_name = action + str(degree) + "_" + image_name
                self.write_row(subject, src_dir, new_image_name, action)
                misc.imsave(src_dir + "/" + new_image_name, rotate_img)

if __name__ == '__main__':
    driver_csv = sys.argv[1]
    image_manipulator = ImageManipulator(driver_csv)
    image_manipulator.make_manipulated_images()
    image_manipulator.driver_csv_file.close()
