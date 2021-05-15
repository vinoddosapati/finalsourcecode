import numpy as np
import sys
from os import listdir
import os
from random import shuffle
import matplotlib.image as mpimg
import cv2
import csv
from csvgenerate import mergingAll

# process the dataset
def process_data(names, latex_key, img_path, save_path, close_kernel=None, dilate_kernel=None, tr_cv_split=80):
    if close_kernel is None:
        close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    if dilate_kernel is None:
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    key = {}
    for k, name in enumerate(names):
        sys.stdout.write(name + "\n")
        # create key
        key[k] = latex_key[name] if(name in latex_key) else  name.lower()
        # get files of images
        imgs = []
        img_files = listdir(img_path + name + '\\')
        shuffle(img_files)
        trainpath = save_path + 'tr\\'
        testpath =  save_path + 'cv\\'
        test_extension = '_cv.csv'
        train_extension = '_tr.csv'
        # each image of component to a train or test component .csv file
        for i, img_file in enumerate(img_files):
            file = img_path + name + '\\' + img_file
            img = mpimg.imread(file)
            # convert to binary and close + dilate
            if close_kernel is None:
                close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
            if dilate_kernel is None:
                dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            new_img = img < 127
            new_img = new_img.astype(np.uint8)
            new_img = cv2.morphologyEx(new_img, cv2.MORPH_CLOSE, close_kernel)
            new_img = cv2.dilate(new_img, dilate_kernel)
            img = new_img

            imgs.append(np.append(img.ravel(), k))
            # print progress
            files_len = len(img_files)
            sys.stdout.write('\r')
            sys.stdout.write('{:.2%}'.format(i / files_len))
            sys.stdout.flush()
        sys.stdout.write('\r100.00%\n')

        # split into training and validation sets and save csv
        arr = np.asarray(imgs)
        number = 100
        ind = len(img_files) * tr_cv_split // number
        np.savetxt(trainpath + name + train_extension, arr[:ind], delimiter=',', fmt='%i')
        np.savetxt(testpath + name + test_extension, arr[ind:], delimiter=',', fmt='%i')

    # save key
    if save_path:
        path = save_path + 'dict.csv'
        with open(path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in key.items():
                writer.writerow([key, value])

latex_key = {
    '(': '\\left(',
    ')': '\\right)',
    'alpha': '\\alpha',
    'ascii_124': '|',
    'beta': '\\beta',
    'cos': '\\cos',
    'Delta': '\\Delta',
    'div': '\\div',
    'exists': '\\exists',
    'forall': '\\forall',
    'forward_slash': '/',
    'gama': '\\gamma',
    'geq': '\\geq',
    'gt': '>',
    'infty': '\\infty',
    'int': '\\int',
    'in': '\\in',
    'lambda': '\\lambda',
    'ldots': '\\ldots',
    'leq': '\\leq',
    'lim': '\\lim',
    'log': '\\log',
    'lt': '<',
    'mu': '\\mu',
    'neq': '\\neq',
    'phi': '\\phi',
    'pi': '\\pi',
    'pm': '\\pm',
    'prime': '\'',
    'rightarrow': '\\rightarrow',
    'sigma': '\\sigma',
    'sin': '\\sin',
    'sqrt': '\\sqrt',
    'sum': '\\sum',
    'tan': '\\tan',
    'theta': '\\theta',
    'times': '\\times',
    '[': '\\left[',
    ']': '\\right]',
    '{': '\\left{',
    '}': '\\right}'
}


print("Split train and test spliting........")
# convert images to csv
img_path = '.\\extracted_images\\'
img_names = listdir(img_path)
save_path = '.\\savedata\\'
# Combine all train and all test generate dict
tr_path = save_path+'tr\\'
cv_path = save_path+'cv\\'
if not os.path.exists(tr_path):
    os.makedirs(tr_path)
if not os.path.exists(cv_path):
    os.makedirs(cv_path)
# process the dataset
# each image of component to a train or test component .csv file
process_data(img_names, latex_key, img_path, save_path)

print("combine and dict...........")

# merging all component .csv files to train, test .csv files
mergingAll(img_names, tr_path, cv_path, save_path)
