makeAverageFromVideo

Repo created to exchange and test an idea about averaging igrams from video. Initial idea by barbidule! and discussion with chantepierre
TODO

    update readme with explanation about the idea and some pictures
    add a licence file (or not for the moment)


- makeAverage.py is a very simple script that creates averages images. the size of the averaged bin is roughly the square root of the total number of frames in the input video (e.g. 10 averages for 100+ frames).

Usage

./makeAverage.py --input <input_file> --output_dir <output_dir> --select_channel {R, G, B} [--output_avg]

Where :

    <input_file> is the path of your input video. OpenCV uses ffmpeg under the hood, refer to ffmpeg for supported formats.
    <output_dir> is the directory where averaged PNG files will be written.
    <channel> is one of R, G, or B
    --output_avg is optional and will trigger the write of an average.png file in the output directory.


- makeDiffImagesFromVideo is a attempt to create useful interferograms in adverse conditions.

this script allows to select a tight region of interest (ROI) around the first interferogram in the input video to later ease the identification of two images with high spatial standard deviation within a sample duration of one second. the coordinates of the ROI is printed in the terminal for further usage.
for each second duration of the input video two images are substracted each to other and the result in saved.
a total video duration of at least one hundred seconds is a nice value to average air currents and vibrations sources out. 

Usage

./makeDiffImagesFromVideo.py  --input_file <input_file> --output_dir <output_dir> --select_channel  {R, G, B} --roi_lst 999 999 999 999 [--output_avg]

Where :

    <input_file> is the path of your input video. OpenCV uses ffmpeg under the hood, refer to ffmpeg for supported formats.
    <output_dir> is the directory where averaged PNG files will be written.
    <channel> is one of R, G, or B
    --output_avg is optional and will trigger the write of an average.png file in the output directory.
    --roi_lst is an optional list of four coordinates of the ROI that can be in use for a serie of videos with (nearly) the same interferogram position in the image .


Installation Guide
Prerequisites

    Python 3.7 or higher
    pip (Python package installer)

Installation Steps

Create a virtual environment :

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required packages via pip :

pip install -r requirements.txt
