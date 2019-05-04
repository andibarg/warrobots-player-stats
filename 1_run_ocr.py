# Load all screenshots of player statistics, crop, run OCR,
# sort into dataframe and save as csv.
#
# Should be run as a first step of the analysis (before
# 2_analyze_ocr.py). Specify folder of screenshots
# (png-format) in /data subfolder.

import os
import pytesseract
import numpy as np
import cv2
from tqdm import tqdm
import pandas as pd

# User input
screenshot_folder = 'iOS_LL_2019-04-28'
show_screenshots = True
savetofile = True

# Find all screenshots
dpath = os.path.join(os.getcwd(),'data',screenshot_folder)
dfiles = os.listdir(dpath)
dfiles = [i for i in dfiles if (i.endswith('.PNG')|i.endswith('.png'))]

# Get text positions from file
ocrpos = np.loadtxt(os.path.join(os.getcwd(),'other','text_pos.csv'),
                    skiprows=1,delimiter=',')

# Initiate csv data file
if savetofile:
    dname = os.path.join(os.path.dirname(dpath),screenshot_folder + '.csv')
    np.savetxt(dname,[],header='Rank,Robot,Weapon',comments='',fmt="%s")

# Loop through screenshots
for ii in tqdm(range(len(dfiles))):
    # Load image
    img = cv2.imread(os.path.join(dpath,dfiles[ii]),0)
    
    # Convert to binary image
    threshold = cv2.adaptiveThreshold(img, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV,201,-35)

    # Loop through text positions
    for jj in range(ocrpos.shape[0]):
        # Crop
        crop_img = threshold[int(ocrpos[jj,2]):int(ocrpos[jj,3]),
                             int(ocrpos[jj,4]):int(ocrpos[jj,5])]

        # OCR
        text = pytesseract.image_to_string(crop_img,
                                           config=('--psm 7 -l eng'))

        # Make dataframe and save
        if ocrpos[jj,1] == 0:
            Robot = text
        else:
            row = pd.DataFrame(pd.Series([ii+1,Robot,text],
                index=['Rank','Robot','Weapon'])).T.set_index('Rank')           
            # Append dataframe to csv
            if savetofile:
                with open(dname, 'a') as f:
                    row.to_csv(f, header=False)

        # Plot
        if show_screenshots:
            # Add rectangle around text postion in figure
            imgrect = cv2.rectangle(cv2.resize(img, (683, 512)),
                ( int(int(ocrpos[jj,4])/3), int(int(ocrpos[jj,2])/3)),
                ( int(int(ocrpos[jj,5])/3),int(int(ocrpos[jj,3])/3) ),
                (255,0,0), 2)
            cv2.imshow('Running OCR ...',imgrect)
            cv2.waitKey(1)
            
if show_screenshots:
    cv2.destroyAllWindows()
