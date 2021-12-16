''' Script for leveling corn rows'''
from pathlib import Path
import glob
import sys
import os

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import cv2

sys.path.insert(0, '../src/')

from align import level_maize_img, rotate_image

home = Path.home()
path = home / 'Desktop' / 'github' / 'cs6670' / 'data' / 'RawData'

for f in path.glob("*"):
    for p in tqdm(sorted(list(f.glob("*_4.tif")))):
        img = cv2.imread(str(p))[:,:,2]
        ind = level_maize_img(img, angle_range=(-20, 20), angle_steps=20)
        
        rotated_image = rotate_image(img, ind)

        filename = os.path.basename(p)
        filename = filename[:filename.index('.tif')]
        cv2.imwrite(str(f)+'/'+filename+'.png', rotated_image)
