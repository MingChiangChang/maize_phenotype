import os
import glob
import json

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

from seg_align import find_blocks, add_extra_blocks, plot_continous_boxes

folders = ['MusgraveG2FUAV_06292020',
           'MusgraveG2FUAV_07092020',
           'RawData']

for folder in folders:
    print(f"Working on /Users/mingchiang/Desktop/github/cs6670/data/{folder}")
    sub_folders = sorted(glob.glob(f'/Users/mingchiang/Desktop/github/cs6670/data/{folder}/*'))
    for sub_folder in sub_folders:
        os.chdir(sub_folder)
        png_ls = sorted(glob.glob("*.png"))
        print(f"Found {len(png_ls)} images in {sub_folder}")
        for png in tqdm(png_ls):
            data = plt.imread(png)

            final_dic = {}
            final_dic['image'] = os.path.basename(png)

            #plt.imshow(data)
            #plt.show()

            block_peaks = find_blocks(data, plot=False, height=1)
            blocks = []

            annotation = []
            for idx, peak in enumerate(block_peaks):
                if idx + 1 < len(block_peaks):
                    #blocks.append(data[:,peaks[idx]:peaks[idx+1]])
                    #plt.imshow(data[:,peaks[idx]:peaks[idx+1]])
                    #plt.show()
                    block = data[:,block_peaks[idx]:block_peaks[idx+1]]

                    x = (block_peaks[idx+1] + block_peaks[idx])/2
                    width = block_peaks[idx+1] - block_peaks[idx]
                    #for idx, block in enumerate(blocks):
                    h_peaks = find_blocks(block, predicted_block_width=30,
                                          axis=1, height=-2, plot=False, rev=True,
                                          prominence=0.3)
                    add_extra_blocks(h_peaks)
                    
                    for j, h_peak in enumerate(h_peaks):
                        if j + 1 < len(h_peaks):
                            y = (h_peaks[j+1]+h_peaks[j])/2
                            height = h_peaks[j+1]-h_peaks[j]
                            annotation_dic = {}
                            annotation_dic['label'] = 'maize'

                            dic = {'x': float(x),
                                   'y': float(y),
                                   'width': float(width),
                                   'height': float(height)}
                            
                            annotation_dic['coordinates'] = dic
                            annotation.append(annotation_dic)
            
            final_dic['annotations'] = annotation
            final_output = [final_dic]

            with open(os.path.basename(png[:-4])+'.xml.json', 'w') as f:
                json.dump(final_output, f )
