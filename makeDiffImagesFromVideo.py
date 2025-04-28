#!/usr/bin/env python3

import numpy as np
import cv2
import argparse
from pathlib import Path
import time
import matplotlib.pyplot as plt

def process_video(input_file, output_dir, channel, roi_lst):
    """
    Process video file by computing running average and differences 
    of a specific color channel

    Args:
        input_file (str): Path to input video file
        output_dir (str): Directory to save output images
        channel (int): Color channel to process (0=blue, 1=green, 2=red)
        roi_lst list of integers defining the ROI
    """
    start_time = time.time()

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    vd = cv2.VideoCapture(input_file)

    if not vd.isOpened():
        raise ValueError(f"Could not open video file: {input_file}")

    fps = int(np.rint(vd.get(cv2.CAP_PROP_FPS)))
    vd.set(cv2.CAP_PROP_POS_FRAMES, fps)

    success, image = vd.read()
    if not success:
        raise ValueError("Could not read first frame")

    fnm_base = input_file.split('.')[0]

    bS = fps + fps % 2
    # imDims = image.shape
    # tab = np.zeros((bS,imDims[0],imDims[0]),dtype=np.uint8)

    tmpImg = image[:,:,channel]
    sat = 250
    tmpImg *= (tmpImg < sat)
    # mdl = np.argmax(
    #     np.convolve(np.sum(tmpImg,axis=0),np.ones((imDims[1])),mode='same'))
    # dbt = int(mdl - imDims[0]/2)
    # fin = int(mdl + imDims[0]/2)
        
    if roi_lst is None:
        
        windowName = 'Select ROI (usage: read prompt)'
        roi = np.asarray(cv2.selectROI(windowName, tmpImg, False, False))
        cv2.destroyWindow(windowName)
    
    else:
        
        roi = np.asarray(roi_lst)
        
    print(' '.join(map(str, roi)))

    imDims = (tmpImg[roi[1]:roi[1]+roi[3],
                     roi[0]:roi[0]+roi[2]].shape)
    tab = np.zeros((bS,imDims[0],imDims[1]),dtype=np.uint8)
           
    count = 1
    i = 0
    while success:
        success, image = vd.read()
        if success:
            
            tab[i,:,:] = image[:,:,channel][roi[1]:roi[1]+roi[3],
                                            roi[0]:roi[0]+roi[2]]
            i += 1
            # Save selected intermediate results every some frames
            if count % (bS) == 0:

                tmpImg = tab.copy().astype(np.int16)
                tmpImg *= (tmpImg < sat)
                imgStd1 = np.std(tmpImg-np.mean(tmpImg,axis=0)[None,:,:],
                                 axis=(1,2))
                i_s = np.argsort(-imgStd1)
                # bst1 = imgStd1[i_s[0]]
                tmpImg = tmpImg[i_s[1:],:,:] - tmpImg[i_s[0],:,:][None,:,:]
                imgStd2 = np.std(tmpImg,axis=(1,2))
                i_b = np.argmax(imgStd2)
                # bst2 = imgStd1[i_s[i_b+1]]
                # print(np.round(bst1,1),np.round(bst2,1))
                im2wr = tmpImg[i_b,:,:]
                im2wr -= np.min(im2wr)
                output_path = Path(output_dir) / f'dif_{fnm_base}_{count}.jpeg'
                cv2.imwrite(str(output_path), im2wr.astype(np.int16))
                
                i = 0

            count += 1

    vd.release()

    end_time = time.time()

    print(f"Total processing time: {end_time - start_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(
        description='Process video channels and compute running averages')
    parser.add_argument(
        '--input_file', required=True, help='Input video file path')
    parser.add_argument(
        '--output_dir', required=True,
        help='Output directory for processed images')
    parser.add_argument(
        '--select_channel', type=str, choices=['B', 'G', 'R'], required=True,
                      help='Select color channel (B=blue, G=green, R=red)')
    parser.add_argument(
        '--roi_lst', nargs=4, action='store', required=False, type=int,
        help='list of four ints defining the roi, e.g: 574 108 728 721')

    args = parser.parse_args()

    try:
        channel_map = {'B': 0, 'G': 1, 'R': 2}
        if args.roi_lst == None:
            
            process_video(args.input_file, args.output_dir,
                          channel_map[args.select_channel], None)
        
        else:
            
            process_video(args.input_file, args.output_dir,
              channel_map[args.select_channel], args.roi_lst)

        print(f"Processing complete. Output saved to {args.output_dir}")
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
