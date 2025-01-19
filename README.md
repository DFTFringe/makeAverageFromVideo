# makeAverageFromVideo

Repo created to exchange and test an idea about averaging igrams from video.
Initial idea by barbidule! and discussion with chantepierre

# TODO

- update readme with explanation about the idea and some pictures
- add a licence file (or not for the moment)

## Usage

```bash
./makeAverage.py --input <input_file> --output_dir <output_dir> --select_channel {R, G, B} [--output_avg]
```

Where :
- `<input_file>` is the path of your input video. OpenCV uses ffmpeg under the hood, refer to ffmpeg for supported formats.
- `<output_dir>` is the directory where averaged PNG files will be written.
- `<channel>` is one of `R`, `G`, or `B`
- `--output_avg` is optional and will trigger the write of an `average.png` file in the output directory.

## Installation Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

Create a virtual environment :

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required packages via pip :
```bash
pip install -r requirements.txt
```
