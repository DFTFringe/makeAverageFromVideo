#!/usr/bin/env python3

import numpy as np
import cv2
import argparse
from pathlib import Path
import time

def process_video(input_file, output_dir, channel, output_avg):
    """
    Process video file by computing running average and differences of a specific color channel

    Args:
        input_file (str): Path to input video file
        output_dir (str): Directory to save output images
        channel (int): Color channel to process (0=blue, 1=green, 2=red)
        output_avg (bool): Optional : also output the substracted average
    """
    start_time = time.time()

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # First pass: compute average
    vd = cv2.VideoCapture(input_file)
    if not vd.isOpened():
        raise ValueError(f"Could not open video file: {input_file}")

    success, image = vd.read()
    if not success:
        raise ValueError("Could not read first frame")

    sumImg = image[:,:,channel] * 1.0

    count = 1
    while success:
        success, image = vd.read()
        if success:
            count += 1
            sumImg += image[:,:,channel] * 1.0

    avgImg = sumImg / (count * 1.0)
    sumImg *= 0.0

    binSize = int(np.sqrt(count))
    print(f"total {count} frames in this video. Averages over {binSize} frames")

    vd.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, image = vd.read()
    sumImg = image[:,:,channel] * 1.0 - avgImg

    count = 1
    while success:
        success, image = vd.read()
        if success:
            count += 1
            sumImg += image[:,:,channel] * 1.0 - avgImg

            # Save intermediate results every some frames
            if count % binSize == 0:
                # Normalize image to 0-255 range
                sumImg -= np.min(sumImg)
                if np.max(sumImg) > 0:  # Avoid division by zero
                    sumImg *= 255.0/np.max(sumImg)

                output_path = Path(output_dir) / f'frame_{count}_channel_{channel}_avg.png'
                cv2.imwrite(str(output_path), sumImg.astype(np.uint8))
                sumImg *= 0.0

    if output_avg :
        output_path = Path(output_dir) / 'average.png'
        print(f"Writing output noise to {output_path}")
        cv2.imwrite(str(output_path), avgImg.astype(np.uint8))

    vd.release()

    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description='Process video channels and compute running averages')
    parser.add_argument('--input_file', required=True, help='Input video file path')
    parser.add_argument('--output_dir', required=True, help='Output directory for processed images')
    parser.add_argument('--output_avg', type=bool, help='Whether to output a noise.png showing what was removed')
    parser.add_argument('--select_channel', type=str, choices=['B', 'G', 'R'], required=True,
                      help='Select color channel (B=blue, G=green, R=red)')

    args = parser.parse_args()

    try:
        channel_map = {'B': 0, 'G': 1, 'R': 2}
        process_video(args.input_file, args.output_dir, channel_map[args.select_channel], args.output_avg)
        print(f"Processing complete. Output saved to {args.output_dir}")
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
